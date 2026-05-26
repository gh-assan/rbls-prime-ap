import numpy as np
import sympy
from sympy import Matrix, primerange
import math
import time
from numba import njit, prange

# =====================================================================
# 0. PRIMORIAL CALCULATION
# =====================================================================

def get_required_primorial(k):
    """Calculates the product of all primes strictly less than k."""
    primes = list(sympy.primerange(2, k))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 1. THE CPU MULTIPROCESSING ENGINE (Compiled via Numba for Apple Silicon)
# =====================================================================

@njit
def mod_mul(a, b, m):
    """
    Overflow-safe modular multiplication for 64-bit integers.
    Uses Russian Peasant algorithm to prevent overflow without needing 128-bit ints.
    """
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
    """Modular exponentiation: (base^exp) % mod"""
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
    """Deterministic 64-bit Miller-Rabin Primality Test (Guaranteed for n < 2^64)"""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n % 3 == 0: return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Deterministic witnesses for all numbers < 2^64
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
    """
    Scans candidate array for length-k arithmetic progressions.
    parallel=True forces Numba to distribute this loop across all M1 CPU cores.
    """
    num_candidates = len(candidates)
    results = np.zeros(num_candidates, dtype=np.int32)
    
    for idx in prange(num_candidates):
        base_a = candidates[idx]
        valid_progression = True

    # Check all terms in the AP-k sequence
        for j in range(k_len):
            current_term = base_a + (j * d_step)
            if not is_prime(current_term):
                valid_progression = False
                break # Early exit on composite
                
        if valid_progression:
            results[idx] = 1
            
    return results

# =====================================================================
# 2. THE ANALYTIC BRAIN (SymPy LLL Lattice Reduction)
# =====================================================================

def get_resonance_parameters(k_length):
    print("--- [PHASE 1: ANALYTIC LLL REDUCTION] ---")
    
    # Imaginary parts of first 3 Riemann Zeros
    t = [14.134725142, 21.022039638, 25.010857580]
    alphas = [ti / (2 * math.pi) for ti in t]
    
    # We want to find a magnitude near 10^15. 
    target_ln = math.log(10**15)
    
    print("Constructing 4D Lattice for Simultaneous Diophantine Approximation...")
    C = 10**8  # Integer scaling factor
    A = [int(alpha * C) for alpha in alphas]
    
    # Matrix construction for LLL
    M = Matrix([
        [C, 0, 0, 0],
        [0, C, 0, 0],
        [0, 0, C, 0],
        [A[0], A[1], A[2], 1]
    ])
    
    # Run Lenstra-Lenstra-Lovasz
    L = M.LLL()
    
    # Extract the shortest vector's multiplier (q)
    base_q = abs(L[0, 3])
    if base_q == 0:
        base_q = 1
        
    multiplier = int(target_ln * C / base_q)
    final_q = base_q * multiplier
    
    y = final_q / C
    a_target = int(math.exp(y))
    
    # Compute primorial step size based on progression length
    d_step = get_required_primorial(k_length)
    
    print(f"LLL complete. Resonant base ln(a) found at: {y:.6f}")
    print(f"Target discrete starting magnitude (a): {a_target:,}")
    print(f"Computed primorial step size (d): {d_step}")
    
    return a_target, d_step

# =====================================================================
# 3. MAIN PIPELINE EXECUTION
# =====================================================================

if __name__ == "__main__":
    print("Initializing LLVM JIT Compilation for Apple M1...")
    
    # Step 1: Run analytic phase alignment
    k_length = 7  # Looking for a 7-term progression
    target_a, d_step = get_resonance_parameters(k_length)
    
    # Step 2: Configure the search space
    batch_size = 5_000_000  # 5 Million numbers per batch is comfortable for the M1
    
    print("\n--- [PHASE 2: DISCRETE M1 CPU SIEVE] ---")
    print(f"Generating block of {batch_size:,} candidates starting at {target_a:,}...")
    candidates = np.arange(target_a, target_a + batch_size, dtype=np.uint64)
    
    # Step 3: Dispatch to Numba parallel engine
    print(f"Dispatching to Apple Silicon performance cores...")
    start_time = time.time()
    
    # The first run will take an extra ~1-2 seconds as Numba compiles the C machine code
    results_mask = evaluate_progressions(candidates, d_step, k_length)
    
    end_time = time.time()
    print(f"Execution completed in {end_time - start_time:.4f} seconds.\n")
    
    # Step 4: Output Results
    successful_indices = np.where(results_mask == 1)[0]
    matches = [candidates[i] for i in successful_indices]
    
    print("--- [RESULTS] ---")
    print(f"Found {len(matches)} valid AP-{k_length} progressions.")
    
    if len(matches) > 0:
        print("\nDisplaying first discovered mathematical progression:")
        first_match = matches[0]
        for i in range(k_length):
            term = first_match + (i * d_step)
            print(f"Index {i}: {term}")