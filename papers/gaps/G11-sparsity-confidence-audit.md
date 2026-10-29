# A Sparsity and Confidence Audit of the AP-28 Route

**Author:** Ghassan Al Hamoud

**Date:** 29 October 2026

**Status:** A necessary support bound and a continuous-model enclosure are proved. No positive finite arithmetic bound or explicit AP-28 is obtained.

### Abstract

Closing technical subproblems does not by itself show that an AP-28 construction is approaching. We audit the current route in two ways. First, even the one-sided uniform character criterion requires at least 11 occupied quadratic quotient classes of nonzero von Mangoldt tuple weight. This strengthens the earlier singleton limitation without assuming absolute correlation bounds. Second, outward-rounded integration encloses a defined density-model main term at the full 64-bit height. The selected family's model term lies between 1.129 and 1.181; the unrestricted $23\#$-difference model lies between 13.270 and 13.876. Selecting the current family retains at most 8.51% of that model term. These are rigorous statements about a support constraint and a model integral, not a count of actual prime progressions. They support confidence in the checked finite calculations and caution about the present uniform-mixing route to an explicit witness.

### 1. What would demonstrate progress toward the construction

The current series has supplied exact finite identities, counterexamples to inadequate assumptions, and an optimal modular minorant. It has not supplied a numerical bound for the actual 28-term prime correlation that makes the certificate positive. It has also not supplied a mathematical rule producing the pair $(a,d)$.

There is progress in understanding the problem and in eliminating invalid proof steps. The evidence does not justify a completion percentage for the AP-28 construction. A valid positive arithmetic certificate, or an actual mathematically derived and verified progression, would change that assessment.

This audit does not optimize the residue minorant again: [the tenth paper](G10-sharp-character-threshold.md) already settled that question for the fixed residue conditions.

### 2. One-sided uniform bounds also require support

Recall the quadratic quotient

$$G/B_2\cong(\mathbb F_2)^7,$$

and the exact character threshold

$$\rho=\frac{693733}{6015973}.$$

Suppose the full von Mangoldt tuple sum $T_0$ is positive. Normalize its nonnegative weights and push them onto this quotient. Let $J$ be the number of occupied quotient points. A nonprincipal quadratic character takes the form $(-1)^{u\cdot x}$, with nonzero $u\in(\mathbb F_2)^7$.

**Proposition 1.** For a probability measure on $(\mathbb F_2)^r$ supported on $J$ points, if $J\le r-1$, some nonprincipal character has mean one. If $J\ge r-1$, some nonprincipal character has mean at least

$$\frac{2(r-1)}J-1.$$

**Proof.** For $J\le r-1$, the support spans a proper linear subspace. A nonzero linear functional annihilates it, so its character is one on the full support.

Otherwise choose the $r-1$ heaviest support points. Their total mass is at least $(r-1)/J$. They span a subspace of dimension at most $r-1$, so a nonprincipal character equals one on all of them. On the remaining mass its value is at least minus one. Its mean is therefore at least $2(r-1)/J-1$. $\square$

For the current $r=7$, the one-sided uniform requirement

$$\operatorname{Re}(T_\chi/T_0)<\rho$$

for every nonprincipal quadratic character forces

$$J>\frac{12}{1+\rho}=\frac{36095838}{3354853},$$

so **at least 11 quotient classes must be occupied**.

The earlier absolute-error argument required at least 48 occupied classes. Proposition 1 shows that merely replacing absolute bounds by uniform one-sided bounds does not solve sparse localization. A phase-aware weighted aggregate can retain information that either uniform bound loses.

The occupied classes here carry tuples for which every von Mangoldt factor is nonzero. Outside the selected power-exclusion family those terms may be proper prime powers. This is not a claim that 11 AP-28s exist, nor an upper bound on how many such tuples occur.

### 3. Define the continuous model being assessed

Let

$$D=223092870,\quad M=7D,\quad H=2^{64}-1,\quad
\alpha=\frac{1651}{2772}.$$

For a difference unit $E$, define

$$I_E(X)=\int_{\substack{a\ge2,\ m\ge1\\a+27Em\le X}}
             \prod_{j=0}^{27}\frac1{\log(a+jEm)}\,da\,dm.$$

The model main terms in this audit are

$$\mathcal M_D=\beta_D I_D(H),\qquad
\mathcal M_M=\beta_D I_M(H),\qquad
\mathcal M_R=\alpha\beta_D I_M(H).$$

The same Euler product $\beta_D$ applies because $D$ and $M$ have the same prime divisors. The earlier rigorous enclosure for this constant is reused.

The linear-prime-pattern framework motivates such main terms [1]. Here they are explicitly defined continuous quantities. No theorem bounding the difference between these quantities and the actual finite prime counts is assumed. The values also do not supply the weighted error quantities $E_0$ and $\epsilon$ in the existing certificate.

### 4. A model-yield cost that follows without numerical integration

Change variables from $m$ to the actual difference $d=Em$. Then

$$I_E(X)=\frac1E\int_{\substack{a\ge2,\ d\ge E\\a+27d\le X}}
                     \prod_{j=0}^{27}\frac1{\log(a+jd)}\,da\,dd.$$

The $M$-domain is a subset of the $D$-domain and $M=7D$, giving

$$I_M(X)\le\frac17 I_D(X).$$

Therefore

$$\frac{\mathcal M_R}{\mathcal M_D}\le\frac\alpha7
=\frac{1651}{19404}<0.0851.$$

The selected family retains at most 8.51% of the baseline model term. Adding the extra power of 7 to the difference produces no compensating Euler-factor gain. Selecting safe start residues reduces it further.

This is a cost in the defined model, not a theorem about the fraction of actual AP-28s discarded. Eliminating prime powers simplified the proof conditions but has not demonstrated a net gain toward finding a progression.

### 5. Rigorous enclosure of the model integral

Put $W=27M$ and $b=Wm$. Then

$$I_M(H)=\frac1W\int_{\substack{a\ge2,\ b\ge W\\a+b\le H}}
 f(a,b)\,da\,db,\qquad
f(a,b)=\prod_{j=0}^{27}\frac1{\log(a+jb/27)}.$$

The function $f$ is positive and nonincreasing in each coordinate. For a rectangle $[a_0,a_1]\times[b_0,b_1]$, its intersection with the triangle has exact doubled area

$$A_2=(H-a_0-b_0)_+^2-(H-a_1-b_0)_+^2
     -(H-a_0-b_1)_+^2+(H-a_1-b_1)_+^2.$$

The cell's integral contribution is enclosed by

$$\frac{A_2}{2W}f(a_1,b_1)
\ \le\ \text{cell contribution}\ \le\
\frac{A_2}{2W}f(a_0,b_0).$$

The upper corner may lie outside the triangle; coordinate monotonicity still makes it a valid lower bound. Dyadic rectangles cover the containing rectangle, and adaptive bisection tightens the largest interval contributions. Every area is calculated with exact integers.

The implementation encloses each logarithm before multiplying or dividing. Python Decimal's natural logarithm is correctly rounded [2]; the adjacent representable numbers enclose its exact value. Directed rounding is then used for interval differences, products, reciprocals, and sums. Tests independently verify logarithm enclosures using rational bounds from the atanh series, rather than another call to the same logarithm routine.

For the $D$-model, the strip $D\le d<M$ contributes a nonnegative correction to $7I_M(H)$. It is bounded above by

$$6\int_2^H f(a,27D)\,da,$$

which is enclosed from above by a one-dimensional monotone sum. This gives a rigorous baseline enclosure without a second two-dimensional integration.

With 8,000 active rectangles and 28-digit outward arithmetic, the results are:

| Defined model term | Lower enclosure | Upper enclosure |
|---|---:|---:|
| Unrestricted $D$ differences, $\mathcal M_D$ | 13.2708983665667183 | 13.8758398361444122 |
| Unrestricted $M$ differences, $\mathcal M_M$ | 1.89584262379524548 | 1.98226281580813542 |
| Selected $M$ family, $\mathcal M_R$ | 1.12916167816953473 | 1.18063344476884256 |

**These enclosures are for a model integral. They are not enclosures for the actual number of prime progressions and are not success probabilities.**

### 6. What the comparison tells us

The selected model term is only of order one at the maximum supported height. Meanwhile the uniform one-sided character route needs at least 11 occupied quadratic classes of positive von Mangoldt tuple weight. This comparison is a warning about the strategy, not a contradiction: the model's finite error is unproved, and the unselected weighted tuple count can include proper prime powers.

A model predicting a few progressions provides weak motivation for trying to prove broad equidistribution before recovering a single one. A more suitable target is an arithmetic estimate for the actual signed score that retains phase and nonuniform information, or a different direct mathematical construction.

### 7. Confidence and remaining work

Confidence in the checked finite algebra and numerical enclosures is high, subject to ordinary mathematical review. The proofs and independent checks support those stated scopes. They do not establish novelty or replace external peer review.

Confidence that the current uniform-mixing route will yield an explicit AP-28 is low. It still lacks its central arithmetic bound, its own model yield is small, and even the one-sided version has a sparsity obstruction. There is no calibrated percentage for eventual success or a defensible completion percentage for the project.

The series is making progress in understanding and eliminating inadequate routes. It has not yet demonstrated a reliable mathematical route to the requested witness. The independently enclosed model term closes one numerical substep at this height; G2, the actual finite discrepancy in G3b/G5, and witness recovery remain open.

### 8. A simpler working target for the next arithmetic argument

The power-free residue family can remain an auxiliary certificate. The main working target should also retain the full $D$-difference family and use the prime-only weight

$$\vartheta_*(n)=\mu(n)^2\Lambda(n)
=\begin{cases}\log n,&n\text{ prime},\\0,&n\text{ composite},\end{cases}\qquad n\ge2.$$

Here $\mu$ is the Möbius function. The identity follows directly: a proper prime power has $\mu^2=0$, and a composite with at least two distinct prime factors has $\Lambda=0$.

The exact sum

$$C_D(X)=\sum_{\substack{a\ge2,m\ge1\\a+27Dm\le X}}
              \prod_{j=0}^{27}\vartheta_*(a+jDm)$$

is positive exactly when that full family contains an AP-28. It incurs neither the selected-family model loss nor a separate prime-power subtraction. Its analytic finite lower bound is still missing. Defining this weight does not make its evaluation easy, supply a count oracle, or constitute a construction.

This identifies a simpler target for a new arithmetic argument while keeping the proved subgroup results available. No existing correlation theorem is assumed to transfer to this finite prime-only sum with a sufficient numerical error without a proof.

### Verification and references

Run `python3 -m research.archimedean_enclosure` to reproduce [the enclosures and support requirement](../../results/archimedean-enclosure-checks.json). The tests check exact clipped areas, partition additivity, independent logarithm bounds, outward products, refinement nesting, and weighted quadratic-character examples. The numerical work integrates a continuous function; it does not enumerate progression candidates.

1. Tao, T., and Teräväinen, J. [Quantitative bounds for Gowers uniformity of the Möbius and von Mangoldt functions](https://arxiv.org/html/2107.02158v4), Theorem 1.6 and Example 1.7. Their asymptotic framework does not certify the finite model error used here.
2. Python 3.9 documentation, [Decimal arithmetic and correctly rounded logarithms](https://docs.python.org/3.9/library/decimal.html).
