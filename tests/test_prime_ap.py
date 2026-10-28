import random

import numpy as np
import pytest
from sympy import isprime

from prime_ap import (UINT64_MAX, build_wheel, expected_probability,
                      get_required_primorial, is_prime, search, singular_series)


@pytest.mark.parametrize('k,d', [(7, 210), (9, 210), (28, 223092870)])
def test_primorial(k, d):
    assert get_required_primorial(k) == d


def test_primality_against_independent_oracle():
    rng = random.Random(20261028)
    samples = list(range(2000)) + [rng.randrange(2**64) for _ in range(1000)]
    samples += [341550071728321, 3825123056546413051, 2**63 - 25, 2**64 - 59, 2**64 - 1]
    for n in samples:
        assert is_prime(n) == bool(isprime(n)), n
    with pytest.raises(ValueError):
        is_prime(2**64)


@pytest.mark.parametrize('k,d', [(2, 1), (3, 2), (3, 6), (5, 30), (7, 210)])
@pytest.mark.parametrize('segment_size', [1, 37, 1000])
def test_search_exhaustive_including_small_prime_exceptions(k, d, segment_size):
    result = search(2, 1600, k, d, sieve_bound=43, segment_size=segment_size)
    expected = [a for a in range(2, 1600) if all(isprime(a + j*d) for j in range(k))]
    assert result.matches == expected
    assert result.raw_starts == 1598


@pytest.mark.parametrize('k,start', [(7, 999721467601817), (8, 999721631514707)])
def test_historical_progressions(k, start):
    result = search(start - 51, start + 52, k, 210, segment_size=17)
    assert start in result.matches
    assert result.matches == [a for a in range(start-51, start+52)
                              if all(isprime(a + j*210) for j in range(k))]


def test_crt_classes_match_exhaustive_residues():
    wheel = build_wheel(9, 210, 13)
    expected = tuple(a for a in range(wheel.modulus)
                     if all((a + j*210) % p for p in wheel.primes for j in range(9)))
    assert wheel.residues == expected
    assert len(wheel.residues) == 8  # (11-9)*(13-9)


def test_span_larger_than_start_interval_is_supported():
    a, d = 224584605939537911, 81292139 * 223092870
    result = search(a-10, a+11, 27, d, segment_size=7)
    assert result.matches == [a]


def test_full_uint64_boundary_and_range_validation():
    result = search(UINT64_MAX-120, UINT64_MAX-1, 2, 1, segment_size=13)
    assert result.matches == []
    with pytest.raises(ValueError, match='last progression'):
        search(UINT64_MAX-10, UINT64_MAX, 3, 6)
    with pytest.raises(TypeError):
        search(1e15, 10**15+10, 3)
    for options in [dict(segment_size=0), dict(sieve_bound=1), dict(wheel_bound=100)]:
        with pytest.raises(ValueError):
            search(2, 100, 3, **options)


def test_singular_series_obstruction_and_difference_gain():
    assert singular_series(28, 9699690) == 0
    # Adding p=11 to d for k=9 multiplies the local factor by (p-1)/(p-k).
    assert singular_series(9, 2310) / singular_series(9, 210) == pytest.approx(5)
    k, d, a = 9, 223092870, 10**9
    assert expected_probability(k, d, a) < singular_series(k, d) / np.log(a)**k


def test_empty_wheel_is_a_completed_negative_search():
    result = search(100, 900, 28, 9699690, sieve_bound=43)
    assert result.matches == []
    assert result.sieve_survivors == 0
    assert result.raw_starts == 800


def test_density_gain_cancels_after_sieving():
    from prime_ap import survivor_density
    d=223092870
    a=singular_series(28,d)/survivor_density(28,d)
    b=singular_series(28,d*29*31)/survivor_density(28,d*29*31)
    assert a == pytest.approx(b)
    assert singular_series(28,d*29*31)/singular_series(28,d) == pytest.approx(280)


def test_legacy_ap28_scanner_respects_difference_bounds():
    from rbls_gpu_pipeline_ap28 import scan_ap_from_primes
    primes=[n for n in range(2,1000) if isprime(n)]
    matches=scan_ap_from_primes(primes,3,12,18,lambda message: None)
    assert matches
    assert all(12 <= d <= 18 for a,d in matches)
    assert scan_ap_from_primes([],3,12,18,lambda message: None) == []
