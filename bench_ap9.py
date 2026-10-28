"""Benchmark the full AP-9 kernel."""
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import math
import time

cuda_source = """
typedef unsigned long long uint64;

__device__ inline uint64 mul_mod(uint64 a, uint64 b, uint64 m) {
    uint64 r = 0;
    a %= m;
    while (b > 0) {
        if (b & 1) { r = (r >= m - a ? r - (m - a) : r + a); }
        a = (a >= m - a ? a - (m - a) : a + a);
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

print("Compiling AP-9 kernel...")
mod = SourceModule(cuda_source)
fn = mod.get_function("evaluate_progressions")

# Test with small batch first
batch_size = 100_000
d_step = 210
k_len = 9
base = 999721400000000

candidates = np.arange(base, base + batch_size, dtype=np.uint64)
results = np.zeros(batch_size, dtype=np.int32)

d_candidates = cuda.mem_alloc(candidates.nbytes)
d_results = cuda.mem_alloc(results.nbytes)
cuda.memcpy_htod(d_candidates, candidates)
cuda.memcpy_htod(d_results, results)

threads = 256
blocks = (batch_size + threads - 1) // threads

t0 = time.time()
fn(d_candidates, np.uint64(d_step), np.int32(k_len), d_results, np.int32(batch_size),
   block=(threads,1,1), grid=(blocks,1))
cuda.Context.synchronize()
t1 = time.time()

cuda.memcpy_dtoh(results, d_results)
found = int(np.sum(results))

print(f'Batch of {batch_size:,} AP-9 candidates: {t1-t0:.3f}s')
print(f'Found: {found}')
print(f'Throughput: {batch_size/(t1-t0):,.0f} candidates/sec')
print(f'Estimated time for 10M: {10_000_000 / (batch_size/(t1-t0)):.1f}s')
