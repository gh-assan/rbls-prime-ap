# Prime arithmetic progressions: mathematical research and exact reference search

The goal is an explicit AP-28: 28 primes of the form `a + j*d`, for `j = 0,...,27`.

The current work has a **new mathematical proposal**, an exact one-difference reference sieve, and historical RBLS experiments. No AP-28 has been found here. The proposal has not yet supplied a mathematical AP-28 construction.

The requested discovery method is mathematical construction. Enumerating more starts, differences, or CRT cells does not meet that requirement. Search programs remain reference checks; final primality verification can validate a mathematically derived candidate.

The latest note, [Signed Character Minorants for Finite AP-28 Certificates](papers/gaps/G9-character-minorant.md), reduces the modular error transfer to 174 character correlations with a relative error factor below nine. It proves a finite sufficient inequality and a limitation of uniform absolute errors during localization. Actual arithmetic estimates meeting the inequality remain unproved.

[Removing Prime Powers by Finite Group Structure](papers/gaps/G8-power-exclusion.md) constructs residue classes containing no perfect powers below `2^64`, eliminating the prime-power correction on a specified family. Exact group theory counts the retained classes without enumerating them. An explicit composite passing the conditions confirms that primality and an AP-28 construction remain unproved.

[A Structural Analytic Route to AP-28](papers/gaps/G7-structural-analytic-route.md) gives the preceding finite prime-correlation criterion and proves a finite-size obstruction to a crude global Fourier certificate. A usable numerical remainder and a mathematical recovery rule are still missing.

The [closure plan](CLOSURE_PLAN.md) states what a verified AP-28 result requires. The preceding local result, [primitive tail decoding](papers/gaps/G6-primitive-tail-decoding.md), proves that sufficiently large tail intersections can be decoded exactly by rational reconstruction. It does not supply aggregate positivity.

The [gap ledger](GAP_LEDGER.md) links focused follow-up papers: primitive exclusions, signed aggregation, rigorous Euler-product errors, witness localization, and finite-height arithmetic remainders. It records which finite subproblems are resolved and which AP-28 claims remain open.

The third paper, [Coupled Defect Moments and Exact Lattice Counts for AP-28](paper_ap28_coupled_bounds.md), proves sharp moment certificates, an explicit limited-independence obstruction, and a 64-bit sparsity obstruction to estimating individual five-prime intersections. It adds exact floor-sum counts and an arithmetic AP-7 check. Aggregate AP-28 bounds remain unproved. The [reproducible certificates](results/coupled-analysis.json) separate arithmetic checks from probability models and geometric proxies.

The follow-up paper, [From Local Admissibility to Prime Completion](paper_ap28_completion.md), derives a finite certificate using five defect moments and identifies the arithmetic bounds still needed for AP-28. Its exact checks and separately labeled model tables are in [the completion analysis](results/completion-analysis.json).

Read [A Projective Lattice Approach to Prime Arithmetic Progressions](paper_projective_ap28.md) first. It studies both the start and difference, combines finite-field projective directions with CRT lattices, and derives the limits of the apparent probability gains. It includes proofs, quantitative estimates, research questions, and primary references.

The earlier [RBLS paper](paper.md) is retained as a historical report with corrections. Its zeta-zero LLL scaling loses the measured phase alignment. The [review](research/review-2026-10-28.md) records that failure, arithmetic bugs, and unresolved historical exposure counts.

## Setup

Python 3.10+ is recommended. The current code was also checked on the available Python 3.9.6 environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

`numpy` and `sympy` suffice for the new reference sieve. `numba` supports the corrected historical CPU engines. PyCUDA and an NVIDIA CUDA toolchain are needed only for historical GPU scripts. The default test suite does not require a GPU; where a C++ compiler is available, it checks the actual CUDA device arithmetic as host C++. That does not establish GPU compilation, dispatch, or performance.

## Exact reference search

```bash
python3 search_prime_ap.py --k 9 --start 1000000000 --count 5000000 \
  --difference 223092870 --output results/ap9-demo.json
```

This examines **every start** in `[start, start+count)`, finds all matches, and records misses, sieve survivors, primality-test counts, and elapsed time. Terms may extend beyond the start interval. The default difference is the product of all primes at most `k`.

CRT generates admissible starts, a segmented sieve excludes small factors from every term, and the final verifier uses exact Python integer arithmetic with twelve Miller–Rabin bases valid below `2^64`. Inputs that would exceed that domain are rejected. Segment memory depends on the start interval block, not on the progression span.

A reproducible fixed demonstration found 11 AP-9s in five million starts; all 99 terms were independently checked with SymPy. Its raw output is [here](results/ap9-structured.json). This supports the reference implementation; it is not evidence for the separate projective research proposal or for AP-28 feasibility.

## Mathematical certificates and estimates

```bash
python3 research/projective_lattice.py
python3 research/run_coupled_analysis.py
python3 research/run_gap_checks.py
python3 -m research.character_minorant
python3 estimate_ap28.py --start 1000000000000000
python3 plan_prime_ap.py --start 1000000000000000 \
  --differences 223092870 6469693230 200560490130 --pilot-count 10000000
python3 research/run_experiments.py
```

The lattice certificate checks exact finite-field counts and basis preservation. It does not search all projective cells. The planner ranks differences by a conjectural density and measured short-pilot work; repeat and enlarge pilots before using a ranking. The experiment runner records all repeats and misses and compares modular generation with direct testing using the same primality verifier.

Increasing a raw-start probability is different from increasing success per unit work. In particular, adding primes to the difference multiplies both the raw density and the sieve survival fraction. The paper derives their cancellation and accounts for the logarithm of each term.

## Historical programs

`rbls_m1_pipeline*.py` retain the old LLL targets for reproducibility and now share corrected unsigned Numba arithmetic in `rbls_numba.py`. Their historical targeting is explicitly marked as unsupported. `rbls_gpu_pipeline*.py` retain CUDA variants with repaired modular addition; a CUDA hardware run remains outstanding.

The legacy AP-28 GPU prototype collects primes in a complete term window. Its configured billion-integer window is shorter than the required 6,023,507,490 span, so it deliberately exits before GPU startup. Use the new reference sieve for bounded-memory searches on starting values. See [AP-28 notes](ap28_notes.md).

The reported AP-7 and AP-8 tuples are genuine primes. Their old run logs do not establish a resonance speedup; the AP-7 exposure is inconsistent and the AP-9 total includes unreconciled coverage. Preserve those logs as historical evidence, not calibrated benchmarks.
