# Signed Tail Aggregation Without Prime-Label Tuples

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Gap G2:** The aggregation algebra is resolved for an explicitly covered finite family. Efficient complete AP-28 candidate generation and a positive AP-28 arithmetic bound remain open.

### Abstract

Expanding a fifth defect moment over five tail-prime labels creates an unnecessary combinatorial burden once the finite candidate family is explicit. We aggregate verified composite incidences by candidate and term, update every required moment by Pascal's identity, and preserve the signed polynomial score directly. Boolean union, rather than an additive prime-label count within each term, also removes the cube-root sieve-depth assumption from finite classification. A monotonicity lemma shows that discarding any verified composite candidate improves every admissible prime-completion minorant. These are exact finite reductions. They do not bound the cost of generating a complete candidate family or its incidence stream.

### 1. Composite incidences form a finite coverage problem

Let $\mathcal R=\{x_1,\ldots,x_R\}$ be a completely specified candidate family, with $k$ terms per candidate, all in $(B,X]$ and free of prime divisors at most $B$.

For every prime $B<q\le\sqrt X$, record an event $(i,j,q)$ when

$$q\mid L_j(x_i),\qquad q^2\le L_j(x_i).$$

A prime term has no event. Every composite term has at least one, because its least prime divisor exceeds $B$ and is at most its square root. Consequently

$$e_{i,j}=1_{\{L_j(x_i)\text{ composite}\}}
=\bigvee_q1_{\{(i,j,q)\text{ is an event}\}}.$$

The operator is Boolean OR. If terms are not restricted to prime or semiprime, replacing OR by the sum of labels is incorrect. For example, $105$ has labels $3,5,7$ below its square root, but represents one composite term.

This proves that the condition $B^3>X$ is unnecessary for **finite Boolean classification**. It was needed for the earlier additive least-prime-factor identity, not for exact verification itself. Complete coverage of the tail-prime range, or an independently valid primality decision for every uncovered term, is still required.

### 2. Aggregate first, without expanding prime tuples

Maintain a $k$-bit mask for each candidate. A verified event sets its term bit. Duplicate events leave the mask unchanged. Let $c$ be the number of set bits before a newly discovered composite term.

Pascal's identity gives, for $r\ge1$,

$$\binom{c+1}{r}-\binom cr=\binom c{r-1}.$$

Therefore all moments through fixed order $s$ can be updated with at most $s$ additions per new term defect. Starting from $M_0=R$, $M_r=0$ for $r>0$, the result is exactly

$$M_r=\sum_i\binom{C(x_i)}r.$$

For a minorant $P(c)=\sum_{r=0}^sb_r\binom cr$, maintain the signed score directly:

$$S=\sum_iP(C(x_i)),\qquad
\Delta S=P(c+1)-P(c).$$

No sum over ordered or unordered prime-label $s$-tuples is evaluated.

At fixed progression length, if a supplied stream contains $E$ events, it needs $O(E)$ membership/deduplication work and at most $kR$ successful term updates. For fixed $s$, the moment updates use $O(skR)$ arithmetic operations after event generation. The masks use $O(kR)$ bits, apart from bookkeeping. These are processing bounds **given the stream**, not bounds for producing it.

The generating-function interpretation is

$$H(z)=\sum_i z^{C(x_i)},\qquad M_r=H^{(r)}(1)/r!.$$

Evaluating the polynomial functional after aggregating the defect states preserves cancellation that separate absolute bounds on the expanded prime-label sums may destroy.

### 3. Positive pruning

**Proposition 1.** Suppose $P(0)=1$ and $P(c)\le0$ at every positive integer. Removing any set $\mathcal F$ of verified composite candidates preserves all prime progressions and cannot decrease the score:

$$S(\mathcal R\setminus\mathcal F)
=S(\mathcal R)-\sum_{x\in\mathcal F}P(C(x))\ge S(\mathcal R).$$

**Proof.** No zero-defect point is removed, and each removed score is nonpositive. $\square$

Once every composite candidate has been removed, the score equals the exact number of prime progressions. This is a purification identity, not a new source of prime density.

The union of candidates hit by any verified composite event is also sufficient for exact counting after complete tail coverage:

$$N_k=R-\left|\bigcup_{j,q}\{i:(i,j,q)\text{ is an event}\}\right|.$$

At that stage moment bounds are optional. Their potential advantage lies in certifying a large implicit family without visiting every candidate, and that harder advantage is not established here.

### 4. Actual arithmetic check

Use the AP-7 family from the third paper: $D=210$, $B=29$, $X=20000$, $1\le m\le10$, and every $a>B$ with $a+6Dm\le X$ whose terms are $B$-rough.

Complete enumeration produces:

| Quantity | Exact value |
|---|---:|
| Rough candidates $R$ | 960 |
| Distinct composite-term incidences | 2005 |
| Candidates hit by at least one incidence | 882 |
| Zero-defect candidates | 78 |
| Quintic score before pruning | $1069/15$ |
| Score after all verified composite candidates are removed | 78 |

The streaming moments are $(960,2005,1772,874,281,66)$ through order five, agreeing with independent direct classification. Duplicate events are explicitly tested and do not alter the result.

For a nonsemiprime check, the two AP-3 candidates $(97,103,109)$ and $(105,111,117)$ are both 2-rough. Boolean coverage correctly gives one prime progression even though the second candidate has more than one tail label for its first term. No cube-root depth assumption is used.

### 5. The arithmetic gap that remains

A valid AP-28 application needs a completely covered candidate family, or a valid bound for the uncovered portion. Neither a truncated incidence stream nor an unvisited residue cell is a certified negative result.

The number of **true** incidences does not bound the work needed to discover them. Testing enormous numbers of candidate–prime nonincidences can still dominate. Generating all rough candidates can also dominate. Prime-pattern algorithms address precisely these kinds of organization costs [1].

Thus the prime-label tuple expansion is avoidable in an explicit finite search, but the central AP-28 arithmetic/efficiency gap is not closed. No positive AP-28 score or complete feasible AP-28 coverage is supplied.

### Reproduction and references

`research/signed_tail_aggregation.py` maintains masks, moments, and signed scores. `research/run_gap_checks.py` checks complete coverage on the stated AP-7 family and records the results in [gap-checks.json](../../results/gap-checks.json).

1. Sorenson, J. P., and Webster, J. (2020). *Two algorithms to find primes in patterns*. [Author preprint](https://arxiv.org/abs/1807.08777).
2. [From Local Admissibility to Prime Completion](../../paper_ap28_completion.md) supplies the defect minorants. This note specializes elementary Boolean union and Pascal identities; it makes no novelty claim for those tools.
