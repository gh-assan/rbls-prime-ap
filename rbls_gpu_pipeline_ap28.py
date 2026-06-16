"""
RBLS GPU Pipeline - AP-28 Search
=================================
Novel algorithm: Uses GPU to find ALL primes in a range near the LLL-resonant target,
then scans prime positions for long arithmetic progressions using difference sets.

Key insight: Instead of testing every number as an AP starting point,
we find all primes first, then look for arithmetic patterns among them.
"""
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import sympy
from sympy import Matrix, primerange
import math
import time
from datetime import datetime

# =====================================================================
# 1. CUDA KERNEL
# =====================================================================
cuda_source = """
typedef unsigned long long uint64;

__device__ inline uint64 mul_mod(uint64 a, uint64 b, uint64 m) {
    uint64 r = 0;
    a %= m;
    while (b > 0) {
        if (b & 1) { r = (r + a) % m; }
        a = (a << 1) % m;
        b >>= 1;
    }
    return r;
}

__device__ uint64 pow_mod(uint64 base, uint64 exp, uint64 mod) {
    uint64 res = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp & 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp >>= 1;
    }
    return res;
}

__device__ bool is_prime(uint64 n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    uint64 d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    const uint64 witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        uint64 a = witnesses[i];
        if (n <= a) break;
        uint64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

__global__ void find_primes(uint64* start_nums, int* is_prime_out, int num_count) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_count) return;
    is_prime_out[idx] = is_prime(start_nums[idx]) ? 1 : 0;
}
"""

# =====================================================================
# 1b. PRIMORIAL CALCULATION
# =====================================================================

def get_required_primorial(k):
    """Calculates the product of all primes <= k."""
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 2. LLL RESONANCE TARGETING
# =====================================================================
def get_resonance_parameters(k_length):
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION] ---")
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    target_ln = math.log(10**15)
    
    print("Constructing 4D Lattice for Simultaneous Diophantine Approximation...")
    C = 10**8
    A = [int(alpha * C) for alpha in alphas]
    
    M = Matrix([
        [C, 0, 0, 0],
        [0, C, 0, 0],
        [0, 0, C, 0],
        [A[0], A[1], A[2], 1]
    ])
    
    L = M.lll()
    base_q = abs(L[0, 3])
    if base_q == 0: base_q = 1
    multiplier = int(target_ln * C / base_q)
    final_q = base_q * multiplier
    y = final_q / C
    a_target = int(math.exp(y))
    d_step = get_required_primorial(k_length)
    
    print(f"LLL complete. Resonant base ln(a) found at: {y:.6f}")
    print(f"Target discrete starting magnitude (a): {a_target:,}")
    print(f"Computed primorial step size (d): {d_step}")
    return a_target, d_step

# =====================================================================
# 3. GPU PRIME FINDER
# =====================================================================
def run_gpu_prime_finder(mod, numbers):
    n = len(numbers)
    h_nums = np.array(numbers, dtype=np.uint64)
    h_results = np.zeros(n, dtype=np.int32)
    d_nums = cuda.mem_alloc(h_nums.nbytes)
    d_results = cuda.mem_alloc(h_results.nbytes)
    cuda.memcpy_htod(d_nums, h_nums)
    cuda.memcpy_htod(d_results, h_results)
    find_primes = mod.get_function("find_primes")
    threads_per_block = 256
    blocks_per_grid = (n + threads_per_block - 1) // threads_per_block
    find_primes(d_nums, d_results, np.int32(n),
                block=(threads_per_block, 1, 1), grid=(blocks_per_grid, 1))
    cuda.Context.synchronize()
    cuda.memcpy_dtoh(h_results, d_results)
    return h_results.astype(bool)

# =====================================================================
# 4. AP SCANNER
# =====================================================================
def scan_ap_from_primes(primes_sorted, k_target, min_d, max_d, result_writer):
    prime_set = set(primes_sorted)
    found = []
    d_step = get_required_primorial(k_target)
    report_interval = max(1, len(primes_sorted) // 10)
    
    for idx, p in enumerate(primes_sorted):
        if idx % report_interval == 0 and idx > 0:
            pct = 100 * idx / len(primes_sorted)
            print(f"  AP scan: {pct:.0f}% ({idx:,}/{len(primes_sorted):,} primes)")
        
        max_reasonable_d = (primes_sorted[-1] - p) // (k_target - 1)
        limit = min(max_reasonable_d, max_d)
        
        for d in range(d_step, limit + 1, d_step):
            if p + (k_target - 1) * d > primes_sorted[-1]:
                break
            valid = True
            for j in range(1, k_target):
                if (p + j * d) not in prime_set:
                    valid = False
                    break
            if valid:
                found.append((p, d))
                terms = [p + j*d for j in range(k_target)]
                result_writer(f"*** FOUND AP-{k_target} starting at {p}, d={d} ***")
                for j, t in enumerate(terms):
                    result_writer(f"  Index {j}: {t}")
    return found

# =====================================================================
# 5. MAIN
# =====================================================================
if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"ap28_search_{timestamp}.txt"
    
    def write_result(msg):
        with open(log_file, 'a') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    
    write_result("RBLS GPU PIPELINE - AP-28 SEARCH")
    write_result("=" * 50)
    
    print("Compiling CUDA kernel...")
    mod = SourceModule(cuda_source)
    print("CUDA compilation successful.")
    
    k_target = 28
    target_a, d_step = get_resonance_parameters(k_target)
    write_result(f"LLL target: {target_a:,}")
    chunk_size = 100_000_000
    num_chunks = 10
    range_size = num_chunks * chunk_size
    required_span = (k_target - 1) * d_step
    if range_size <= required_span:
        msg = (
            f"Configured range ({range_size:,}) is too small for AP-{k_target} "
            f"with d={d_step:,}; need more than {required_span:,} numbers. "
            "Use a larger, memory-aware segmented scan before treating AP-28 "
            "results as meaningful."
        )
        print(msg)
        write_result(msg)
        raise SystemExit(1)

    all_primes = []
    
    print(f"\n--- [PHASE 2: PRIME COLLECTION] ---")
    print(f"Scanning {num_chunks}x{chunk_size:,} = {range_size:,} numbers")
    
    overall_start = time.time()
    
    for ci in range(num_chunks):
        chunk_start = target_a + ci * chunk_size
        print(f"\nChunk {ci+1}/{num_chunks}: {chunk_start:,} ... ", end="", flush=True)
        
        nums = np.arange(chunk_start, chunk_start + chunk_size, dtype=np.uint64)
        t0 = time.time()
        mask = run_gpu_prime_finder(mod, nums)
        t1 = time.time()
        
        chunk_primes = nums[mask].tolist()
        all_primes.extend(chunk_primes)
        
        print(f"{t1-t0:.1f}s, {len(chunk_primes):,} primes (total: {len(all_primes):,})", flush=True)
        del nums, mask
    
    all_primes.sort()
    print(f"\nTotal: {len(all_primes):,} primes collected")
    write_result(f"Primes collected: {len(all_primes):,}")
    
    # Phase 3
    max_d = range_size // (k_target - 1)
    
    print(f"\n--- [PHASE 3: AP-{k_target} SCAN] ---")
    print(f"Scanning {len(all_primes):,} primes, d from {d_step} to {max_d:,}")
    
    t2 = time.time()
    results = scan_ap_from_primes(all_primes, k_target, d_step, max_d, write_result)
    t3 = time.time()
    
    overall_end = time.time()
    total_hours = (overall_end - overall_start) / 3600
    
    print(f"\n--- [RESULTS] ---")
    print(f"Time: {total_hours:.2f} hours")
    print(f"Range: {target_a:,} to {target_a + range_size:,}")
    print(f"Primes: {len(all_primes):,}")
    print(f"AP-{k_target}: {len(results)} found")
    
    write_result(f"Total time: {total_hours:.2f}h")
    write_result(f"AP-{k_target} progressions found: {len(results)}")
    
    if results:
        file_ap = log_file.replace('.txt', '_ap.txt')
        with open(file_ap, 'w') as f:
            f.write(f"AP-{k_target} PROGRESSIONS - {timestamp}\n")
            f.write(f"Range: {target_a:,} to {target_a + range_size:,}\n\n")
            for p, d in results:
                f.write(f"Start: {p}, d = {d}\n")
                for j in range(k_target):
                    f.write(f"  {j}: {p + j*d}\n")
                f.write("\n")
        print(f"Results saved to: {file_ap}")
    
    print(f"Log saved to: {log_file}")
