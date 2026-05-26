"""
Estimate the feasibility of finding AP-28 (28-term arithmetic progression of primes).
"""
import math
import sympy

def get_required_primorial(k):
    """Calculates the product of all primes <= k."""
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial
k = 28      # progression length
d = get_required_primorial(k)  # step size (primorial of all primes < k)

print(f"Step size d = P_{{{k}}} = {d}")
print()

# Probability a random number near 10^15 is prime
ln_n = math.log(10**15)
p_prime = 1.0 / ln_n
print(f"Prime probability near 10^15: {p_prime:.6f} ({1/p_prime:.1f} numbers on average per prime)")

# Probability an AP-28 chain (28 numbers, each d apart) are ALL prime
# Since they're not independent (same residue classes modulo small primes),
# this is a rough upper bound
p_ap28 = p_prime ** k
print(f"Probability of AP-28 (naive): {p_ap28:.2e}")
print(f"Expected candidates to test: {1/p_ap28:.2e}")
print()

# More realistic: with d = primorial P_{k}, all terms share same mod-d residue.
# Only residues coprime to d can work: phi(d) residues out of d.
phi_d = d
for p in sympy.primerange(2, k):
    phi_d = phi_d * (p - 1) // p
print(f"phi({d}) = {phi_d}")
filter_factor = phi_d / d
print(f"Fraction of residues coprime to {d}: {filter_factor:.4f}")
# For the surviving residues, the probability each term is prime is higher
p_cond = p_prime / filter_factor
print(f"Conditional prime prob (coprime to {d}): {p_cond:.6f}")
p_ap28_refined = p_cond ** k
print(f"AP-28 prob (conditioned on coprime residue): {p_ap28_refined:.2e}")
print(f"Expected candidates to test: {1/p_ap28_refined:.2e}")
print()

# Time estimation based on our GPU (18 sec for 10M candidates)
time_per_10m = 18  # seconds
candidates_needed = 1 / p_ap28_refined
batches_needed = candidates_needed / 10_000_000
total_seconds = batches_needed * time_per_10m
print(f"--- Time Estimation ---")
print(f"Batches of 10M needed: {batches_needed:.2e}")
print(f"Total GPU time: {total_seconds:.2e} seconds")
print(f"  = {total_seconds/3600:.2e} hours")
print(f"  = {total_seconds/86400:.2e} days")
print(f"  = {total_seconds/(86400*365):.2e} years")

