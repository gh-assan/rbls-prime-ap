import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

# Simple test kernel
mod = SourceModule("""
__device__ inline unsigned long long mul_mod(unsigned long long a, unsigned long long b, unsigned long long m) {
    unsigned long long r = 0;
    a %= m;
    while (b > 0) {
        if (b & 1) { r = (r + a) % m; }
        a = (a << 1) % m;
        b >>= 1;
    }
    return r;
}

__device__ unsigned long long pow_mod(unsigned long long base, unsigned long long exp, unsigned long long mod) {
    unsigned long long res = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp & 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp >>= 1;
    }
    return res;
}

__device__ bool is_prime(unsigned long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    unsigned long long d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    const unsigned long long witnesses[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        unsigned long long a = witnesses[i];
        if (n <= a) break;
        unsigned long long x = pow_mod(a, d, n);
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

__global__ void test_primes(unsigned long long* nums, int* results, int n) {
    int idx = threadIdx.x;
    if (idx < n) results[idx] = is_prime(nums[idx]) ? 1 : 0;
}
""")

test_fn = mod.get_function('test_primes')

# Test some known primes and composites
test_nums = np.array([2, 3, 4, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 29, 31, 97, 100, 101, 1009, 1000000007, 999999999989], dtype=np.uint64)
results = np.zeros(len(test_nums), dtype=np.int32)

d_nums = cuda.mem_alloc(test_nums.nbytes)
d_res = cuda.mem_alloc(results.nbytes)
cuda.memcpy_htod(d_nums, test_nums)
cuda.memcpy_htod(d_res, results)

test_fn(d_nums, d_res, np.int32(len(test_nums)), block=(256,1,1), grid=(1,1))
cuda.Context.synchronize()
cuda.memcpy_dtoh(results, d_res)

print('Number -> IsPrime?')
for i in range(len(test_nums)):
    status = "PRIME" if results[i] else "composite"
    print(f'{test_nums[i]:15d} -> {status}')
