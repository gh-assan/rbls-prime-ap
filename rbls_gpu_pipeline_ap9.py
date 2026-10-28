"""
RBLS GPU Pipeline - AP-9 Search
=================================
Searches for 9-term arithmetic progressions of primes near the LLL-resonant target.

For k=9: primorial of primes <= 9 = 2*3*5*7 = 210
"""
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import sympy
from sympy import Matrix, primerange
import math
import time

# =====================================================================
# 0. PRIMORIAL CALCULATION
# =====================================================================

def get_required_primorial(k):
    """Calculates the product of all primes <= k."""
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 1. CUDA KERNEL
# =====================================================================
cuda_source = """
typedef unsigned long long uint64;

// Russian peasant multiplication (safe for n < 2^64, no __int128 needed)
__device__ inline uint64 mul_mod(uint64 a, uint64 b, uint64 m) {
    uint64 r = 0; a %= m;
    while (b > 0) { if (b & 1) r = (r >= m - a ? r - (m - a) : r + a); a = (a >= m - a ? a - (m - a) : a + a); b >>= 1; }
    return r;
}

__device__ uint64 pow_mod(uint64 base, uint64 exp, uint64 mod) {
    uint64 res = 1; base %= mod;
    while (exp > 0) { if (exp & 1) res = mul_mod(res, base, mod); base = mul_mod(base, base, mod); exp >>= 1; }
    return res;
}

__device__ bool is_prime(uint64 n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    uint64 d = n - 1; int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    const uint64 witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        uint64 a = witnesses[i]; if (n <= a) break;
        uint64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) { x = mul_mod(x, x, n); if (x == n - 1) { composite = false; break; } }
        if (composite) return false;
    }
    return true;
}

__global__ void evaluate_progressions(uint64* candidates, uint64 d_step, int k_len, int* results, int num_candidates) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_candidates) return;
    uint64 base_a = candidates[idx];
        if (k_len < 2 || d_step == 0 ||
            (uint64)(k_len - 1) > (~(uint64)0 - base_a) / d_step) {
            results[idx] = 0; return;
        }
    bool valid = true;
    for (int j = 0; j < k_len; j++) {
        if (!is_prime(base_a + j * d_step)) { valid = false; break; }
    }
    results[idx] = valid ? 1 : 0;
}
"""

# =====================================================================
# 2. LLL RESONANCE TARGETING
# =====================================================================
def get_resonance_parameters(k_length):
    import warnings
    warnings.warn("Legacy LLL scaling does not preserve phase alignment; "
                  "use search_prime_ap.py for the modular search.", RuntimeWarning)
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION] ---")
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    target_ln = math.log(10**15)
    C = 10**8
    A = [int(alpha * C) for alpha in alphas]
    M = Matrix([[C, 0, 0, 0], [0, C, 0, 0], [0, 0, C, 0], [A[0], A[1], A[2], 1]])
    L = M.lll()
    base_q = abs(L[0, 3])
    if base_q == 0: base_q = 1
    final_q = base_q * int(target_ln * C / base_q)
    y = final_q / C
    a_target = int(math.exp(y))
    d_step = get_required_primorial(k_length)
    print(f"LLL complete. ln(a)={y:.6f}, a={a_target:,}, d={d_step}")
    return a_target, d_step

# =====================================================================
# 3. GPU DISPATCHER - Chunked with progress every ~10s
# =====================================================================
def run_gpu_sieve_chunked(mod, candidate_array, common_difference, k_length, batch_label):
    total = len(candidate_array)
    fn = mod.get_function("evaluate_progressions")
    threads = 256
    chunk_size = 10_000_000  # Process entire batch in one chunk

    all_matches = []
    processed = 0
    t_start = time.time()
    last_report = t_start

    for offset in range(0, total, chunk_size):
        end = min(offset + chunk_size, total)
        chunk = np.ascontiguousarray(candidate_array[offset:end], dtype=np.uint64)
        n = len(chunk)

        # Alloc GPU mem
        d_chunk = cuda.mem_alloc(chunk.nbytes)
        d_res = cuda.mem_alloc(n * 4)
        cuda.memcpy_htod(d_chunk, chunk)
        cuda.memset_d8(d_res, 0, n * 4)

        # Launch kernel
        blocks = (n + threads - 1) // threads
        fn(d_chunk, np.uint64(common_difference), np.int32(k_length), d_res, np.int32(n),
           block=(threads, 1, 1), grid=(blocks, 1))
        cuda.Context.synchronize()

        # Read back
        h_res = np.zeros(n, dtype=np.int32)
        cuda.memcpy_dtoh(h_res, d_res)
        d_chunk.free()
        d_res.free()

        # Collect matches
        found = np.where(h_res == 1)[0]
        for idx in found:
            all_matches.append(chunk[idx])

        processed += n
        now = time.time()
        if now - last_report >= 10 or processed >= total:
            pct = 100 * processed / total
            rate = processed / (now - t_start)
            eta = (total - processed) / rate if rate > 0 else 0
            print(f"  {batch_label}: {pct:.0f}% ({processed:,}/{total:,})"
                  f" | {len(all_matches)} found | {rate:,.0f}/s | ETA {eta:.0f}s")
            last_report = now

        if len(all_matches) > 0:
            break

    return all_matches

# =====================================================================
# 4. ESTIMATE
# =====================================================================
def estimate_probability(k, d):
    ln_n = math.log(10**15)
    singular = 1.0
    for p in sympy.primerange(2, 100_000):
        residues = len({(j * d) % p for j in range(k)})
        if residues == p:
            singular = 0.0
            break
        singular *= (1.0 - residues / p) / ((1.0 - 1.0 / p) ** k)
    p_ap = singular / (ln_n ** k) if singular else 0.0
    print(f"\n--- AP-{k} Estimate ---")
    print(f"d={d}, singular series≈{singular:.3e}")
    print(f"P(AP-{k})≈{p_ap:.2e}, expected raw candidates≈{1/p_ap:.2e}")
    return 1.0 / p_ap

# =====================================================================
# 5. MAIN
# =====================================================================
if __name__ == "__main__":
    k_length = 9
    d_step = get_required_primorial(k_length)
    print(f"AP-{k_length} search, d={d_step}")

    expected_candidates = estimate_probability(k_length, d_step)

    print("\nCompiling CUDA kernel...")
    mod = SourceModule(cuda_source)
    print("CUDA compilation successful.\n")

    target_a, d_step = get_resonance_parameters(k_length)

    batch_size = 10_000_000
    max_batches = 500

    print(f"\n--- [GPU SIEVE] ---")
    print(f"k={k_length}, d={d_step}, batch={batch_size:,}, max={max_batches}")

    overall_start = time.time()
    total_found = 0
    batch_num = 11  # Resume from batch 11 (already searched 10 batches)

    while batch_num <= max_batches:
        current_start = target_a + ((batch_num - 1) * batch_size)
        print(f"\nBatch {batch_num}: {current_start:,} ...")

        candidates = np.arange(current_start, current_start + batch_size, dtype=np.uint64)

        t0 = time.time()
        matches = run_gpu_sieve_chunked(mod, candidates, d_step, k_length, f"Batch {batch_num}")
        t1 = time.time()

        print(f"  Batch {batch_num} done: {t1-t0:.1f}s, {len(matches)} found")

        # Cooling pause: 10% of batch time, max 30 seconds
        if batch_num > 11:
            cool_time = min(30, (t1 - t0) * 0.1)
            if cool_time > 1:
                print(f"  Cooling {cool_time:.0f}s to lower GPU temperature...")
                time.sleep(cool_time)

        if matches:
            print("\n" + "=" * 70)
            print(f"*** FOUND AP-{k_length}! ***")
            print("=" * 70)
            for idx, m in enumerate(matches):
                print(f"\nProgression #{idx+1} starting at {m}:")
                for i in range(k_length):
                    print(f"  Index {i}: {m + i*d_step}")
            total_found += len(matches)
            break

        if batch_num == 11:
            remaining_batches = max_batches - 11 + 1
            print(f"  Est total for remaining {remaining_batches} batches: {((t1-t0)*remaining_batches)/3600:.1f}h")

        batch_num += 1

    overall_end = time.time()
    searched = (batch_num - 1) * batch_size
    print(f"\n--- [DONE] ---")
    print(f"Searched {searched:,} candidates in {overall_end-overall_start:.2f}s")
    print(f"AP-{k_length} found: {total_found}")
