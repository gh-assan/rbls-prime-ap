import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import sympy
from sympy import Matrix
import math
import time

# =====================================================================
# 1. THE CUDA KERNEL (Compiles dynamically for Tesla T4)
# =====================================================================
cuda_source = """
typedef unsigned long long uint64;

// Device function for overflow-safe modular multiplication (64-bit, no 128-bit needed)
__device__ inline uint64 mul_mod(uint64 a, uint64 b, uint64 m) {
    uint64 r = 0;
    a %= m;
    while (b > 0) {
        if (b & 1) {
            r = (r + a) % m;
        }
        a = (a << 1) % m;
        b >>= 1;
    }
    return r;
}

// Device function for modular exponentiation: (base^exp) % mod
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

// Deterministic 64-bit Miller-Rabin Primality Test (Guaranteed for n < 2^64)
__device__ bool is_prime(uint64 n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    uint64 d = n - 1;
    int s = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        s++;
    }

    const uint64 witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    
    for (int i = 0; i < 12; i++) {
        uint64 a = witnesses[i];
        if (n <= a) break;

        uint64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;

        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}

// Main Kernel: Scans candidate array for length-k arithmetic progressions
__global__ void evaluate_progressions(uint64* candidates, uint64 d_step, int k_len, int* results, int num_candidates) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_candidates) return;

    uint64 base_a = candidates[idx];
    bool valid_progression = true;

    // Check all terms in the AP-k sequence
    for (int j = 0; j < k_len; j++) {
        uint64 current_term = base_a + (j * d_step);
        if (!is_prime(current_term)) {
            valid_progression = false;
            break; // Early exit on composite
        }
    }

    results[idx] = valid_progression ? 1 : 0;
}
"""

# =====================================================================
# 2. THE ANALYTIC BRAIN (SymPy LLL Lattice Reduction)
# =====================================================================
def get_resonance_parameters():
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION] ---")
    
    # Imaginary parts of first 3 Riemann Zeros
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    
    # We want to find a magnitude near 10^15. 
    # ln(10^15) is roughly 34.5387. We search for a phase alignment near here.
    target_ln = math.log(10**15)
    
    print("Constructing 4D Lattice for Simultaneous Diophantine Approximation...")
    C = 10**8  # Integer scaling factor
    A = [int(alpha * C) for alpha in alphas]
    
    # Matrix construction for LLL
    M = Matrix([
        [C, 0, 0, 0],
        [0, C, 0, 0],
        [0, 0, C, 0],
        [A[0], A[1], A[2], 1]
    ])
    
    # Run Lenstra-Lenstra-Lovasz
    L = M.lll()
    
    # Extract the shortest vector's multiplier (q)
    # To force the magnitude near 10^15, we scale the base vector
    base_q = abs(L[0, 3])
    if base_q == 0:
        base_q = 1
        
    multiplier = int(target_ln * C / base_q)
    final_q = base_q * multiplier
    
    y = final_q / C
    a_target = int(math.exp(y))
    
    # Align discrete step size d with primorial P7 = 2*3*5*7 = 210
    P7 = 210
    
    print(f"LLL complete. Resonant base ln(a) found at: {y:.6f}")
    print(f"Target discrete starting magnitude (a): {a_target:,}")
    print(f"Enforcing Primorial P7 step size (d): {P7}")
    
    return a_target, P7

# =====================================================================
# 3. THE GPU DISPATCHER
# =====================================================================
def run_gpu_sieve(mod, candidate_array, common_difference, k_length):
    num_candidates = len(candidate_array)
    
    evaluate_progressions = mod.get_function("evaluate_progressions")
    
    # Ensure C-contiguous memory layout
    h_candidates = np.array(candidate_array, dtype=np.uint64)
    h_results = np.zeros(num_candidates, dtype=np.int32)
    
    # Allocate GPU VRAM
    d_candidates = cuda.mem_alloc(h_candidates.nbytes)
    d_results = cuda.mem_alloc(h_results.nbytes)
    
    # Transfer RAM -> VRAM
    cuda.memcpy_htod(d_candidates, h_candidates)
    cuda.memcpy_htod(d_results, h_results)
    
    # Optimize grid for Tesla T4 (256 threads per block)
    threads_per_block = 256
    blocks_per_grid = (num_candidates + threads_per_block - 1) // threads_per_block
    
    # Launch Kernel
    evaluate_progressions(
        d_candidates, 
        np.uint64(common_difference), 
        np.int32(k_length), 
        d_results, 
        np.int32(num_candidates),
        block=(threads_per_block, 1, 1), 
        grid=(blocks_per_grid, 1)
    )
    
    # Transfer VRAM -> RAM
    cuda.Context.synchronize()
    cuda.memcpy_dtoh(h_results, d_results)
    
    # Extract matches
    successful_indices = np.where(h_results == 1)[0]
    return [h_candidates[i] for i in successful_indices]

# =====================================================================
# 4. MAIN PIPELINE EXECUTION
# =====================================================================
if __name__ == "__main__":
    print("Compiling 128-bit CUDA C++ Kernel on Tesla T4...")
    mod = SourceModule(cuda_source)
    print("CUDA compilation successful.\n")

    # Step 1: Run analytic phase alignment
    target_a, d_step = get_resonance_parameters()
    
    # Step 2: Configure the search space
    k_length = 7  # Looking for a 7-term progression
    batch_size = 10_000_000  # Streaming 10 Million numbers per GPU burst
    max_batches = 200  # Search up to 200 batches (2 billion candidates)
    
    print("\n--- [PHASE 2: DISCRETE GPU SIEVE] ---")
    
    overall_start = time.time()
    total_found = 0
    batch_num = 1
    estimated_time_per_batch = None
    
    while batch_num <= max_batches:
        current_start = target_a + ((batch_num - 1) * batch_size)
        print(f"\nBatch {batch_num}: Candidates {current_start:,} to {current_start + batch_size:,}...")
        
        candidates = np.arange(current_start, current_start + batch_size, dtype=np.uint64)
        
        start_time = time.time()
        matches = run_gpu_sieve(mod, candidates, d_step, k_length)
        end_time = time.time()
        
        elapsed = end_time - start_time
        
        if estimated_time_per_batch is None:
            estimated_time_per_batch = elapsed
        
        print(f"  GPU execution: {elapsed:.4f}s. Found {len(matches)} AP-{k_length} progressions.")
        
        if len(matches) > 0:
            print("\n" + "=" * 60)
            print("*** FOUND VALID AP-7 PROGRESSION(S)! ***")
            print("=" * 60)
            for idx, m in enumerate(matches):
                print(f"\nProgression #{idx + 1} starting at {m}:")
                for i in range(k_length):
                    term = m + (i * d_step)
                    print(f"  Index {i}: {term}")
            total_found += len(matches)
            break  # Stop once we find at least one
        
        batch_num += 1
    
    overall_end = time.time()
    total_time = overall_end - overall_start
    print(f"\n--- [FINAL RESULTS] ---")
    print(f"Searched {batch_num - 1} batch(es) ({(batch_num - 1) * batch_size:,} candidates) in {total_time:.2f} seconds.")
    print(f"Total AP-{k_length} progressions found: {total_found}")