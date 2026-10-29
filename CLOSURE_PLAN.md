# What is needed to close the AP-28 work

Date: 29 October 2026. Current goal: an explicit pair `(a,d)` with all 28 terms `a+j*d`, `0<=j<28`, independently verified prime. Proving existence at unspecified large heights is already known; this project seeks an explicit construction and a credible route to it.

## Method constraint

The user requires a mathematical method of finding the pair, without brute-force discovery. Enlarging a grid, enumerating CRT directions or tail labels, and checking more candidates do not satisfy that instruction. Existing search engines support validation of earlier work. Software may check identities, bound numerical errors, and verify the 28 terms of a mathematically derived candidate.

## Two routes to the original goal

### Constructive route

1. Derive a candidate from specified mathematical structure and state its domain. It may be a small subset of all possible AP-28s. Finding a witness does not require covering every possible pair.
2. Prove that the construction supplies an actual candidate whose 28 terms pass independent primality verification. A heuristic ranking alone does not supply the required mathematical construction.
3. Record the actual pair, all terms, verification method, tested domain, and sufficient provenance to reproduce it.

This settles the construction goal without requiring a global finite-height count-model error theorem. That separate theoretical claim would remain open unless proved.

### Analytic-certificate route

1. Define one finite family `R` precisely, including term-height limits, difference restrictions, roughness, primitivity, and boundary handling.
2. Obtain proved coupled bounds for its actual moments or another valid completion score. One sufficient condition is

   `L_R - U_M1 + (5/6)*L_M2 - (1/2)*U_M3 > 0`.

   The symbols must be valid arithmetic lower/upper bounds for the same family. Model fits do not provide these bounds.
3. Give a constructive way to evaluate certified subfamily scores accurately enough to localize a positive singleton. The localization contract is already proved; its oracle must follow from mathematical structure with justified recovery cost. Computing the oracle by exhaustively searching the family does not meet the method constraint.
4. Independently verify the recovered pair and every term.

If numerical calculations enter the certificate, their signed remainder must be controlled tightly enough that the final lower bound stays strictly positive. Exact Euler-product constants do not supply that control.

## What closing every research claim additionally requires

| Remaining claim | Closure evidence |
|---|---|
| G2: effective signed AP-28 aggregation | A genuine aggregate arithmetic theorem giving a positive completion bound and a mathematical way to recover its witness |
| G3b/G5: finite-height count-model accuracy | A proved discrepancy bound for the stated family and range; an independently enclosed integral if that model term is used; all selection conditions included |
| Explicit AP-28 output | The actual integers and independent primality verification of all 28 terms |

A witness alone proves existence of that progression. It does not establish accuracy of a global count model. Conversely, a positive heuristic main term is not a witness or a count lower bound.

## Local decoding result

A new local result strengthens the sparse-intersection analysis. In the cube-root sieve regime below `2^64`, five tail-prime constraints determine at most one primitive candidate, and classical rational reconstruction can recover it exactly. The proof checks the full size condition, and the implementation refuses unsupported regimes.

All 66 nonempty fifth-order intersections in the existing small arithmetic family were recovered, with independent checks on selected cells. This closes one local counting question. It does not bound the number of label sets to visit or establish a positive AP-28 score.

See [Primitive Tail Intersections as Rational Reconstruction](papers/gaps/G6-primitive-tail-decoding.md) and [the exact checks](results/tail-decoding-checks.json).

## Next gate

The decisive remaining work is **aggregate positivity or an actual witness**. A useful next result must do at least one of the following:

- establish actual coupled arithmetic bounds that make a completion score positive;
- prove an analytic prime-correlation bound with numerical errors small enough for a positive certificate;
- derive a candidate from mathematical structure whose 28 terms can be independently certified prime.

Small-length experiments and further identities can validate components, but they do not establish these AP-28 outcomes. No proof or compute budget currently available in this repository guarantees closure. Additional papers will not by themselves create the missing arithmetic result.

## Structural analytic route

[The seventh note](papers/gaps/G7-structural-analytic-route.md) supplies an alternative sufficient condition on the full two-variable cone: a proved lower bound for the actual von Mangoldt correlation must exceed an explicit upper bound for contributions from proper prime powers. Published effective quantitative theorems imply this eventually at large heights. This repository does not extract a usable height, numerical remainder, or witness-recovery map.

The note also proves that a crude global normalized `U^27`-norm error certificate below the current height requires nearly pointwise knowledge of primality. Applying that generic bound to a cheap density model cannot close the gap. This obstruction is specific to the stated certificate; it does not exclude relative or structured analytic methods.

## Algebraic removal of the prime-power correction

[The eighth note](papers/gaps/G8-power-exclusion.md) constructs 152,755,199 unit classes modulo `7*23#` containing no perfect powers below `2^64`. The count follows from independent primary components of finite unit groups; no progression candidates or full residue tables are enumerated. On progressions preserving one of these classes, a positive von Mangoldt product comes from primes, so that family's prime-power correction is zero.

The theorem has a finite height restriction. Every fixed unit class contains perfect powers at sufficiently large heights. The same note constructs a composite progression in every retained class below 90,575,705,251, showing that the congruences alone do not force primality. A sufficiently strong joint arithmetic bound and a constructive recovery rule remain missing.

## Compact arithmetic target after modular aggregation

[The ninth note](papers/gaps/G9-character-minorant.md) proves an exact signed minorant using one principal and 173 nonprincipal characters. A valid principal lower bound `T0 >= V_M(X)*beta_L - E0` and valid upper bounds `Re(Tchi) <= epsilon` imply a positive AP-28 certificate whenever `E0 + 9*epsilon < V_M(X)*beta_L`, in the stated height range. Only one-sided weighted information is fundamentally required; absolute-value bounds are a stronger optional assumption.

The modular coefficient loss is now bounded independently of the number of selected residue classes. The arithmetic bounds themselves remain unproved. A uniform absolute-error version fails near a singleton, as proved by Parseval, so the existing bisection contract still needs a sharper arithmetic oracle or a phase-aware structural recovery rule. This note does not close finite prime-correlation positivity or produce the actual pair.

## Results of the next proof-and-review loop

[The tenth note](papers/gaps/G10-sharp-character-threshold.md) checks two possible ways forward:

1. **Improve the residue minorant:** closed by an exact optimality proof. The existing ratio `6015973/693733` already attains the best possible uniform character-error ratio for the fixed safe set. A matching dual distribution proves the lower bound for every pointwise minorant, including those with more character terms.
2. **Insert a published quantitative estimate directly:** the proposed `w>23` substitution fails the stated `w<=Q(N)` range at natural 64-bit scale; the stronger cited logarithmic theorem has an ineffective implied constant. These facts do not rule out other applications or a separately derived finite bound, but neither substitution supplies the required numerical errors.

The decisive unresolved work is still actual arithmetic positivity and constructive recovery. The dual measure is abstract and does not show that an arithmetic AP-28 distribution has the same obstruction. Subsequent passes need new arithmetic information, nonuniform signed control, or a different proved construction. A conditional rewrite, uninstantiated asymptotic constant, or another rearrangement of this optimal minorant does not close a gap. No finite termination guarantee for this research loop has been established.

## Confidence audit and working direction

[The eleventh note](papers/gaps/G11-sparsity-confidence-audit.md) supplies a one-sided support obstruction and a rigorous enclosure of a defined model integral. Even the uniform one-sided gate needs at least 11 occupied quadratic classes. The selected family's model term is only between 1.129 and 1.181 at the full 64-bit height; this is not a bound on an actual count or a success probability. No contradiction is inferred because the arithmetic model error is unproved and the unselected weighted population may contain proper prime powers.

The power-free restrictions simplify a proof component but retain at most 8.51% of the unrestricted `23#` family's defined model term. Their net benefit toward an actual construction has not been demonstrated. Confidence in the checked finite components is high subject to review; confidence in this uniform-mixing construction route is low. A completion percentage or calibrated success probability is unavailable.

Keep the residue certificates as auxiliary tools. Use the full `23#` family and the exact prime-only weight `theta_*(n)=mu(n)^2*Lambda(n)` as the primary arithmetic target. A proved positive finite correlation for that weight, or a phase-aware signed bound supplying an actual construction, is required. Introducing this weight closes neither the arithmetic estimate nor witness recovery; it avoids imposing extra residue restrictions merely to remove prime powers.

## Newer transference result: finite applicability checked

The [29 October assessment](research/transference-route-assessment-2026-10-29.md) examines the March 2026 sparse Green–Tao result using its interval norm and stated parameters. The prescribed `W` in Theorem 6.2 is 1 at the present height; replacing it directly by `23#` is not licensed by that formula. Both the published `W=1` interval and a hypothetical `W=23#` adaptation have an additional finite obstruction: a `U^56` majorant error below one forces the majorant below 2.01 pointwise, incompatible with the stated unscaled prime-weight peaks.

For scaled or thinned prime weights with that majorant and an absolute dense-model mean error at most 0.01, the mean of the resulting `[0,1]`-valued model is below the density of an explicit AP-28-free digit set. Consequently its mean alone cannot give a positive universal progression bound at these scales. Exact counts, a sharp interval-norm comparison, and a finite Brun–Titchmarsh bound establish this result. It is stronger than merely failing to extract asymptotic constants, but its scope is the direct finite recipe stated in the assessment.

Do not continue this recipe by assigning optimistic constants or adding another conditional density criterion. A useful next construction argument must bring in the actual joint arithmetic or exploit specific structure of a model beyond density. Larger heights and other relative methods remain possible research directions, without a demonstrated construction here. The original witness goal and G2/G3b/G5 remain open; this assessment is negative route evidence, not a completed AP-28 gate.
