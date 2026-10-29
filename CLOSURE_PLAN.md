# What is needed to close the AP-28 work

Date: 29 October 2026. Current goal: an explicit pair `(a,d)` with all 28 terms `a+j*d`, `0<=j<28`, independently verified prime. Proving existence at unspecified large heights is already known; this project seeks an explicit construction and a credible route to it.

## Two routes to the original goal

### Constructive route

1. Select an exactly described search family and domain. It may be a small subset of all possible AP-28s. Finding a witness does not require searching every possible pair.
2. Obtain an actual candidate whose 28 terms pass independent primality verification. Candidate generation may use a heuristic; the final witness proof must be exact.
3. Record the actual pair, all terms, verification method, tested domain, and sufficient provenance to reproduce it.

This settles the construction goal without requiring a global finite-height count-model error theorem. That separate theoretical claim would remain open unless proved.

### Analytic-certificate route

1. Define one finite family `R` precisely, including term-height limits, difference restrictions, roughness, primitivity, and boundary handling.
2. Obtain proved coupled bounds for its actual moments or another valid completion score. One sufficient condition is

   `L_R - U_M1 + (5/6)*L_M2 - (1/2)*U_M3 > 0`.

   The symbols must be valid arithmetic lower/upper bounds for the same family. Model fits do not provide these bounds.
3. Give a constructive way to evaluate certified subfamily scores accurately enough to localize a positive singleton. The localization contract is already proved; its oracle cost remains part of the arithmetic task.
4. Independently verify the recovered pair and every term.

If numerical calculations enter the certificate, their signed remainder must be controlled tightly enough that the final lower bound stays strictly positive. Exact Euler-product constants do not supply that control.

## What closing every research claim additionally requires

| Remaining claim | Closure evidence |
|---|---|
| G2: effective signed AP-28 aggregation | A complete incidence/candidate method with a demonstrated feasible budget, or a genuine aggregate arithmetic theorem giving a positive completion bound |
| G3b/G5: finite-height count-model accuracy | A proved discrepancy bound for the stated family and range; an independently enclosed integral if that model term is used; all selection conditions included |
| Explicit AP-28 output | The actual integers and independent primality verification of all 28 terms |

A witness alone proves existence of that progression. It does not establish accuracy of a global count model. Conversely, a positive heuristic main term is not a witness or a count lower bound.

## Work completed in this turn

A new local result strengthens the sparse-intersection analysis. In the cube-root sieve regime below `2^64`, five tail-prime constraints determine at most one primitive candidate, and classical rational reconstruction can recover it exactly. The proof checks the full size condition, and the implementation refuses unsupported regimes.

All 66 nonempty fifth-order intersections in the existing small arithmetic family were recovered, with independent checks on selected cells. This closes one local counting question. It does not bound the number of label sets to visit or establish a positive AP-28 score.

See [Primitive Tail Intersections as Rational Reconstruction](papers/gaps/G6-primitive-tail-decoding.md) and [the exact checks](results/tail-decoding-checks.json).

## Next gate

The decisive remaining work is **aggregate positivity or an actual witness**. A useful next result must do at least one of the following:

- compress the admissible-cell or tail-label enumeration with a proved completeness/cost advantage;
- establish actual coupled arithmetic bounds that make a completion score positive;
- produce a candidate whose 28 terms can be independently certified prime.

Small-length experiments and further identities can validate components, but they do not establish these AP-28 outcomes. No proof or compute budget currently available in this repository guarantees closure. Additional papers will not by themselves create the missing arithmetic result.
