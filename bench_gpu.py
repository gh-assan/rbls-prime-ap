"""Quick GPU benchmark: measure is_prime throughput."""
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import math
import time

src = """
__device__ inline unsigned long long mul_mod(unsigned long long a, unsigned long long b, unsigned long long m) {
    unsigned long long r = 0; a %= m;
    while (b > 0) { if (b & 1) r = (r + a) % m; a = (a << 1) % m; b >>= 1; } return r;
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
        for (int r = 1; r < s; r++) { x = mul_mod(x, x, n); if (x == n - 1) goto next; }
        return false; next:;
    }
    return true;
}
__global__ void bench(unsigned long long* nums, int* res, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n) return;
    res[idx] = is_prime(nums[idx]) ? 1 : 0;
}
"""

print("Compiling benchmark kernel...")
mod = SourceModule(src)
fn = mod.get_function('bench')

n = 1_000_000
base = 999721400000000
nums = np.arange(base, base + n, dtype=np.uint64)
res = np.zeros(n, dtype=np.int32)
d_nums = cuda.mem_alloc(nums.nbytes)
d_res = cuda.mem_alloc(res.nbytes)
cuda.memcpy_htod(d_nums, nums)
cuda.memcpy_htod(d_res, res)

t0 = time.time()
fn(d_nums, d_res, np.int32(n), block=(256,1,1), grid=((n+255)//256,1))
cuda.Context.synchronize()
t1 = time.time()

cuda.memcpy_dtoh(res, d_res)
primes_found = int(np.sum(res))
print(f'1M is_prime checks: {t1-t0:.3f}s')
print(f'Primes found: {primes_found}')
print(f'Throughput: {n/(t1-t0):,.0f} numbers/sec')
