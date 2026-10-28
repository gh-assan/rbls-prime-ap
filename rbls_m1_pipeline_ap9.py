"""
RBLS M1 Pipeline — AP-9 Search
================================
Searches for 9-term arithmetic progressions of primes near the LLL-resonant target
using Numba JIT + parallel CPU on Apple Silicon.

Key optimizations ported from GPU AP-8 pipeline:
  - Odd-only filtering (d=210 even => even a0 makes all terms even => skip 50%)
  - Multi-batch processing with per-batch progress reporting
  - Probability estimation at startup

For k=9: primorial of primes <= 9 = 2*3*5*7 => d=210.
The startup estimate uses a truncated Hardy-Littlewood singular series.
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
# 0. PRIMORIAL CALCULATION
# =====================================================================

def get_required_primorial(k):
    """Product of all primes <= k."""
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 1. NUMBA JIT ENGINE (Apple Silicon)
# =====================================================================

from rbls_numba import mod_mul, pow_mod, is_prime, evaluate_progressions

# =====================================================================
# 2. ANALYTIC PHASE (SymPy LLL Lattice Reduction)
# =====================================================================

def get_resonance_parameters(k_length):
    import warnings
    warnings.warn("Legacy LLL scaling does not preserve phase alignment; "
                  "use search_prime_ap.py for the modular search.", RuntimeWarning)
    """LLL lattice reduction targeting ~10^15 via Riemann zeta zeros."""
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

    print(f"LLL complete. Historical target ln(a) = {y:.6f}")
    print(f"Target starting magnitude  = {a_target:,}")
    print(f"Primorial step size (d)    = {d_step}")
    print(f"  d = product of primes <= {k_length} = {d_step}")
    print(f"  d parity: {'even' if d_step % 2 == 0 else 'odd'} "
          f"(even => odd-only filter applicable, cuts search space in half)")

    return a_target, d_step

# =====================================================================
# 3. PROBABILITY ESTIMATE
# =====================================================================

def estimate_probability(k, d):
    """
    Heuristic estimate of expected candidates needed for an AP-k with step d
    near 10^15, using a truncated Hardy-Littlewood singular series.
    """
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
# 4. MAIN PIPELINE
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RBLS M1 Pipeline — AP-9 Search")
    print("M1 Native (Numba JIT + parallel CPU)")
    print("=" * 70)

    k_length = 9
    batch_size = 10_000_000   # Raw candidates per batch (before odd filter)
    max_batches = 200          # 200 batches = 2B raw candidates (~1B odd)

    # ---- Phase 1: Analytic LLL resonance targeting ----
    target_a, d_step = get_resonance_parameters(k_length)

    # ---- Phase 1b: Probability estimate ----
    expected_candidates = estimate_probability(k_length, d_step)
    expected_batches_10m = expected_candidates / 10_000_000
    expected_batches_5m = expected_candidates / 5_000_000
    print(f"  (at 5M odd/batch: {expected_batches_5m:.1f} batches)")

    first_start = target_a
    if first_start % 2 == 0:
        first_start += 1
        print(f"\nAdjusted start to odd: {first_start:,}")

    print(f"\n--- [PHASE 2: DISCRETE M1 CPU SIEVE] ---")
    print(f"k={k_length}, d={d_step}, batch={batch_size:,} raw/batch, max={max_batches} batches")
    print(f"Odd-only filter active (every even a0 skipped, ~5M odd candidates/batch)")
    print(f"First batch start: {first_start:,}")
    print(f"LLVM JIT compilation occurs on first batch (~1-2s overhead)")
    if max_batches * 5_000_000 < expected_candidates:
        print(f"*** WARNING: {max_batches} batches may not be enough to find AP-{k_length} ***")
        print(f"    Expected ~{expected_batches_5m:.0f} batches at 5M odd/batch")
        print(f"    Consider increasing max_batches after this run completes.")

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
              f" | ETA {eta:>6.0f}s")

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
    print(f"Total time: {total_elapsed:.2f}s ({total_elapsed/60:.2f} min)")
    print(f"Average throughput: {total_odd_processed/total_elapsed:,.0f} odd/s")
    print(f"AP-{k_length} progressions found: {total_found}")
    print("=" * 70)
