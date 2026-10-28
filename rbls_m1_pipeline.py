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
    """Calculates the product of all primes <= k."""
    primes = list(sympy.primerange(2, k + 1))
    primorial = 1
    for p in primes:
        primorial *= p
    return primorial

# =====================================================================
# 1. THE CPU MULTIPROCESSING ENGINE (Compiled via Numba for Apple Silicon)
# =====================================================================

from rbls_numba import mod_mul, pow_mod, is_prime, evaluate_progressions

# =====================================================================
# 2. THE ANALYTIC BRAIN (SymPy LLL Lattice Reduction)
# =====================================================================

def get_resonance_parameters(k_length):
    import warnings
    warnings.warn("Legacy LLL scaling does not preserve phase alignment; "
                  "use search_prime_ap.py for the modular search.", RuntimeWarning)
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
    L = M.lll()
    
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
    
    print(f"LLL complete. Historical target ln(a): {y:.6f}")
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
