# AP-28 gap ledger

Last updated: 29 October 2026. A gap is closed only at the scope stated below. A conditional reformulation does not establish an AP-28 or a practical discovery budget.

The first three papers are committed through `a8ddcc9` on `codex/prime-ap-math-review`.

| Gap | Dedicated paper | Status | Evidence required for full closure |
|---|---|---|---|
| G1. Primitive-point and origin exclusions in a geometric cell | [Primitive-point exclusions](papers/gaps/G1-primitive-exclusions.md) | Resolved for finite correctness; large-domain cost remains in G2 | Correct sublattice intersections, Möbius inversion, independent finite counts |
| G2. Signed aggregation over tail-prime labels | [Signed tail aggregation](papers/gaps/G2-signed-aggregation.md) | Open arithmetic problem | A proved positive AP-28 arithmetic bound and witness recovery from mathematical structure |
| G3a. Error from truncating the local-factor product | [Euler-product errors](papers/gaps/G3-euler-product-errors.md) | Resolved for the stated products and parameters | Outward-rounded partial products and a proved infinite-tail enclosure |
| G3b/G5. Error between a finite-height model and actual AP-28 counts | [Finite-height remainders](papers/gaps/G5-finite-height-remainder.md) | Open; actual arithmetic counterfamily verifies a limitation | A valid finite-height arithmetic remainder; bounding the Euler tail alone does not supply one |
| G4. Locate a witness from a positive finite-family certificate | [Witness localization](papers/gaps/G4-witness-localization.md) | Resolved as a finite localization contract; oracle cost remains in G2 | Additive score, certified child selection, finite termination, independent term verification |
| Goal: an explicit verified AP-28 derived mathematically | All papers | Open | Actual `(a,d)`, a mathematical construction, and verification of all 28 terms; no such witness is currently supplied |

Existing results are in [the projective formulation](paper_projective_ap28.md), [completion certificates](paper_ap28_completion.md), and [coupled bounds](paper_ap28_coupled_bounds.md). The third paper proves limits of certain five-moment strategies; it does not prove that AP-28 is impossible.

## Verified results in the gap papers

- G1: an exact divisibility-intersection basis and finite Möbius correction; a general triangular coefficient is retained when an integer slope no longer exists.
- G2: Boolean incidence aggregation handles multiple tail factors without a cube-root depth assumption; complete AP-7 coverage gives 2005 defects, score `1069/15`, and 78 zero-defect candidates. It does not establish an efficient complete AP-28 incidence stream.
- G3a: rigorous infinite-product enclosures are `3.312948771602789797972e18 <= beta <= 3.324621461220568134309e18`, with local-factor ratio between `3.549438062740978869797` and `3.550396938396844835386`.
- G4: an additive-score bisection contract, with interval refinement conditions, locates and independently verifies an AP-7 witness. It is not an AP-28 oracle.
- G5: a verified arithmetic family inside the 64-bit domain passes every prime through 37 while factor 41 forces a composite term. This demonstrates a limitation of finite local information, not an AP-28 impossibility result.

Reproduce all five checks with `python3 research/run_gap_checks.py`. The machine-readable evidence is [results/gap-checks.json](results/gap-checks.json).

## Open completion gate

The series has **not** established a positive AP-28 arithmetic bound, complete feasible AP-28 coverage, or an explicit AP-28. Further papers count as progress only when they add a checked result or a concrete counterexample; restating these requirements does not close them.

## New local result: primitive tail decoding

[Primitive Tail Intersections as Rational Reconstruction](papers/gaps/G6-primitive-tail-decoding.md) proves that every specified fifth-order tail intersection in the cube-root, 64-bit AP-28 regime has at most one primitive candidate and meets a complete rational-reconstruction size bound. The exact decoder recovers all 66 nonempty fifth-order intersections in the existing small validation family. Aggregate AP-28 positivity remains open; recovered defect candidates are not prime witnesses.

The [closure plan](CLOSURE_PLAN.md) distinguishes the original witness goal from the additional count-model theorem. A verified witness settles the construction goal even if the global model-error claim remains open.

## Required mathematical discovery method

The user requires a mathematical construction, without brute-force discovery. Enumeration cost improvements alone no longer satisfy the completion gate. Reference searches and small proof checks remain validation tools.

[A Structural Analytic Route to AP-28](papers/gaps/G7-structural-analytic-route.md) gives a finite analytic certificate accounting explicitly for prime-power contributions. It correctly separates the effective quantitative theorem of Tao and Teräväinen from Leng's stronger error rate with an ineffective implied constant. It also proves a sharp norm-to-pointwise lower comparison that makes the crude global `U^27` certificate unhelpful at the current height unless its model already determines primality pointwise.

This is a checked mathematical limitation and a precise analytic target. It does **not** close G2, the required numerical finite-height remainders in G3b/G5, or the explicit-construction goal. The published asymptotic theorem applies to the full convex cone, not automatically to the selected rough families used in earlier papers.

## Prime-power correction resolved on a new finite family

[Removing Prime Powers by Finite Group Structure](papers/gaps/G8-power-exclusion.md) proves a residue-class construction excluding all perfect powers below `2^64`. On the associated AP-28 family, the proper-prime-power correction in a von Mangoldt count is exactly zero. The proof counts the retained 152,755,199 classes algebraically, without a class scan or candidate search. [Exact evidence](results/power-exclusion-checks.json) includes the exceptional thirteenth power and the finite-group certificates.

This closes the **prime-power correction for this family only**. It leaves the finite prime-correlation remainder and actual witness recovery open. The construction also proves that every retained class contains a composite progression below 90,575,705,251, so these congruences cannot by themselves be a primality construction. The former full-cone and rough-family claims retain their stated scopes.

## Modular error transfer resolved with a signed character minorant

[Signed Character Minorants for Finite AP-28 Certificates](papers/gaps/G9-character-minorant.md) replaces a separate remainder for each selected residue class by a minorant with 174 character coefficients. Absorbing the exceptional power into a quadratic subgroup gives a positive principal coefficient and a nonprincipal-to-principal coefficient ratio below nine. Under actual principal and twisted arithmetic bounds, `E0 + 9*epsilon < V_M(X)*beta_L` is sufficient for an AP-28. The paper supplies the transfer inequality, **not numerical arithmetic bounds satisfying it**.

This closes the modular error-aggregation step. G2 and G3b/G5 remain open. A separate Parseval result proves that the uniform absolute-error version needs at least 48 occupied quadratic quotient classes and cannot certify a singleton. The one-sided signed expression retains more information; constructive recovery must supply that information through valid child estimates or another structural method. [Exact constants](results/character-minorant-checks.json) explicitly record that the actual arithmetic bounds are unavailable.

## Certificate optimization resolved; arithmetic loop remains open

[A Sharp Character-Error Threshold and the Remaining Arithmetic Gap](papers/gaps/G10-sharp-character-threshold.md) supplies an exact matching dual measure and proves that `6015973/693733` is the optimal uniform Fourier-error ratio for the fixed five bad subgroups. The measure has no safe mass while every nonprincipal character amplitude is at most `693733/6015973`. It is an abstract unit-class distribution, not a distribution of actual prime progressions.

This closes the weight-optimization question within that framework. It does not close the arithmetic remainder. A separate source audit finds that the direct use of the published `2<=w<=Q(N)` uniformity range cannot take `w>23` when `N<2^64`; another cited stronger rate has an ineffective constant. These checks reject those numerical shortcuts, not AP-28 or all other analytic applications. [The certificate](results/character-optimality-checks.json) records the exact dual weights and scopes.

The loop still lacks a proved positive finite arithmetic score and a mathematical witness-recovery rule. Further coefficient rearrangements inside the optimized uniform framework cannot supply them. No AP-28 is supplied, and the remaining research gaps are not marked closed.

## Sparsity audit and enclosure of the continuous model term

[A Sparsity and Confidence Audit of the AP-28 Route](papers/gaps/G11-sparsity-confidence-audit.md) proves that the uniform one-sided character criterion requires at least 11 occupied quadratic quotient classes of nonzero von Mangoldt tuples. This population can include prime powers outside the selected family; it is not a claim of 11 prime progressions.

The same note encloses the defined continuous main terms at `2^64-1`: the selected `7*23#` family has model term between 1.129 and 1.181, while the unrestricted `23#` family has model term between 13.270 and 13.876. The selected model is at most `1651/19404 < 8.51%` of the latter. Exact box areas, logarithm enclosures, outward rounding, and the earlier Euler-product enclosure establish these numerical statements. [The certificate](results/archimedean-enclosure-checks.json) explicitly marks the actual finite prime-count error and witness as unavailable.

This closes evaluation of this continuous model term at this height, **not the arithmetic discrepancy in G3b/G5**. The audit lowers confidence in uniform mixing as the main construction route. The full `23#` family with the prime-only weight `mu(n)^2*Lambda(n)` is retained as a simpler target for a new finite arithmetic bound; the weight's definition is not such a bound or a recovery algorithm.

## Finite assessment of the March 2026 transference result

The [new source assessment](research/transference-route-assessment-2026-10-29.md) checks the actual interval norm rather than assuming a cyclic-group obstruction transfers automatically. Its sharp comparison rules out a `U^56` majorant error below one for the stated unscaled prime peaks on the two assessed intervals. For scaled/thinned weights with the specified mean control, exact digit-defined counterexamples also rule out a positive universal AP-28 bound based only on the resulting density at these scales. The prescribed `W` of the cited theorem is separately checked.

[The exact certificate](results/transference-audit-checks.json) records these finite obstructions and explicitly leaves the actual AP-28 arithmetic lower bound and witness unavailable. This eliminates the direct finite recipe under its stated hypotheses. It does not rule out AP-28, larger heights, or arguments exploiting additional arithmetic structure, and it closes none of G2, G3b/G5, or the construction goal.

## Published records cannot be extended

[No Published AP-26 or AP-27 Record Extends to AP-28](papers/gaps/G12-record-extension-census.md) checks the four known AP-27s and four published AP-26s against the record table updated 12 October 2026, which still lists 27 as the longest length. An overlap lemma forces any prime AP-28 sharing at least 15 terms with a record to contain one of its two adjacent neighbors. All 16 neighbors have an exact proper divisor or are nonpositive. [The certificate](results/record-extension-checks.json) also blocks all 20 full-containment windows and shows exactly one window per record survives modulo 29.

This closes the record-extension route completely. It supplies no new candidate and closes none of G2, G3b/G5, or the construction goal.

## Calibration against actual record counts and verdict

[How Far Is an AP-28?](papers/gaps/G13-calibrated-distance.md) uses PrimeGrid's totals (71 AP-26s, 4 AP-27s, 0 AP-28s, accessed 29 October 2026). An independent neighbor probability predicts the AP-26/AP-27 ratio as 15.9; the observed 17.75 is within Poisson noise. This is actual-count evidence for the density model at record heights. It is not the finite-height theorem G3b/G5 requires. The model predicts about 20 maximal AP-27s per AP-28, with a data-only range of 8 to 86.

The paper also measures the information congruences supply: 36 of the roughly 91 bits needed through prime 541, and output-sensitive CRT enumeration stops paying near prime 83. With the existence, deterministic-prime and structure barriers in its Section 5, this supports a firm verdict: **G2 and G3b/G5 are open problems of current mathematics, and the search-free construction goal cannot be met with known methods.** [The calibration](results/ap28-distance.json) is reproducible.

## Brainstorm experiments

The [domain-ladder brainstorm](research/brainstorm-domain-ladder.md) lists unproved candidate methods; each tested one gets its own note.

- C1, [Resonance Bisection](papers/gaps/G14-resonance-bisection.md): rejected. LLL finds the resonant frequencies of a sieve's exact Fourier expansion, but their share of the deciding information falls with each added sieve prime, and guided bisection costs 380 to 93,000 times wheel enumeration on an AP-10 analog. [Results](results/resonance-bisection.json).
