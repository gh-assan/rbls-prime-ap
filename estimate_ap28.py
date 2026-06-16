"""
Estimate the feasibility of finding an AP-28 (28-term arithmetic progression of
primes) near 10^15.
"""
import math
import sympy


def get_required_primorial(k):
    """Calculates the product of all primes <= k."""
    primorial = 1
    for p in sympy.primerange(2, k + 1):
        primorial *= p
    return primorial


def singular_series(k, d, prime_bound=100_000):
    """Truncated Hardy-Littlewood singular series for {0, d, ..., (k-1)d}."""
    series = 1.0
    for p in sympy.primerange(2, prime_bound):
        residues = len({(j * d) % p for j in range(k)})
        if residues == p:
            return 0.0
        series *= (1.0 - residues / p) / ((1.0 - 1.0 / p) ** k)
    return series


k = 28
d = get_required_primorial(k)
x = 10**15
ln_x = math.log(x)

print(f"Step size d = {d:,}")
print(f"Spread (k-1)d = {(k - 1) * d:,}")
print(f"Prime probability near 10^15: {1 / ln_x:.6f} ({ln_x:.1f} numbers per prime)")
print()

p_naive = (1.0 / ln_x) ** k
print(f"Naive independent probability: {p_naive:.2e}")
print(f"Naive expected raw starts: {1 / p_naive:.2e}")
print()

series = singular_series(k, d)
p_hl = series / (ln_x ** k) if series else 0.0
print(f"Truncated singular series: {series:.3e}")
print(f"Hardy-Littlewood-style probability per raw start: {p_hl:.2e}")
print(f"Expected raw starts: {1 / p_hl:.2e}")
print()

time_per_10m = 18  # seconds, rough historical GPU timing
batches_needed = (1 / p_hl) / 10_000_000
total_seconds = batches_needed * time_per_10m
print("--- Time Estimation ---")
print(f"Batches of 10M needed: {batches_needed:.2e}")
print(f"Total GPU time: {total_seconds:.2e} seconds")
print(f"  = {total_seconds / 3600:.2e} hours")
print(f"  = {total_seconds / 86400:.2e} days")
print(f"  = {total_seconds / (86400 * 365):.2e} years")
