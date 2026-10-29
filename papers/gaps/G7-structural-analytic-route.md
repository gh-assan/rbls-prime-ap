# A Structural Analytic Route to AP-28

**Author:** Ghassan Al Hamoud

**Date:** 29 October 2026

**Status:** Mathematical research note. No explicit AP-28 construction is obtained. The prime-correlation theorems cited below are established work, not new results of this project.

### Abstract

The required discovery method must derive an AP-28 from mathematical structure. Enumerating more starts, differences, CRT cells, or tail labels does not meet that requirement. We formulate a finite analytic certificate using an actual von Mangoldt correlation and an explicit correction for prime powers. Existing quantitative results imply that this certificate eventually succeeds at sufficiently large heights, but the present note does not supply numerical constants or recover a pair of integers. We also prove a finite-size obstruction to a tempting shortcut: at a 64-bit term height, a direct global $U^{27}$-norm error certificate requires almost pointwise knowledge of primality. Higher-order Fourier analysis remains relevant, but this blunt certificate cannot supply the missing construction.

### 1. The mathematical target

An explicit construction must output integers $a>1$ and $d>0$, together with a proof that

$$a,a+d,\ldots,a+27d$$

are prime. A probabilistic score, a prime-density model, and a statement that sufficiently large progressions exist have different conclusions. None supplies these integers by itself.

Green and Tao proved that prime progressions of every length exist [1]. Thus the new research target is a usable construction or a quantitative argument that also recovers a witness. Repeating their existence conclusion would not settle this target.

The following argument works with the full two-variable cone. It does not assume the cube-root roughness conditions or multiplier cap used in the earlier moment papers. A theorem for this cone cannot silently be substituted for a theorem about those selected families.

### 2. A finite analytic certificate with the prime-power correction included

Fix

$$D=223092870,\qquad W=27D.$$

For $X\ge W+2$, define

$$\Omega_X=\{(a,m)\in\mathbb R^2:a\ge2,\ m\ge1,\ a+Wm\le X\}.$$

Its area is exactly

$$V(X)=\frac{(X-2-W)^2}{2W}.$$

Let $\Lambda(n)$ be the von Mangoldt function, with value $\log p$ at every prime power $p^e$, and zero otherwise. Consider the **actual arithmetic sum**

$$T(X)=\sum_{(a,m)\in\Omega_X\cap\mathbb Z^2}
       \prod_{j=0}^{27}\Lambda(a+jDm).$$

The local constant for these forms is

$$\beta_D=\prod_p\beta_p,\qquad
\beta_p=\begin{cases}
(1-1/p)^{-27},&p\mid D,\\
(1-27/p)(1-1/p)^{-27},&p\nmid D.
\end{cases}$$

The earlier [Euler-product note](G3-euler-product-errors.md) supplies the rigorous lower bound

$$\beta_D\ge\beta_L=3.312948771602789797972\times10^{18}.$$

Suppose an arithmetic argument proves

$$|T(X)-V(X)\beta_D|\le E(X).\tag{1}$$

This assumption concerns a finite prime correlation. It is substantially stronger than bounding the tail of the Euler product.

A positive $T(X)$ alone could count prime powers. To remove them, set

$$M(X)=\left\lfloor\frac{X-2}{W}\right\rfloor,\qquad
K(X)=\lfloor\log_2X\rfloor,$$

and

$$S(X)=(K(X)-1)\lfloor\sqrt X\rfloor.$$

There are at most $S(X)$ proper prime-power values at most $X$. Indeed, sum over exponents $2\le e\le K(X)$ and overcount their possible bases by $\lfloor\sqrt X\rfloor$ for each exponent. For a fixed term index $j$ and value $n$, each multiplier $m$ determines at most one start $a=n-jDm$. There are at most $M(X)$ such multipliers in the cone.

Consequently, tuples containing a proper prime power in at least one position contribute at most

$$B_{\rm pp}(X)=28M(X)S(X)(\log X)^{28}\tag{2}$$

to $T(X)$. This is a coarse upper bound, but it is unconditional and finite.

**Proposition 1.** If (1) is proved and

$$V(X)\beta_L-E(X)-B_{\rm pp}(X)>0,\tag{3}$$

then an AP-28 with difference divisible by $D$ exists below $X$.

**Proof.** The arithmetic sum exceeds the total possible weight of all tuples containing a proper prime power. Its remaining positive contribution must come from a tuple with every term prime. The condition $m\ge1$ excludes a constant progression. $\square$

This is an analytic sufficient condition. It does not evaluate $T(X)$ by enumerating progressions. However, this note has not proved a numerical $E(X)$ that makes (3) positive at an explicit useful height. The deliberately coarse prime-power correction can also require improvement.

### 3. What published prime-correlation theorems actually provide

Tao and Teräväinen [2, Theorem 1.6] establish, for fixed finite-complexity systems, an error of the form

$$E(X)\le C_D X^2(\log\log X)^{-c_D}$$

for sufficiently large $X$, with effective constants. Our coefficient vectors $(1,jD)$ are pairwise nonproportional, so their theorem applies to this fixed system and convex cone. Their Example 1.7 also treats prime arithmetic progressions directly.

Here $V(X)/X^2\to1/(2W)$, while $B_{\rm pp}(X)/X^2\to0$. Thus (3) eventually holds. This specializes an established analytic existence theorem; it does not give a new AP-28 discovery.

Leng [3, Theorem 5] subsequently obtains stronger logarithmic savings for linear equations in primes. Its stated implied constant is ineffective because of Siegel's theorem. This stronger rate therefore cannot simply replace the effective bound above in a numerical certificate. Choosing a large logarithmic exponent does not justify assigning the unknown constant the value one or assuming the asymptotic regime begins below $2^{64}$.

A practical application needs actual admissible constants, a verified height, and a constructive recovery argument. None is supplied by the displayed asymptotic notation alone.

### 4. A finite-size obstruction to the simplest Fourier shortcut

For a finite abelian group $G$ of size $N$, use normalized averages in the Gowers norm:

$$\|h\|_{U^s}^{2^s}
=\mathbb E_{x,t_1,\ldots,t_s}
  \prod_{\omega\in\{0,1\}^s}\mathcal C^{|\omega|}
  h(x+\omega\cdot t).$$

Here $\mathcal C$ denotes complex conjugation. The following elementary lower bound is decisive at finite sizes.

**Proposition 2.** For $s\ge2$ and every $h:G\to\mathbb C$,

$$\|h\|_{U^s}\ge N^{-(s+1)/2^s}\|h\|_\infty.\tag{4}$$

**Proof.** In the recursive norm identity, each summand
$\|\Delta_t h\|_{U^{s-1}}^{2^{s-1}}$ is nonnegative. Retain $t=0$, where $\Delta_0h=|h|^2$. Every cube product for this nonnegative function is nonnegative. Retain the cube with all remaining increments zero and base point $x_0$ maximizing $|h|$. Its contribution gives

$$\|h\|_{U^s}^{2^s}
\ge N^{-1}\||h|^2\|_{U^{s-1}}^{2^{s-1}}
\ge N^{-(s+1)}|h(x_0)|^{2^s}.$$

Taking the $2^s$-th root proves (4). A function supported at one point attains equality, so the comparison is sharp for arbitrary functions. $\square$

If $N\le2^{66}$ and $s=27$, then

$$N^{-28/2^{27}}
\ge1-\frac{66\cdot28}{2^{27}}
=\frac{16776985}{16777216}
>\frac{49999}{50000}.\tag{5}$$

We used $e^{-u}\ge1-u$ and $\log2<1$. In this range, the normalized $U^{27}$ norm cannot be much smaller than the largest pointwise error.

To see the consequence, choose a prime $P>2X$ with $P<4X$. For $X\le2^{64}-1$, this gives $P<2^{66}$. Let $f$ on $\mathbb F_P$ indicate the ordinary primes in $[2,X]$, and let $g:\mathbb F_P\to[0,1]$ be a proposed model. Write

$$\mathcal A_{28}(u_0,\ldots,u_{27})
=\mathbb E_{a,d\in\mathbb F_P}\prod_{j=0}^{27}u_j(a+jd).$$

The standard generalized von Neumann inequality [4, Theorem 2.2] and telescoping give

$$|\mathcal A_{28}(f,\ldots,f)-\mathcal A_{28}(g,\ldots,g)|
\le28\|f-g\|_{U^{27}}.\tag{6}$$

Suppose a certificate uses an upper bound $\epsilon\ge\|f-g\|_{U^{27}}$ in (6). Because $\mathcal A_{28}(g,\ldots,g)\le1$, even a positive lower bound requires $\epsilon<1/28$. Equations (4)-(5) then force

$$\|f-g\|_\infty<\frac{50000}{28\cdot49999}<0.036.\tag{7}$$

In particular, thresholding $g$ at $1/2$ already recovers $f$ at every point. A cheap local-density model that differs substantially from the prime indicator somewhere cannot pass this certificate at this height.

The constant-density version fails even more directly. If $g=\delta=\mathbb Ef$, telescoping improves the factor 28 to $1+\delta+\cdots+\delta^{27}$. But $\delta<1/2$, $\|f-\delta\|_\infty\ge1/2$, and therefore its norm error exceeds $0.49999$, while its main term is at most $2^{-28}$.

For an integer witness, the constant progressions must also be removed. Since $P>2X$, any nonconstant cyclic progression entirely supported in $[2,X]$ lifts to an ordinary increasing or decreasing progression: all adjacent integer differences lie in an interval of length less than $P$ and are congruent modulo $P$, so they are equal. Thus the number of increasing integer AP-28s is exactly

$$\frac{P^2\mathcal A_{28}(f,\ldots,f)-\pi(X)}2.$$

Subtracting this diagonal only strengthens the requirement on the error certificate.

**Scope.** This obstruction concerns the normalized global norm and the crude error conversion (6). It does not rule out relative transference, structured decompositions, cancellation in the specific AP correlation, or another algebraic construction. Passing to a vastly larger ambient group changes the numerical bound, but its normalization and boundary costs must then be retained.

### 5. Why lowering the uniformity order is not a general repair

There is an exact polynomial identity

$$\sum_{j=0}^{27}(-1)^j\binom{27}{j}(a+jd)^{26}=0.\tag{8}$$

It follows by applying a 27th finite difference to a degree-26 polynomial. Over $\mathbb F_p$, $p>27$, set

$$h_j(x)=\exp\!\left(\frac{2\pi i}{p}
            (-1)^j\binom{27}{j}x^{26}\right).$$

Equation (8) gives $\mathcal A_{28}(h_0,\ldots,h_{27})=1$. Nevertheless,

$$\|h_j\|_{U^{26}}^{2^{26}}
=1-(1-1/p)^{25}\longrightarrow0.$$

For the norm formula, 26 differences leave a nonzero multiple of $t_1\cdots t_{26}$. Averaging over the last increment gives zero unless one of the preceding 25 increments is zero. All relevant coefficients are nonzero because $p>27$.

Thus there is no general mixed-correlation theorem replacing $U^{27}$ control by arbitrarily small $U^{26}$ control for these 28 forms. This is an abstract complex-function obstruction, not a construction of primes or a claim about every specialized prime argument.

The same issue appears algebraically. For $0\le r\le27$, the powers $(a+jd)^r$, $0\le j\le27$, span a space of rank $r+1$ in characteristic greater than 27. Rank first reaches 28 at $r=27$. Additional parameter coordinates that leave these forms unchanged do not remove this dependency.

### 6. The construction still needed

The useful direction is a structured prime-correlation argument that retains the small-prime factors and bounds the remaining AP-specific contribution. It must do both of the following:

1. Prove a positive finite arithmetic bound, with all numerical errors and prime-power terms controlled. Proposition 1 gives one precise sufficient condition.
2. Derive the actual pair from the structure producing that bound, with justified recovery cost. A global asymptotic count alone does not provide this map. The earlier localization lemma is useful only once its arithmetic oracle is supplied.

Those tasks remain open here. The present note excludes one inadequate Fourier certificate and supplies a rigorous analytic target. It does not turn a density heuristic into a construction, and it does not close G2 or the finite-height parts of G3b/G5.

### Verification and references

`research/analytic_ap28_certificates.py` checks exact constants and algebra. `tests/test_analytic_ap28_certificates.py` independently checks the finite-difference relation, the Vandermonde rank transition, the finite-size constants, exact small-group norm inequalities including the equality case, and the proper-power overcount. These are proof checks, not an AP discovery search.

1. Green, B., and Tao, T. *The primes contain arbitrarily long arithmetic progressions*. [Annals of Mathematics](https://annals.math.princeton.edu/2008/167-2/p03).
2. Tao, T., and Teräväinen, J. *Quantitative bounds for Gowers uniformity of the Möbius and von Mangoldt functions*. [Primary paper, Theorem 1.6, Example 1.7, and Section 3](https://arxiv.org/html/2107.02158v4). Published in JEMS 27 (2025).
3. Leng, J. *Efficient Equidistribution of Nilsequences*. [Primary paper](https://arxiv.org/html/2312.10772v5). Theorem 5 gives the linear-prime-pattern application.
4. Gowers, W. T., and Wolf, J. *The true complexity of a system of linear equations*. [Primary paper](https://arxiv.org/pdf/0711.0185). Theorem 2.2 supplies the standard bounded-function AP estimate used in (6).
