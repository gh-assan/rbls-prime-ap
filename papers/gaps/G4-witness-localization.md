# Constructive Localization from a Positive Prime-Completion Score

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Gap G4:** The finite localization contract is resolved. A positive AP-28 input certificate, an affordable score oracle, and an actual AP-28 witness are not supplied.

### Abstract

A positive aggregate certificate is useful only if it can lead to an explicit progression. We give a finite localization procedure for an additive prime-completion minorant. With an exact score oracle, at most $1+\lceil\log_2R\rceil$ score queries locate a zero-defect candidate in an indexed family of size $R$. Certified intervals can replace exact child scores when their width is small enough relative to the positive parent lower bound. Rational score spacing provides a finite precision criterion, although its absolute precision can be expensive for large families. A completely enumerated AP-7 example demonstrates the contract and independent final verification. The query bound does not include the cost of evaluating the arithmetic scores.

### 1. The required input contract

Let $\mathcal R=\{x_0,\ldots,x_{R-1}\}$ be a finite, correctly covered candidate family. Let $C(x)$ be its **actual** number of composite terms and let

$$P(0)=1,\qquad P(c)\le0\quad(c=1,\ldots,k).$$

Define the additive score

$$S(J)=\sum_{i\in J}P(C(x_i)).$$

Assume a positive initial certificate $S(\mathcal R)>0$. An exact score oracle returns $S(J)$ on requested index intervals. It must not substitute the number of defects observed in an incomplete incidence stream for $C$.

The contract isolates a previously implicit requirement. Neither the existence nor the efficiency of an AP-28 score oracle is proved here; those belong to [G2](G2-signed-aggregation.md).

### 2. Exact localization

Bisect the current index interval into disjoint children $L$ and $R$. Query $S(L)$. If it is positive, retain $L$. Otherwise retain $R$, whose score is the positive parent score minus $S(L)$.

**Theorem 1.** Starting from a positive parent score, this procedure reaches a zero-defect singleton after at most $\lceil\log_2R\rceil$ child queries.

**Proof.** Additivity gives $S(\text{parent})=S(L)+S(R)$. If the left score is nonpositive, the right is strictly positive. Hence every retained interval has positive score. Its size is at most the ceiling of half the previous size. At a singleton, positivity of $P(C)$ forces $C=0$. $\square$

Counting an initial oracle query for the whole family gives at most $1+\lceil\log_2R\rceil$ queries. This is a query bound, not an elapsed-time or bit-complexity bound. The oracle may require a very large arithmetic calculation at each node.

### 3. Certified intervals and shared information

Suppose the parent has a valid lower bound $\ell>0$, while the left score lies in $[a,b]$. Then

$$S(R)\ge\ell-b.$$

Thus retain the left child if $a>0$; otherwise retain the right if $\ell-b>0$. If neither holds, refine the arithmetic bounds.

A positive parent lower bound alone does not force either separately computed child lower bound to be positive. For example, $\ell=1$ and a left interval $[-1,2]$ are insufficient. Treating such a case as a negative child result would be an error.

**Proposition 2.** If $b-a<\ell$, one of the two selection rules succeeds.

**Proof.** If $a>0$, select left. Otherwise $b=a+(b-a)<\ell$, so $\ell-b>0$ and right is certified. $\square$

This uses the shared parent information rather than unrelated estimates for both children.

### 4. Rational spacing and its cost

If the values $P(c)$ all lie in $q^{-1}\mathbb Z$, every subset score lies on that same grid. An interval of width strictly less than $1/q$ contains at most one grid value, so a valid such interval determines the score exactly.

For a paired-root polynomial, its integer normalization denominator provides a safe $q$. Positive exact scores are then at least $1/q$. The observation guarantees a finite precision target for an exact arithmetic procedure; it does not show that this target is cheap to attain.

For a large family, an absolute error below $1/q$ can mean an extremely small relative error in a normalized moment estimate. The localization theorem cannot be used to hide that requirement. Validity of the score calculation remains the hard input.

### 5. An actual arithmetic example

The recorded AP-7 family has 960 fully covered rough candidates and quintic score $1069/15>0$. The complete tail-incidence stream contains 2005 distinct term defects. Prefix sums of the actual rational candidate scores provide an exact oracle for this small example.

Localization uses ten oracle calls including the initial score and reaches

$$a=47,\qquad d=210,$$

with terms

$$47,257,467,677,887,1097,1307.$$

All seven terms are independently checked by SymPy. The query trace, including positive parent and selected-child scores, is stored in [gap-checks.json](../../results/gap-checks.json).

The prefix sums were constructed from an explicit enumeration. This check therefore validates localization and its coverage contract; it does not demonstrate an inexpensive oracle for a large implicit family.

### 6. Final verification and the remaining goal

Once an AP-28 singleton were located, its 28 terms would still be verified independently, with the common difference and the full primality-test domain checked. Below $2^{64}$, the first twelve prime bases provide a deterministic Miller–Rabin test [1]. A witness beyond that range needs an appropriately certified primality method instead of extending the finite-range claim.

This paper closes the logical step from a valid finite positive certificate and score oracle to an explicit point. It does not provide the missing positive AP-28 certificate. No AP-28 witness has been obtained by this localization check.

### Reproduction and references

`research/witness_localization.py` implements exact bisection and interval child selection. `research/run_gap_checks.py` supplies the completely covered AP-7 family and independently verifies the returned progression. The localization proof uses only finite additivity and bisection; no novelty claim is made for those tools.

1. Sorenson, J., and Webster, J. (2017). *Strong pseudoprimes to twelve prime bases*. [Author preprint](https://arxiv.org/abs/1509.00864).
2. The admissible minorants and their arithmetic interpretation are developed in [the completion paper](../../paper_ap28_completion.md) and [the coupled-bounds paper](../../paper_ap28_coupled_bounds.md).
