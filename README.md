# Prime arithmetic progressions: mathematical research and exact reference search

The goal is an explicit AP-28: 28 primes of the form `a + j*d`, for `j = 0,...,27`.

The current work has a **new mathematical proposal**, an exact one-difference reference sieve, and historical RBLS experiments. No AP-28 has been found here. The proposal has not yet supplied a mathematical AP-28 construction.

The requested discovery method is mathematical construction. Enumerating more starts, differences, or CRT cells does not meet that requirement. Search programs remain reference checks; final primality verification can validate a mathematically derived candidate.

A [fixed candidate check](research/fixed-ap27-candidate-check.md) independently verifies the August 2026 published AP-27 and derives its only direct extension not excluded modulo 29. The new endpoint has proper divisor 2971, so the candidate fails. Both composite neighbors also imply that any prime AP-28 can share at most 14 terms with this fixed source progression. This is a failed construction check, not an AP-28 discovery or a closed arithmetic gap.

[Garner Tree Search Is the Wheel](papers/gaps/G16-garner-tree.md) tests mixed-radix tree search with box pruning. Its best order saves a constant 12-23% of wheel work at every sieve bound; every level past the window modulus costs exactly `S_i(|G_p|-2)+S_{i+1}` more. Closed, with one practical constant: order filter primes by survival fraction.

[Meissel–Lehmer for Prime Patterns](papers/gaps/G15-pattern-counting.md) tests the second brainstorm candidate. The exact analogue of Legendre's recursion exists for every pattern and agrees with direct sieving on 39 sizes. For primes its states collapse to one per sieve prime; for twins, 3-term and 5-term progressions they grow faster than `x` (exponents 1.16-1.30). A substitution records its residue whenever a pattern has two forms, so the collapse behind sublinear prime counting does not extend. Closed.

[Resonance Bisection](papers/gaps/G14-resonance-bisection.md) tests the first candidate from the [domain-ladder brainstorm](research/brainstorm-domain-ladder.md). Sieve counts are exact sums of products of Dirichlet kernels; LLL on the CRT dual finds resonant frequencies carrying 88% of the count fluctuation at sieve bound 23, against 4% for low-complexity frequencies. The captured share falls as sieve primes are added, and bisection even with optimal frequencies costs 380 to 93,000 times the wheel. Rejected as a discovery method; the resonance finder is kept as a tool.

[How Far Is an AP-28?](papers/gaps/G13-calibrated-distance.md) calibrates the density model against PrimeGrid's actual counts (71 AP-26s, 4 AP-27s, no AP-28). A window model predicts the observed AP-26/AP-27 ratio (15.9 against 17.75) and about 20 AP-27 finds per AP-28. Isolating one of the roughly 13.6 expected AP-28s below `2^64` takes about 91 bits; congruences supply 36 bits cheaply. **Verdict: no known mathematical method yields an AP-28 without a search of roughly PrimeGrid's scale.** This is a limit of current mathematics; see the paper's Section 5.

[No Published AP-26 or AP-27 Record Extends to AP-28](papers/gaps/G12-record-extension-census.md) extends that check to all four known AP-27s and four published AP-26s. As of the record table updated 12 October 2026, 27 is still the longest known length. Both neighbors of every listed record have an exact proper divisor or are nonpositive, so any prime AP-28 shares at most 14 terms with each. Modulo 29, the only full extension window is the one Wróblewski's program already tests. The route of extending known records is closed; no AP-28 is supplied.

The [finite transference assessment](research/transference-route-assessment-2026-10-29.md) checks a March 2026 primary result against the actual scale. On both stated intervals, a `U^56` majorant error below one forces a pointwise bound below 2.01, incompatible with the indicated unscaled prime weights. Scaling the weights subject to the stated mean control leaves a density-only argument unable to guarantee AP-28: explicit sets with higher density contain no AP-28. This rules out the direct finite recipe assessed here, not all transference arguments or heights. It supplies no positive arithmetic bound or witness.

[A Sparsity and Confidence Audit of the AP-28 Route](papers/gaps/G11-sparsity-confidence-audit.md) proves that even the uniform one-sided character criterion needs at least 11 occupied quadratic classes of positive von Mangoldt tuple weight. It rigorously encloses the selected family's density-model main term between 1.129 and 1.181 at the full 64-bit height. These are model-integral bounds, not actual prime counts or success probabilities. The audit supports low confidence in the current uniform-mixing route and retains the full `23#` family with a prime-only weight as a simpler arithmetic target.

[A Sharp Character-Error Threshold and the Remaining Arithmetic Gap](papers/gaps/G10-sharp-character-threshold.md) proves the existing exact coefficient ratio is optimal for the fixed residue conditions and uniform-error metric. A matching abstract dual distribution supplies the proof. A parameter audit rejects one direct numerical substitution into a published uniformity theorem. Actual prime-correlation bounds and the AP-28 construction remain open.

[Signed Character Minorants for Finite AP-28 Certificates](papers/gaps/G9-character-minorant.md) reduces the modular error transfer to 174 character coefficients with a relative error factor below nine. It proves a finite sufficient inequality and a limitation of uniform absolute errors during localization. Actual arithmetic estimates meeting the inequality remain unproved.

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
python3 -m research.character_optimality
python3 -m research.archimedean_enclosure
python3 -m research.transference_audit
python3 -m research.check_published_ap27
python3 -m research.record_extensions
python3 -m research.ap28_distance
python3 -m research.resonance_bisection
python3 -m research.pattern_counting
python3 -m research.garner_tree
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
