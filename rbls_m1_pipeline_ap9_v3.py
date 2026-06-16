"""
RBLS M1 Pipeline — AP-9 Search v3
==================================
Third attempt: Multi-target LLL (top 3 lattice vectors sorted by quality).
The GPU AP-8 pipeline used this strategy and successfully found AP-8.
The M1 pipeline was only using the 1st LLL vector; this explores all 3.
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
# 2. MULTI-TARGET LLL RESONANCE
# =====================================================================
def get_multiple_resonance_targets(k_length):
    """
    Extract top 3 LLL vectors as independent starting targets.
    Sorts by resonance quality (phase alignment with Riemann zeros).
    """
    print("--- [PHASE 1: MULTI-TARGET LLL REDUCTION] ---")
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
    d_step = get_required_primorial(k_length)

    targets = []
    for row_idx in range(min(3, L.rows)):
        base_q = abs(L[row_idx, 3])
        if base_q == 0:
            base_q = 1
        multiplier = int(target_ln * C / base_q)
        final_q = base_q * multiplier
        y = final_q / C
        a_target = int(math.exp(y))

        # Compute quality: how close are phases to integers?
        quality_scores = []
        for i, alpha in enumerate(alphas):
            phase = (y * alpha) % 1.0
            quality_scores.append(min(phase, 1.0 - phase))  # distance to nearest integer

        avg_quality = sum(quality_scores) / len(quality_scores)

        # Ensure odd start
        if a_target % 2 == 0:
            a_target += 1

        targets.append((a_target, d_step, y, avg_quality))
        print(f"  Target #{row_idx+1}: a={a_target:,}, ln(a)={y:.6f}, quality={avg_quality:.6f}")

    # Sort by quality (lower = better alignment)
    targets.sort(key=lambda x: x[3])

    best = targets[0]
    worst = targets[-1]
    print(f"\n  Best quality:  a={best[0]:,} (q={best[3]:.6f})")
    print(f"  Worst quality: a={worst[0]:,} (q={worst[3]:.6f})")

    return targets, d_step

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
# 4. SEARCH ONE TARGET
# =====================================================================
def search_target(target_a, d_step, k_length, batch_size, max_batches, target_label):
    """Search one LLL target. Returns (found: bool, a0: int or None)"""
    first_start = target_a
    if first_start % 2 == 0:
        first_start += 1

    print(f"\n--- [SEARCHING TARGET {target_label}] ---")
    print(f"Starting at: {first_start:,}")
    print(f"Range: {first_start:,} to {first_start + batch_size * max_batches:,}")
    print(f"Batches: {max_batches}, batch size: {batch_size:,} raw ({batch_size//2:,} odd)")

    total_odd_processed = 0
    total_found = 0
    target_start_time = time.time()

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
            return True, match

        total_odd_processed += num_odd

        elapsed = time.time() - target_start_time
        rate = total_odd_processed / elapsed if elapsed > 0 else 0

        print(f"  {target_label} Batch {batch_num:3d}/{max_batches}: "
              f"{num_odd:>7,} odd in {batch_elapsed:>6.2f}s | 0 matches"
              f" | {rate:>8,.0f} odd/s"
              f" | searching: {current_start:,}")

    return False, None

# =====================================================================
# 5. MAIN
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("RBLS M1 Pipeline — AP-9 Search v3")
    print("Multi-target LLL (top 3 vectors, quality-sorted)")
    print("=" * 70)

    k_length = 9
    batch_size = 10_000_000
    batches_per_target = 100   # 100 batches per target = ~500M raw per target
    d_step = 210

    # Phase 1: Multi-target LLL
    targets, d_step = get_multiple_resonance_targets(k_length)
    expected_candidates = estimate_probability(k_length, d_step)

    print(f"\nTotal search plan: {len(targets)} targets × {batches_per_target} batches")
    print(f"Total raw candidates: {len(targets) * batches_per_target * batch_size:,}")
    print(f"Total odd candidates: ~{len(targets) * batches_per_target * batch_size // 2:,}")

    overall_start = time.time()

    # Phase 2: Search each target in quality order (best first)
    found = False
    for target_idx, (target_a, _, _, quality) in enumerate(targets):
        label = f"T{target_idx+1} (q={quality:.4f})"
        target_found, match = search_target(
            target_a, d_step, k_length,
            batch_size, batches_per_target, label
        )
        if target_found:
            found = True
            break

        elapsed = time.time() - overall_start
        remaining_targets = len(targets) - (target_idx + 1)
        print(f"\n  Target {target_idx+1} complete. "
              f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min). "
              f"Remaining targets: {remaining_targets}")

    overall_end = time.time()
    total_elapsed = overall_end - overall_start
    total_raw = len(targets) * batches_per_target * batch_size
    total_odd_est = total_raw // 2

    print()
    print("=" * 70)
    print("--- [FINAL RESULTS] ---")
    print(f"Targets searched:     {len(targets)}")
    print(f"Batches per target:   {batches_per_target}")
    print(f"Total raw candidates: {total_raw:,}")
    print(f"Total odd candidates: ~{total_odd_est:,}")
    print(f"Total time:           {total_elapsed:.2f}s ({total_elapsed/60:.2f} min)")
    print(f"AP-{k_length} found:       {'YES' if found else 'NO'}")
    if found:
        print(f"  a0 = {match:,}")
        for i in range(k_length):
            term = match + i * d_step
            print(f"  Term {i}: {term}")
    print("=" * 70)
