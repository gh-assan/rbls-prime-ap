import random

import numpy as np
import pytest
from sympy import isprime

pytest.importorskip('numba')
from rbls_numba import evaluate_progressions, is_prime, mod_mul


def test_modular_multiplication_near_unsigned_limit():
    rng = random.Random(287)
    samples = [(2**64-60, 2**64-60, 2**64-59), (2**63-1, 2**63-1, 2**64-59)]
    samples += [(rng.randrange(2**64), rng.randrange(2**64), rng.randrange(1, 2**64))
                for _ in range(200)]
    for a, b, m in samples:
        assert int(mod_mul(np.uint64(a), np.uint64(b), np.uint64(m))) == a*b % m


def test_numba_primality_uses_integer_arithmetic():
    rng = random.Random(20261028)
    values = [0, 1, 2, 3, 37, 41, 2**63-25, 2**64-59, 2**64-1,
              341550071728321, 3825123056546413051]
    values += [rng.randrange(2**64) for _ in range(200)]
    for value in values:
        assert bool(is_prime(np.uint64(value))) == bool(isprime(value)), value


def test_numba_terms_above_float_exactness_limit():
    a, d = 224584605939537911, 81292139 * 223092870
    values = np.array([a-2, a, a+2], dtype=np.uint64)
    assert evaluate_progressions(values, d, 27).tolist() == [0, 1, 0]
    with pytest.raises(ValueError):
        evaluate_progressions(np.array([2**64-1], dtype=np.uint64), 1, 2)
