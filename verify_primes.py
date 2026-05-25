"""
Independent CPU-side verification of the AP-7 progression found by the GPU.
Uses Python's built-in arbitrary precision integers and pow() with 3-arg mod.
"""
import math
import sys

# The progression found
start = 999721467601817
d = 210
k = 7

terms = [start + i * d for i in range(k)]

print("=" * 60)
print("VERIFYING AP-7 PROGRESSION FOUND BY GPU")
print("=" * 60)
print(f"Common difference (d): {d}")
print()

# ===== DETERMINISTIC MILLER-RABIN (CPU, independent implementation) =====

def is_prime_mr(n):
    """Deterministic Miller-Rabin for 64-bit integers."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # Deterministic witnesses for n < 2^64
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

# ===== TRIAL DIVISION BY SMALL PRIMES (quick sanity check) =====

def trial_division(n, limit=1000000):
    """Check divisibility by small primes up to limit."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Generate small primes up to limit using simple sieve
    sieve_limit = min(limit, int(math.isqrt(n)) + 1)
    
    # Check 2 separately
    if n % 2 == 0:
        return False
    
    # Check odd numbers up to sieve_limit
    d = 3
    while d <= sieve_limit:
        if n % d == 0:
            return False
        d += 2
        # Quick check: if d*d > n, no need to continue
        if d * d > n:
            break
    return True  # Passed trial division

# ===== VERIFY =====

all_prime = True
print(f"{'Term':<8} {'Number':<22} {'Trial Div':<12} {'Miller-Rabin':<12}")
print("-" * 60)

for i, term in enumerate(terms):
    # Quick trial division first
    td_pass = trial_division(term, limit=100000)
    
    # Full Miller-Rabin
    mr_pass = is_prime_mr(term)
    
    status_td = "PASS" if td_pass else "FAIL"
    status_mr = "PRIME" if mr_pass else "COMPOSITE"
    
    print(f"Index {i:<2} {term:<22} {status_td:<12} {status_mr:<12}")
    
    if not mr_pass:
        all_prime = False

print()
print("=" * 60)
if all_prime:
    print("VERIFICATION SUCCESSFUL -- All 7 terms are PRIME!")
else:
    print("VERIFICATION FAILED -- Some terms are composite!")
print("=" * 60)
print()

# ===== Also verify the difference between consecutive terms =====
print("Verifying arithmetic progression property:")
for i in range(k - 1):
    diff = terms[i + 1] - terms[i]
    print(f"  Term {i+1} - Term {i} = {diff} {'OK' if diff == d else 'MISMATCH'}")
