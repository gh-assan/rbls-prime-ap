"""
RBLS GPU Pipeline - AP-8 Search (OPTIMIZED)
================================================
Searches for 8-term arithmetic progressions of primes near the LLL-resonant target.

Optimizations over base pipeline:
  1. shift-loop mul_mod (compatible with all GPUs)
  2. Skip even a0 (210d ensures all terms cycle odd/even → must start odd)
  3. High-throughput kernel: 512 threads, multiple candidates per thread (unroll 2x)
  4. Multiple LLL resonance targets (top 3 lattice vectors)
  5. Multi-target LLL (top 3 lattice vectors)

For k=8: primorial of primes <= 8 = 2*3*5*7 = 210
"""
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import sympy
from sympy import Matrix
import math
import time
from datetime import datetime

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
# 1. OPTIMIZED CUDA KERNEL
# =====================================================================
cuda_source = """
typedef unsigned long long uint64;

// OPTIMIZATION 1: Russian peasant multiplication (shift-loop)
// Works on all GPUs; __int128 not available on this machine
__device__ inline uint64 mul_mod(uint64 a, uint64 b, uint64 m) {
    uint64 r = 0; a %= m;
    while (b > 0) { if (b & 1) r = (r + a) % m; a = (a << 1) % m; b >>= 1; }
    return r;
}

__device__ uint64 pow_mod(uint64 base, uint64 exp, uint64 mod) {
    uint64 res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp >>= 1;
    }
    return res;
}

// Miller-Rabin with base-2 prefilter: catches ~75% of composites with 1 witness
__device__ bool is_prime_fast(uint64 n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if ((n & 1) == 0) return false;  // even > 2 -> composite
    if (n % 3 == 0) return n == 3;

    // Precompute d, s once
    uint64 d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }

    // OPTIMIZATION 3: Base-2 first (catches ~75% of composites cheaply)
    {
        uint64 x = pow_mod(2, d, n);
        if (x != 1 && x != n - 1) {
            bool composite = true;
            for (int r = 1; r < s; r++) {
                x = mul_mod(x, x, n);
                if (x == n - 1) { composite = false; break; }
            }
            if (composite) return false;
        }
    }

    // Remaining witnesses only if base-2 passed
    const uint64 witnesses[] = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 11; i++) {
        uint64 a = witnesses[i];
        if (n <= a) break;
        uint64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

// OPTIMIZATION 2 & 4: High-throughput kernel
// - 512 threads per block (better occupancy on Turing/T4)
// - Each thread processes 2 candidates (instruction-level parallelism)
// - Skip even starting values implicitly via input generation
__global__ void evaluate_progressions_opt(
    uint64* candidates, uint64 d_step, int k_len, int* results, int num_candidates
) {
    // Two candidates per thread for better ILP
    int idx0 = (blockIdx.x * blockDim.x + threadIdx.x) * 2;
    int idx1 = idx0 + 1;

    // Candidate 0
    if (idx0 < num_candidates) {
        uint64 base_a = candidates[idx0];
        bool valid = true;
        for (int j = 0; j < k_len; j++) {
            if (!is_prime_fast(base_a + j * d_step)) { valid = false; break; }
        }
        results[idx0] = valid ? 1 : 0;
    }

    // Candidate 1 (independent - good for ILP)
    if (idx1 < num_candidates) {
        uint64 base_a = candidates[idx1];
        bool valid = true;
        for (int j = 0; j < k_len; j++) {
            if (!is_prime_fast(base_a + j * d_step)) { valid = false; break; }
        }
        results[idx1] = valid ? 1 : 0;
    }
}
"""

# =====================================================================
# 2. MULTI-RESONANCE LLL TARGETING
# =====================================================================
def get_resonance_parameters(k_length):
    """OPTIMIZATION 5: Extract top 3 LLL vectors as multiple targets."""
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION (MULTI-TARGET)] ---")
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    target_ln = math.log(10**15)
    C = 10**8
    A = [int(alpha * C) for alpha in alphas]
    M = Matrix([[C, 0, 0, 0], [0, C, 0, 0], [0, 0, C, 0], [A[0], A[1], A[2], 1]])
    L = M.lll()

    targets = []
    d_step = get_required_primorial(k_length)

    for row_idx in range(min(3, L.rows)):
        base_q = abs(L[row_idx, 3])
        if base_q == 0:
            base_q = 1
        multiplier = int(target_ln * C / base_q)
        final_q = base_q * multiplier
        y = final_q / C
        a_target = int(math.exp(y))
        # Compute resonance quality: how close are the phase alignments?
        quality_scores = []
        for i, alpha in enumerate(alphas):
            phase = (y * alpha) % 1.0
            quality_scores.append(min(phase, 1.0 - phase))  # distance to nearest integer
        avg_quality = sum(quality_scores) / len(quality_scores)
        targets.append((a_target, d_step, y, avg_quality))
        print(f"  Target #{row_idx+1}: a={a_target:,}, ln(a)={y:.6f}, d={d_step}, quality={avg_quality:.4f}")

    # Sort by quality (lower = better alignment)
    targets.sort(key=lambda x: x[3])
    best = targets[0]
    print(f"\n  Best target: a={best[0]:,}, quality={best[3]:.4f}")
    return targets

# =====================================================================
# 3. OPTIMIZED GPU DISPATCHER
# =====================================================================
def run_gpu_sieve_optimized(mod, candidate_array, common_difference, k_length, batch_label):
    """
    OPTIMIZATION 2: Only test odd starting values.
    With d=210 (even), if a0 is even, ALL terms are even → composite.
    So we filter to odd a0 in numpy before GPU transfer.
    """
    # Filter to odd candidates only
    odd_mask = (candidate_array & 1) == 1
    odd_candidates = candidate_array[odd_mask]

    if len(odd_candidates) == 0:
        return []

    total = len(odd_candidates)
    fn = mod.get_function("evaluate_progressions_opt")
    threads = 512  # OPTIMIZATION 4: higher thread count for better occupancy
    chunk_size = 10_000_000

    all_matches = []
    processed = 0
    t_start = time.time()
    last_report = t_start

    for offset in range(0, total, chunk_size):
        end = min(offset + chunk_size, total)
        chunk = np.ascontiguousarray(odd_candidates[offset:end], dtype=np.uint64)
        n = len(chunk)

        # Alloc GPU mem
        d_chunk = cuda.mem_alloc(chunk.nbytes)
        d_res = cuda.mem_alloc(n * 4)
        cuda.memcpy_htod(d_chunk, chunk)
        cuda.memset_d8(d_res, 0, n * 4)

        # Launch kernel with 2x unroll
        blocks = (n + threads * 2 - 1) // (threads * 2)
        fn(d_chunk, np.uint64(common_difference), np.int32(k_length), d_res, np.int32(n),
           block=(threads, 1, 1), grid=(blocks, 1))
        cuda.Context.synchronize()

        # Read back
        h_res = np.zeros(n, dtype=np.int32)
        cuda.memcpy_dtoh(h_res, d_res)
        d_chunk.free()
        d_res.free()

        # Collect matches
        found = np.where(h_res == 1)[0]
        for idx in found:
            all_matches.append(chunk[idx])

        processed += n
        now = time.time()
        if now - last_report >= 8 or processed >= total:
            pct = 100 * processed / total
            elapsed = now - t_start
            rate = processed / elapsed if elapsed > 0 else 0
            eta = (total - processed) / rate if rate > 0 else 0
            effective_rate = len(candidate_array) / elapsed if elapsed > 0 else 0  # rate vs raw input
            print(f"  {batch_label}: {pct:.0f}% ({processed:,}/{total:,} odd)"
                  f" | {len(all_matches)} found | {rate:,.0f} odd/s ({effective_rate:,.0f} raw/s) | ETA {eta:.0f}s")
            last_report = now

        if len(all_matches) > 0:
            break

    return all_matches

# =====================================================================
# 4. ESTIMATE
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
    print(f"P(AP-{k})≈{p_ap:.2e}")
    # Account for odd-only filtering (50% reduction)
    expected_raw = 1.0 / p_ap
    expected_odd = expected_raw / 2  # half the candidates are odd
    print(f"Expected raw candidates: {expected_raw:.2e}")
    print(f"Expected odd candidates (after even-skip): {expected_odd:.2e}")
    print(f"  Expected batches of 10M raw: {expected_raw/10_000_000:.1f}")
    return expected_raw

# =====================================================================
# 5. MAIN
# =====================================================================
if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"RBLS Optimized Pipeline — AP-8 Search — {timestamp}")
    print("=" * 70)

    k_length = 8
    d_step = get_required_primorial(k_length)
    print(f"\nAP-{k_length} search, d={d_step}")

    expected_candidates = estimate_probability(k_length, d_step)

    print("\nCompiling OPTIMIZED CUDA kernel (shift-loop mul_mod + base-2 prefilter + 2x unroll)...")
    t0 = time.time()
    mod = SourceModule(cuda_source)
    print(f"CUDA compilation successful ({time.time()-t0:.1f}s).\n")

    # Get multiple resonance targets
    targets = get_resonance_parameters(k_length)

    batch_size = 10_000_000  # Raw batch size (before odd filtering → 5M effective)
    max_batches = 50  # Per target, so 3 targets × 50 = 150 batches max

    overall_start = time.time()
    total_found = 0

    # Search each target in order of quality
    for target_idx, (target_a, d_step, ln_a, quality) in enumerate(targets):
        print(f"\n{'='*70}")
        print(f"TARGET #{target_idx+1}: a={target_a:,}, quality={quality:.4f}")
        print(f"{'='*70}")

        batch_num = 1
        while batch_num <= max_batches:
            current_start = target_a + ((batch_num - 1) * batch_size)
            # Ensure odd start (d=210 is even, so a0 parity = all terms parity)
            if (current_start & 1) == 0:
                current_start += 1

            raw_count = batch_size
            if batch_num == 1:
                odd_count = (raw_count + 1) // 2  # roughly half are odd
                print(f"\nBatch {batch_num}: {current_start:,} ({odd_count:,} odd / {raw_count:,} raw) ...")
            else:
                print(f"\nBatch {batch_num}: {current_start:,} ...")

            candidates = np.arange(current_start, current_start + raw_count, dtype=np.uint64)

            t_batch_start = time.time()
            matches = run_gpu_sieve_optimized(mod, candidates, d_step, k_length, f"T{target_idx+1}B{batch_num}")
            t_batch_end = time.time()
            elapsed = t_batch_end - t_batch_start

            print(f"  Batch {batch_num} done: {elapsed:.1f}s, {len(matches)} found")

            # Cooling: 60s after each batch to protect GPU
            if batch_num >= 1 and batch_num < max_batches:
                print(f"  Cooling 60s ...")
                time.sleep(60)

            if matches:
                print("\n" + "=" * 70)
                print(f"*** FOUND AP-{k_length}! ***")
                print("=" * 70)
                for idx, m in enumerate(matches):
                    print(f"\nProgression #{idx+1} starting at {m}:")
                    for i in range(k_length):
                        term = m + i * d_step
                        print(f"  Index {i}: {term}")
                total_found += len(matches)
                break

            if batch_num == 1:
                remaining = max_batches * len(targets)
                print(f"  Est total for {remaining} batches: {elapsed*remaining/3600:.1f}h")

            batch_num += 1

        if total_found > 0:
            break
    else:
        # Exhausted all targets
        pass

    overall_end = time.time()
    print(f"\n--- [DONE] ---")
    print(f"Total time: {(overall_end-overall_start)/3600:.2f}h")
    print(f"AP-{k_length} found: {total_found}")
