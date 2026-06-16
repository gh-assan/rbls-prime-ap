"""
RBLS M1 Pipeline — AP-9 Search v2
==================================
Second attempt: shifted search window ~5 trillion past the original LLL target.
The first run (200 batches, 83 min) found nothing despite P(miss) ≈ 0.3%.
This run covers new ground further from the original resonance target.
"""
import numpy as np
import sympy
from sympy import Matrix
import math
import time
import sys
sys.stdout.reconfigure(line_buffering=True)
from numba import njit, prange

# =====================================================================
# 0. PRIMORIAL
# =====================================================================
def get_required_primorial(k):
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 1. NUMBA JIT ENGINE
# =====================================================================
@njit
def mod_mul(a, b, m):
    res = 0
    a = a % m
    while b > 0:
        if b % 2 == 1:
            res = (res + a) % m
        a = (a * 2) % m
        b //= 2
    return res

@njit
def pow_mod(base, exp, mod):
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = mod_mul(res, base, mod)
        base = mod_mul(base, base, mod)
        exp //= 2
    return res

@njit
def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    witnesses = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in witnesses:
        if n <= a:
            break
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for r in range(1, s):
            x = mod_mul(x, x, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

@njit(parallel=True)
def evaluate_progressions(candidates, d_step, k_len):
    num_candidates = len(candidates)
    results = np.zeros(num_candidates, dtype=np.int32)
    for idx in prange(num_candidates):
        base_a = candidates[idx]
        valid = True
        for j in range(k_len):
            if not is_prime(base_a + j * d_step):
                valid = False
                break
        if valid:
            results[idx] = 1
    return results

# =====================================================================
# 2. LLL RESONANCE
# =====================================================================
def get_resonance_parameters(k_length):
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION] ---")
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    target_ln = math.log(10**15)
    C = 10**8
    A = [int(alpha * C) for alpha in alphas]
    M = Matrix([
        [C, 0, 0, 0],
        [0, C, 0, 0],
        [0, 0, C, 0],
        [A[0], A[1], A[2], 1]
    ])
    L = M.lll()
    base_q = abs(L[0, 3])
    if base_q == 0:
        base_q = 1
    multiplier = int(target_ln * C / base_q)
    final_q = base_q * multiplier
    y = final_q / C
    a_target = int(math.exp(y))
    d_step = get_required_primorial(k_length)
    print(f"LLL complete. Resonant ln(a) = {y:.6f}")
    print(f"Target starting magnitude  = {a_target:,}")
    print(f"Primorial step size (d)    = {d_step}")
    return a_target, d_step

# =====================================================================
# 3. ESTIMATE
# =====================================================================
def estimate_probability(k, d):
    ln_n = math.log(10**15)
    singular = 1.0
    for p in sympy.primerange(2, 100_000):
        residues = len({(j * d) % p for j in range(k)})
        if residues == p:
            singular = 0.0
            break
        singular *= (1.0 - residues / p) / ((1.0 - 1.0 / p) ** k)
    p_ap = singular / (ln_n ** k) if singular else 0.0
    print(f"\n--- AP-{k} Estimate ---")
    print(f"d={d}, singular series≈{singular:.3e}")
    print(f"P(AP-{k})≈{p_ap:.2e}, expected raw candidates≈{1/p_ap:.2e}")
    print(f"  Expected batches of 10M raw: {1/p_ap/10_000_000:.1f}")
    return 1.0 / p_ap

# =====================================================================
# 4. MAIN
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("RBLS M1 Pipeline — AP-9 Search v2")
    print("Shifted window: 5 trillion past original LLL target")
    print("=" * 70)

    k_length = 9
    batch_size = 10_000_000
    max_batches = 200
    window_shift = 5_000_000_000_000  # 5 trillion offset from original starting point

    # Phase 1: original LLL resonance
    target_a_orig, d_step = get_resonance_parameters(k_length)
    expected_candidates = estimate_probability(k_length, d_step)

    # Shift the start by 5 trillion
    first_start = target_a_orig + window_shift
    if first_start % 2 == 0:
        first_start += 1

    print(f"\nOriginal LLL target:  {target_a_orig:,}")
    print(f"Window shift:         {window_shift:,} ({window_shift/1e12:.0f}T)")
    print(f"New starting point:   {first_start:,}")
    print(f"Ending point:         {first_start + batch_size * max_batches:,}")

    print(f"\n--- [PHASE 2: DISCRETE M1 CPU SIEVE] ---")
    print(f"k={k_length}, d={d_step}, batch={batch_size:,} raw/batch, max={max_batches} batches")
    print(f"Odd-only filter active")
    print(f"First batch start: {first_start:,}")

    overall_start = time.time()
    total_odd_processed = 0
    total_found = 0

    for batch_num in range(1, max_batches + 1):
        current_start = first_start + (batch_num - 1) * batch_size
        raw_candidates = np.arange(
            current_start,
            current_start + batch_size,
            dtype=np.uint64
        )
        odd_candidates = raw_candidates[raw_candidates % 2 == 1]
        num_odd = len(odd_candidates)

        batch_start = time.time()
        results_mask = evaluate_progressions(odd_candidates, d_step, k_length)
        batch_end = time.time()
        batch_elapsed = batch_end - batch_start

        found_indices = np.where(results_mask == 1)[0]
        if len(found_indices) > 0:
            for idx in found_indices:
                total_found += 1
                match = odd_candidates[idx]
                print()
                print("=" * 60)
                print(f"*** DISCOVERED AP-{k_length}! a0 = {match:,} ***")
                print("=" * 60)
                for i in range(k_length):
                    term = match + i * d_step
                    is_p = is_prime(term)
                    print(f"  Term {i}: {term}  {'PRIME' if is_p else 'COMPOSITE'}")
                print()

        total_odd_processed += num_odd

        elapsed = time.time() - overall_start
        rate = total_odd_processed / elapsed if elapsed > 0 else 0
        remaining_odd = (max_batches - batch_num) * (batch_size // 2)
        eta = remaining_odd / rate if rate > 0 else 0

        print(f"Batch {batch_num:3d}/{max_batches}: "
              f"{num_odd:>7,} odd in {batch_elapsed:>6.2f}s "
              f"| matches: {len(found_indices)}"
              f" | {rate:>8,.0f} odd/s"
              f" | ETA {eta:>6.0f}s"
              f" | searching: {current_start:,}")

        if total_found > 0:
            print(f"\nFound AP-{k_length} — ending search early.")
            break

    overall_end = time.time()
    total_elapsed = overall_end - overall_start
    total_raw = batch_size * max_batches

    print()
    print("=" * 70)
    print("--- [RESULTS] ---")
    print(f"Searched {total_raw:,} raw candidates ({total_odd_processed:,} odd)")
    print(f"Window: {first_start:,} to {first_start + batch_size * max_batches:,}")
    print(f"Total time: {total_elapsed:.2f}s ({total_elapsed/60:.2f} min)")
    print(f"Average throughput: {total_odd_processed/total_elapsed:,.0f} odd/s")
    print(f"AP-{k_length} progressions found: {total_found}")
    print("=" * 70)
