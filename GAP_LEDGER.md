# AP-28 gap ledger

Last updated: 29 October 2026. A gap is closed only at the scope stated below. A conditional reformulation does not establish an AP-28 or a practical discovery budget.

The first three papers are committed through `a8ddcc9` on `codex/prime-ap-math-review`.

| Gap | Dedicated paper | Status | Evidence required for full closure |
|---|---|---|---|
| G1. Primitive-point and origin exclusions in a geometric cell | [Primitive-point exclusions](papers/gaps/G1-primitive-exclusions.md) | Resolved for finite correctness; large-domain cost remains in G2 | Correct sublattice intersections, Möbius inversion, independent finite counts |
| G2. Signed aggregation over tail-prime labels | [Signed tail aggregation](papers/gaps/G2-signed-aggregation.md) | Open arithmetic efficiency problem | Complete candidate/incidence coverage and a positive AP-28 signed bound within an established budget |
| G3a. Error from truncating the local-factor product | [Euler-product errors](papers/gaps/G3-euler-product-errors.md) | Resolved for the stated products and parameters | Outward-rounded partial products and a proved infinite-tail enclosure |
| G3b/G5. Error between a finite-height model and actual AP-28 counts | [Finite-height remainders](papers/gaps/G5-finite-height-remainder.md) | Open; actual arithmetic counterfamily verifies a limitation | A valid finite-height arithmetic remainder; bounding the Euler tail alone does not supply one |
| G4. Locate a witness from a positive finite-family certificate | [Witness localization](papers/gaps/G4-witness-localization.md) | Resolved as a finite localization contract; oracle cost remains in G2 | Additive score, certified child selection, finite termination, independent term verification |
| Goal: an explicit verified AP-28 and feasible route to obtain it | All papers | Open | Actual `(a,d)` and verification of all 28 terms; no such witness is currently supplied |

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

[A Structural Analytic Route to AP-28](papers/gaps/G7-structural-analytic-route.md) gives a finite analytic certificate with the prime-power contribution explicitly removed. It correctly separates the effective quantitative theorem of Tao and Teräväinen from Leng's stronger error rate with an ineffective implied constant. It also proves a sharp norm-to-pointwise lower comparison that makes the crude global `U^27` certificate unhelpful at the current height unless its model already determines primality pointwise.

This is a checked mathematical limitation and a precise analytic target. It does **not** close G2, the required numerical finite-height remainders in G3b/G5, or the explicit-construction goal. The published asymptotic theorem applies to the full convex cone, not automatically to the selected rough families used in earlier papers.
