"""Exact, bounded-memory prime AP search on candidate starts (not term windows)."""
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from math import exp, log, log1p, prod
from operator import index
from time import perf_counter

import numpy as np
from sympy import primerange

UINT64_MAX = (1 << 64) - 1
WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def integer(value):
    """Reject floats instead of silently rounding search bounds."""
    return int(index(value))


def get_required_primorial(k):
    k = integer(k)
    if k < 2:
        raise ValueError("k must be at least 2")
    return prod(primerange(2, k + 1))


def is_prime(n):
    """Deterministic Miller-Rabin below 2**64; Python integers never overflow."""
    n = integer(n)
    if n < 2:
        return False
    if n > UINT64_MAX:
        raise ValueError("deterministic verifier requires n < 2**64")
    for p in WITNESSES:
        if n % p == 0:
            return n == p
    odd = n - 1
    shifts = (odd & -odd).bit_length() - 1
    odd >>= shifts
    for base in WITNESSES:
        value = pow(base, odd, n)
        if value in (1, n - 1):
            continue
        for _ in range(shifts - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


@lru_cache(maxsize=128)
def sieve_plan(k, d, bound):
    """Forbidden start residues: a == -j*d (mod p)."""
    return tuple((int(p), tuple(sorted({(-j * d) % p for j in range(min(k, p))})))
                 for p in primerange(2, bound + 1))


@dataclass(frozen=True)
class Wheel:
    modulus: int
    residues: tuple
    primes: tuple


@lru_cache(maxsize=128)
def build_wheel(k, d, prime_bound=43, max_classes=4096):
    """CRT construction with a strict limit on stored residue classes."""
    modulus, residues, used = 1, (0,), []
    for p, forbidden in sieve_plan(k, d, prime_bound):
        if len(forbidden) == p:
            return Wheel(p, (), (p,))
        # Primes dividing d have only one forbidden residue; use strided sieving.
        if d % p == 0:
            continue
        allowed = tuple(r for r in range(p) if r not in forbidden)
        if len(residues) * len(allowed) > max_classes:
            continue
        inverse = pow(modulus, -1, p)
        residues = tuple(sorted(r + modulus * (((s - r) * inverse) % p)
                                for r in residues for s in allowed))
        modulus *= p
        used.append(p)
    return Wheel(modulus, residues, tuple(used))


def wheel_segment(start, stop, wheel):
    """Sorted candidates in [start, stop), with no array of size wheel.modulus."""
    if not wheel.residues:
        return np.empty(0, dtype=np.uint64)
    # The number of blocks can be large when there is no useful wheel. Use a
    # direct arange then: this path is bounded by the numeric segment width.
    if wheel.modulus == 1:
        return np.arange(stop - start, dtype=np.uint64) + np.uint64(start)
    parts = []
    for r in wheel.residues:
        first = start + (r - start) % wheel.modulus
        if first < stop:
            count = (stop - 1 - first) // wheel.modulus + 1
            parts.append(np.arange(count, dtype=np.uint64) * np.uint64(wheel.modulus)
                         + np.uint64(first))
    if not parts:
        return np.empty(0, dtype=np.uint64)
    return np.sort(np.concatenate(parts))


def sieve_candidates(candidates, k, d, bound, excluded=()):
    """Filter starts whose terms exceed bound; no false rejection of small primes."""
    alive = np.ones(len(candidates), dtype=bool)
    for p, forbidden in sieve_plan(k, d, bound):
        if p in excluded:
            continue
        residues = candidates % np.uint64(p)
        if d % p == 0:
            alive &= residues != 0
        else:
            # k < p for admissible tuples: roots occupy a cyclic interval after
            # multiplying by d^-1. This uses one vector comparison per prime.
            scaled = (residues * np.uint64(pow(d, -1, p))) % np.uint64(p)
            alive &= (scaled > 0) & (scaled <= p - k)
        if not alive.any():
            break
    return candidates[alive]


@dataclass
class SearchResult:
    k: int
    d: int
    start: int
    stop: int
    sieve_bound: int
    segment_size: int
    wheel_modulus: int
    wheel_classes: int
    wheel_primes: tuple
    raw_starts: int = 0
    wheel_candidates: int = 0
    sieve_survivors: int = 0
    primality_tests: int = 0
    matches: list = field(default_factory=list)
    seconds: float = 0.0

    def to_dict(self):
        return asdict(self)


def search(start, stop, k, d=None, *, sieve_bound=1000, segment_size=1_000_000,
           wheel_bound=43, max_wheel_classes=4096):
    """Find ALL AP-k starts in [start, stop). Terms may extend beyond stop.

    Completeness is for the specified positive difference d and uint64 domain.
    No early stop or success-dependent accounting is used.
    """
    start, stop, k = map(integer, (start, stop, k))
    d = get_required_primorial(k) if d is None else integer(d)
    sieve_bound, segment_size, wheel_bound, max_wheel_classes = map(
        integer, (sieve_bound, segment_size, wheel_bound, max_wheel_classes))
    if k < 2 or d < 1 or start < 2 or stop <= start:
        raise ValueError("require k >= 2, d > 0, and 2 <= start < stop")
    if segment_size < 1 or not 2 <= sieve_bound <= 1_000_000:
        raise ValueError("require segment_size > 0 and 2 <= sieve_bound <= 1000000")
    if not 2 <= wheel_bound <= 97 or max_wheel_classes < 1:
        raise ValueError("require 2 <= wheel_bound <= 97 and max_wheel_classes > 0")
    if stop - 1 + (k - 1) * d > UINT64_MAX:
        raise ValueError("last progression term must be below 2**64")
    wheel = build_wheel(k, d, min(wheel_bound, sieve_bound), max_wheel_classes)
    result = SearchResult(k, d, start, stop, sieve_bound, segment_size,
                          wheel.modulus, len(wheel.residues), wheel.primes)
    began = perf_counter()

    def verify(a):
        for j in range(k):
            result.primality_tests += 1
            if not is_prime(a + j * d):
                return
        result.matches.append(a)

    # Divisibility by p is harmless when the term equals p. Handle the small
    # prefix directly; in the rest every term exceeds every sieving prime.
    prefix_stop = min(stop, sieve_bound + 1)
    for a in range(start, prefix_stop):
        result.raw_starts += 1
        result.wheel_candidates += 1
        result.sieve_survivors += 1
        verify(a)
    for lo in range(max(start, prefix_stop), stop, segment_size):
        hi = min(stop, lo + segment_size)
        candidates = wheel_segment(lo, hi, wheel)
        result.raw_starts += hi - lo
        result.wheel_candidates += len(candidates)
        survivors = sieve_candidates(candidates, k, d, sieve_bound, wheel.primes)
        result.sieve_survivors += len(survivors)
        for a in survivors:
            verify(int(a))
    result.seconds = perf_counter() - began
    return result


def singular_series(k, d, prime_bound=100_000):
    """Partial product through prime_bound; a heuristic, not an error bound."""
    k, d, prime_bound = map(integer, (k, d, prime_bound))
    if k < 2 or d < 1 or prime_bound < k:
        raise ValueError("require k >= 2, d > 0, and prime_bound >= k")
    total = 0.0
    for p in primerange(2, prime_bound + 1):
        occupied = 1 if d % p == 0 else min(k, p)
        if occupied == p:
            return 0.0
        total += log1p(-occupied / p) - k * log1p(-1 / p)
    return exp(total)


def expected_probability(k, d, start, prime_bound=100_000):
    """Use all term logarithms, important when (k-1)*d is comparable to start."""
    if start < 2:
        raise ValueError("start must be >= 2")
    return singular_series(k, d, prime_bound) / prod(log(start + j * d) for j in range(k))


def survivor_density(k, d, prime_bound=1000):
    """Exact periodic survival fraction, evaluated in floating point."""
    total = 0.0
    for p in primerange(2, prime_bound + 1):
        occupied = 1 if d % p == 0 else min(k, p)
        if occupied == p:
            return 0.0
        total += log1p(-occupied / p)
    return exp(total)
