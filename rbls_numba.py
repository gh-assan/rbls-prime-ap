"""Shared Numba backend. Explicit unsigned types avoid float64 promotion."""
import numpy as np
from numba import boolean, njit, prange, uint64

from prime_ap import UINT64_MAX, WITNESSES, integer


@njit(uint64(uint64, uint64, uint64))
def mod_mul(a, b, m):
    # Every addition is performed only when its mathematical result fits.
    result = np.uint64(0)
    a %= m
    while b > 0:
        if b & np.uint64(1):
            if result >= m - a:
                result -= m - a
            else:
                result += a
        if a >= m - a:
            a -= m - a
        else:
            a += a
        b >>= np.uint64(1)
    return result


@njit(uint64(uint64, uint64, uint64))
def pow_mod(base, exponent, modulus):
    result = np.uint64(1)
    base %= modulus
    while exponent > 0:
        if exponent & np.uint64(1):
            result = mod_mul(result, base, modulus)
        base = mod_mul(base, base, modulus)
        exponent >>= np.uint64(1)
    return result


@njit(boolean(uint64))
def is_prime(n):
    if n < np.uint64(2):
        return False
    for witness in WITNESSES:
        p = np.uint64(witness)
        if n % p == 0:
            return n == p
    odd = n - np.uint64(1)
    shifts = 0
    while odd & np.uint64(1) == 0:
        odd >>= np.uint64(1)
        shifts += 1
    for witness in WITNESSES:
        value = pow_mod(np.uint64(witness), odd, n)
        if value == np.uint64(1) or value == n - np.uint64(1):
            continue
        for _ in range(shifts - 1):
            value = mod_mul(value, value, n)
            if value == n - np.uint64(1):
                break
        else:
            return False
    return True


@njit(parallel=True)
def _evaluate_progressions(candidates, d_step, k_len):
    results = np.zeros(len(candidates), dtype=np.int32)
    for idx in prange(len(candidates)):
        valid = True
        for j in range(k_len):
            if not is_prime(candidates[idx] + np.uint64(j) * d_step):
                valid = False
                break
        if valid:
            results[idx] = 1
    return results


def evaluate_progressions(candidates, d_step, k_len):
    d_step, k_len = integer(d_step), integer(k_len)
    if d_step < 1 or k_len < 2:
        raise ValueError('require d > 0 and k >= 2')
    values = np.asarray(candidates)
    if values.ndim != 1 or values.dtype.kind not in 'iu':
        raise ValueError('candidates must be a one-dimensional integer array')
    if len(values) and (int(values.min()) < 0 or
                       int(values.max()) + (k_len - 1) * d_step > UINT64_MAX):
        raise ValueError('progression terms must fit uint64')
    if d_step > UINT64_MAX or k_len > np.iinfo(np.int64).max:
        raise ValueError('difference or length exceeds the backend integer range')
    return _evaluate_progressions(values.astype(np.uint64), np.uint64(d_step), np.int64(k_len))
