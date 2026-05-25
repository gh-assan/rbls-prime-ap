import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

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

__global__ void evaluate_progressions(uint64* candidates, uint64 d_step, int k_len, int* results, int num_candidates) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_candidates) return;

    uint64 base_a = candidates[idx];
    bool valid_progression = true;

    for (int j = 0; j < k_len; j++) {
        uint64 current_term = base_a + (j * d_step);
        if (!is_prime(current_term)) {
            valid_progression = false;
            break;
        }
    }
    results[idx] = valid_progression ? 1 : 0;
}
"""

mod = SourceModule(cuda_source)

def run_gpu_sieve(candidate_array, common_difference, k_length):
    num_candidates = len(candidate_array)
    evaluate_progressions = mod.get_function("evaluate_progressions")
    
    h_candidates = np.array(candidate_array, dtype=np.uint64)
    h_results = np.zeros(num_candidates, dtype=np.int32)
    
    d_candidates = cuda.mem_alloc(h_candidates.nbytes)
    d_results = cuda.mem_alloc(h_results.nbytes)
    
    cuda.memcpy_htod(d_candidates, h_candidates)
    cuda.memcpy_htod(d_results, h_results)
    
    threads_per_block = 256
    blocks_per_grid = (num_candidates + threads_per_block - 1) // threads_per_block
    
    evaluate_progressions(
        d_candidates, np.uint64(common_difference), np.int32(k_length),
        d_results, np.int32(num_candidates),
        block=(threads_per_block, 1, 1), grid=(blocks_per_grid, 1)
    )
    
    cuda.Context.synchronize()
    cuda.memcpy_dtoh(h_results, d_results)
    
    successful_indices = np.where(h_results == 1)[0]
    return [h_candidates[i] for i in successful_indices]

# ===== TEST 1: Known small AP-3 progression (7, 37, 67) with difference 30 =====
print("=== TEST 1: Known small AP-3 (7, 37, 67) d=30 ===")
candidates = np.arange(1, 100, dtype=np.uint64)
matches = run_gpu_sieve(candidates, 30, 3)
print(f"AP-3 found starting at: {matches}")
print()

# ===== TEST 2: AP-5 known pattern =====
print("=== TEST 2: Scanning for AP-5 (d=30) up to 1000 ===")
candidates = np.arange(1, 1000, dtype=np.uint64)
matches = run_gpu_sieve(candidates, 30, 5)
print(f"AP-5 found starting at: {matches}")
if matches:
    first = matches[0]
    terms = [first + i*30 for i in range(5)]
    print(f"Terms: {terms}")
print()

# ===== TEST 3: AP-3 with d=6 (small step) =====
print("=== TEST 3: AP-3 (d=6) searching up to 200 ===")
candidates = np.arange(1, 200, dtype=np.uint64)
matches = run_gpu_sieve(candidates, 6, 3)
print(f"AP-3 (d=6) found starting at: {matches}")
if matches:
    for m in matches[:5]:
        terms = [m + i*6 for i in range(3)]
        print(f"  {m}: {terms}")
print()

# ===== TEST 4: Verify the original pipeline range for a small subset =====
print("=== TEST 4: Small sample around the pipeline's target range ===")
# Check a handful of numbers around 10^15 to verify the logic
candidates = np.arange(999721403904400, 999721403904420, dtype=np.uint64)
matches = run_gpu_sieve(candidates, 210, 3)
print(f"AP-3 near pipeline target: {matches}")
if matches:
    for m in matches:
        terms = [m + i*210 for i in range(3)]
        print(f"  {m}: {terms}")
print()

# ===== TEST 5: Check individual primes in the pipeline target range =====
print("=== TEST 5: Counting primes near pipeline target ===")
# Just test for is_prime on a small range near the target
simple_kernel = SourceModule("""
__device__ inline unsigned long long mul_mod(unsigned long long a, unsigned long long b, unsigned long long m) {
    unsigned long long r = 0; a %= m;
    while (b > 0) { if (b & 1) r = (r + a) % m; a = (a << 1) % m; b >>= 1; }
    return r;
}
__device__ unsigned long long pow_mod(unsigned long long base, unsigned long long exp, unsigned long long mod) {
    unsigned long long res = 1; base %= mod;
    while (exp > 0) { if (exp & 1) res = mul_mod(res, base, mod); base = mul_mod(base, base, mod); exp >>= 1; }
    return res;
}
__device__ bool is_prime(unsigned long long n) {
    if (n < 2 || n % 2 == 0) return n == 2;
    unsigned long long d = n - 1; int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    const unsigned long long witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        unsigned long long a = witnesses[i]; if (n <= a) break;
        unsigned long long x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        for (int r = 1; r < s; r++) { x = mul_mod(x, x, n); if (x == n - 1) goto next_witness; }
        return false; next_witness:;
    }
    return true;
}
__global__ void count_primes(unsigned long long* nums, int* res, int n) {
    int idx = threadIdx.x; if (idx < n) res[idx] = is_prime(nums[idx]) ? 1 : 0;
}
""")
count_fn = simple_kernel.get_function('count_primes')
pixels = np.arange(999721403904400, 999721403904500, dtype=np.uint64)
pix_res = np.zeros(len(pixels), dtype=np.int32)
d_pix = cuda.mem_alloc(pixels.nbytes)
d_pixr = cuda.mem_alloc(pix_res.nbytes)
cuda.memcpy_htod(d_pix, pixels)
cuda.memcpy_htod(d_pixr, pix_res)
count_fn(d_pix, d_pixr, np.int32(len(pixels)), block=(256,1,1), grid=(1,1))
cuda.Context.synchronize()
cuda.memcpy_dtoh(pix_res, d_pixr)

prime_indices = np.where(pix_res == 1)[0]
print(f"Found {len(prime_indices)} primes in range 999721403904400..999721403904500")
for idx in prime_indices[:10]:
    print(f"  {pixels[idx]}")
