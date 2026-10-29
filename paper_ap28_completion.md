# From Local Admissibility to Prime Completion

## Semiprime defects and finite certificates for AP-28

**Author:** Ghassan Al Hamoud  
**Series:** Follow-up to *A Projective Lattice Approach to Prime Arithmetic Progressions*  
**Status:** Mathematical research note. The finite certificate below is proved; a positive certificate for an actual AP-28 region is not established.

### Abstract

The projective-lattice formulation constructs arithmetic progressions without selected small prime factors, but does not establish that all 28 terms can be made prime within a feasible search budget. We develop a precise bridge between these two statements. In a bounded family with terms at most $X$, sieving beyond $X^{1/3}$ leaves each term either prime or semiprime. The number of composite terms becomes a bounded defect variable. We express its binomial moments through least-prime-factor incidences and derive finite polynomial certificates for a positive number of zero-defect progressions. An explicit degree-five minorant uses only five nontrivial moments and can succeed where the degree-five Bonferroni bound fails. Its proof is exact and does not assume independent primality. We verify the arithmetic identities on an AP-5 family and calibrate the certificate separately in a 28-event probability model. We also quantify the tradeoff between sieve depth and moment complexity and estimate the total two-variable search volume required by a prime-tuple model. The remaining arithmetic problem is explicit: establish sufficiently sharp, signed moment bounds for a real AP-28 family. This paper does not supply those bounds or an AP-28 witness.

### 1. The statement that must be proved

Let

$$D=23\#=223092870,\qquad L_j(a,m)=a+jDm,\quad 0\le j<28.$$

The earlier paper gives exact congruence lattices containing locally admissible pairs $(a,m)$. It leaves open whether those pairs can be organized so that simultaneous primality is attainable with practical resources.

There are two different gaps:

1. **Certification:** What finite statement would force at least one candidate to have all 28 terms prime?
2. **Arithmetic control:** Can that statement be established for an actual candidate family without already performing an infeasible search?

We give an exact answer to the first and a concrete formulation of the second. Replacing the second by an independence assumption would not solve the original problem.

The combination is sieve theory, finite probability, integer polynomial optimization, and geometry of numbers. Polynomial moment bounds are established tools; Sibuya's treatment of discrete majorants and minorants is particularly relevant [1]. We make no claim that this framework or paired-root polynomials are new.

### 2. A finite setting with at most one defect per term

The following arguments apply to general length $k$. Assume $D$ contains every prime at most $k-1$. For AP-28, the stated $D$ has this property.

Fix integers $B,X$ with

$$B>k,\qquad B^3>X.$$

Let $\mathcal R$ be a finite, explicitly specified set of pairs satisfying

$$m\ge1,\qquad B<a,\qquad a+(k-1)Dm\le X,$$

$$\gcd(a,Dm)=1,$$

and suppose every $L_j$ is free of prime divisors at most $B$. Write $R=|\mathcal R|$.

The condition $a>B$ deliberately removes the small-prime boundary. An AP with a term equal to a sieving prime must be handled separately; this formulation does not claim to cover that boundary.

**Lemma 1 — prime or semiprime.** Every term in every pair in $\mathcal R$ is either prime or a product of exactly two primes, counting multiplicity.

**Proof.** Every prime factor exceeds $B$. Three prime factors would give a term exceeding $B^3>X$. Every term exceeds one. $\square$

**Lemma 2 — pairwise coprimality.** For each $(a,m)\in\mathcal R$, the $k$ terms are pairwise coprime.

**Proof.** Suppose a prime $p$ divides $L_i$ and $L_j$, $i<j$. Since $\gcd(L_i,Dm)=\gcd(a,Dm)=1$, the identity $L_j-L_i=(j-i)Dm$ implies $p\mid j-i$. Thus $p\le k-1$, so $p\mid D$, contradicting $\gcd(L_i,D)=1$. $\square$

Let $e_j(a,m)$ equal one when $L_j$ is composite and zero when it is prime. Define the defect count

$$C(a,m)=\sum_{j=0}^{k-1}e_j(a,m),\qquad 0\le C\le k.$$

The desired count is

$$N_k=\#\{(a,m)\in\mathcal R:C(a,m)=0\}.$$

If $\Omega(n)$ counts prime factors with multiplicity, Lemma 1 also gives the exact identity

$$C(a,m)=\Omega\!\left(\prod_jL_j(a,m)\right)-k.$$

This identity does not make $\Omega$ inexpensive to obtain. It identifies precisely what local admissibility has failed to decide.

### 3. Composite defects as exact divisibility incidences

For a prime $q>B$, put

$$E_{j,q}=\{(a,m)\in\mathcal R:q\mid L_j(a,m),\ q^2\le L_j(a,m)\}.$$

Only $q\le\sqrt X$ can occur.

**Lemma 3 — unique tail label.** On $\mathcal R$,

$$e_j=\sum_{B<q\le\sqrt X\atop q\text{ prime}}1_{E_{j,q}}.$$

**Proof.** A composite term is $qr$ with primes $B<q\le r$. Exactly its smaller factor satisfies the displayed conditions. The square case is counted once. A prime term satisfies none of them. $\square$

Define binomial defect moments

$$M_r=\sum_{(a,m)\in\mathcal R}\binom{C(a,m)}r,\qquad M_0=R.$$

Expanding products of defect indicators gives

$$M_r=\sum_{0\le j_1<\cdots<j_r<k}
\ \sum_{B<q_1,\ldots,q_r\le\sqrt X\atop q_\ell\text{ prime}}
\left|\bigcap_{\ell=1}^rE_{j_\ell,q_\ell}\right|.$$

By Lemma 2, intersections with equal $q$ labels at distinct positions are empty. The expression can therefore be restricted to pairwise distinct $q_\ell$.

This is a finite identity, not an asymptotic. It translates the primality gap into counts of congruence-lattice points with additional linear inequalities. Counting those incidences accurately is substantial arithmetic work; the identity does not remove it.

### 4. A polynomial certificate for complete primality

Let $P$ be a polynomial satisfying

$$P(0)=1,\qquad P(c)\le0\quad(c=1,\ldots,k).$$

Expand it in the binomial basis,

$$P(c)=\sum_{r=0}^s b_r\binom cr.$$

**Theorem 1 — finite completion certificate.** For every family $\mathcal R$ described above,

$$N_k\ge\sum_{r=0}^s b_rM_r.$$

In particular, a strictly positive right-hand side proves that $\mathcal R$ contains an AP-$k$ of primes.

**Proof.** Pointwise, $1_{\{C=0\}}\ge P(C)$. Sum over $\mathcal R$ and use the binomial expansion. $\square$

The theorem actually holds for any finite family with binary defect indicators; the semiprime assumptions are needed for the divisibility interpretation in Section 3, not for this polynomial inequality.

A useful explicit family is

$$P_{\mathbf r}(c)=(1-c)\prod_{r\in\mathbf r}
\frac{(c-r)(c-r-1)}{r(r+1)},$$

where every $r$ is a positive integer. For integer $c$, each paired factor is nonnegative. Consequently $P_{\mathbf r}(0)=1$ and $P_{\mathbf r}(c)\le0$ for every positive integer $c$. It is a valid minorant without any distributional assumption.

The root locations can be chosen to suppress the defect counts that would otherwise dominate a negative lower bound. This is a finite polynomial optimization problem, not a modification of the prime numbers.

### 5. An explicit five-moment condition for AP-28

Choose paired roots $(3,4)$ and $(7,8)$:

$$P(c)=\frac{(1-c)(c-3)(c-4)(c-7)(c-8)}{672}.$$

Exact finite differences give

$$P(c)=1-\binom c1+\frac{51}{56}\binom c2
-\frac{41}{56}\binom c3+\frac{13}{28}\binom c4
-\frac5{28}\binom c5.$$

Therefore an explicit sufficient condition is

$$\boxed{
R-M_1+\frac{51}{56}M_2-\frac{41}{56}M_3
+\frac{13}{28}M_4-\frac5{28}M_5>0.
}$$

This inequality, with *actual arithmetic moments or valid bounds for them*, would establish an AP-28 in the specified family. It is the main concrete target of the follow-up.

Bounds must have the correct direction: negative coefficients require upper bounds for the corresponding moments, while positive coefficients require lower bounds. Upper bounds for every incidence count alone are insufficient.

For $R>0$, write $\mu_r=M_r/R$. If estimates $\widehat\mu_r$ have certified errors $|\mu_r-\widehat\mu_r|\le\varepsilon_r$, then

$$\frac{N_k}{R}\ge\sum_{r=0}^5b_r\widehat\mu_r
-\sum_{r=0}^5|b_r|\varepsilon_r.$$

This explicitly states how accurate the arithmetic estimates must be. An observed fit to a model is not a certified error interval.

#### A calibration in a probability model

For 28 independent defect indicators with probability $1/10$, the normalized moments are

$$(\mu_0,\ldots,\mu_5)=
\left(1,\frac{14}5,\frac{189}{50},\frac{819}{250},
\frac{819}{400},\frac{2457}{2500}\right).$$

The displayed polynomial gives the exact lower bound

$$\frac{153}{8000}=0.019125,$$

whereas the ordinary degree-five Bonferroni expression gives

$$\sum_{r=0}^5(-1)^r\mu_r=-\frac{2313}{10000}.$$

The model's actual zero-defect probability is $(9/10)^{28}\approx0.0523348$. Thus choosing a different valid minorant can reduce the burden on a finite certificate. This calculation is **not evidence that these moments describe AP-28 candidates**.

Here $\sum|b_r|=30/7$. If all six normalized moment errors were bounded by a common $\varepsilon$, the same model-centered certificate would remain positive for $\varepsilon<0.0044625$. In practice $\mu_0=1$ is known exactly, so its error is zero.

### 6. An arithmetic verification at smaller progression length

The exact checker uses $k=5$, $D=30$, $B=20$, and $X=5000$, with

$$21\le a<2000,\qquad m\in\{1,2,3,4\}.$$

After the stated primitive-point and roughness conditions, the family contains 105 pairs. The independently checked defect histogram is

$$(n_0,n_1,n_2,n_3,n_4,n_5)=(47,44,10,4,0,0).$$

Its binomial moments are

$$(M_0,M_1,M_2,M_3,M_4,M_5)=(105,76,22,4,0,0).$$

The least-prime-factor incidence calculation reproduces those moments without using the primality classification. The polynomial

$$P(c)=\frac{(1-c)(c-2)(c-3)}6$$

gives $N_5\ge105-76+22-4=47$. Independent primality checks find exactly 47. Equality occurs here because this particular sample has no four- or five-defect candidates; it is not a general sharpness assertion.

One verified example is

$$29+120j,\qquad0\le j<5.$$

The example checks the bridge from divisibility incidences to a positive arithmetic certificate. It does not extrapolate that bridge's computational cost to AP-28.

### 7. How deep must the initial sieve go?

A crude certificate is $N_k\ge R-M_1$. Its weakness can be quantified.

For a single integer sampled up to $X$, the rough-number asymptotic uses Buchstab's function [2,3]. With $B=X^\theta$, $u=1/\theta$, and $1/3\le\theta\le1/2$, the limiting prime fraction among $B$-rough integers is

$$q(\theta)=\frac1{u\omega(u)}
=\frac1{1+\log(u-1)}.$$

One can also see this expression by counting primes and products $qr$ with $X^\theta<q\le r$ and $qr\le X$: the prime-number-theorem integral for the semiprimes has relative main term $\log((1-\theta)/\theta)$.

The single-integer asymptotic does not establish independent defects in an AP. Using independence only as a calibration gives:

| $\theta$ | Single-integer limiting prime fraction | Model mean defects in 28 terms | Model zero-defect fraction |
|---:|---:|---:|---:|
| $1/3$ | 0.5906 | 11.46 | $3.95\times10^{-7}$ |
| 0.40 | 0.7115 | 8.08 | $7.26\times10^{-5}$ |
| 0.45 | 0.8329 | 4.68 | 0.00597 |
| 0.48 | 0.9259 | 2.08 | 0.1158 |
| 0.49 | 0.9615 | 1.08 | 0.3334 |
| 0.495 | 0.9804 | 0.55 | 0.5744 |

Within this calibration, $R-M_1>0$ needs $q>27/28$, equivalently

$$\theta>\frac1{1+e^{1/27}}\approx0.490742.$$

Thus a first-moment argument asks for a sieve almost at the square-root boundary. This is a limitation of this model-based first-moment calculation, not a theorem prohibiting a more structured family.

The five-moment example with $q=0.9$ corresponds to $\theta=1/(1+e^{1/9})\approx0.472251$. It illustrates a tradeoff: shallower initial sieving may be compensated by stronger information about joint defects. It supplies no AP-28 moment bounds at that depth.

Deeper sieving also decreases the number of surviving candidates. In a fixed family whose possible prime terms exceed both sieve bounds, changing the bound removes composite candidates and preserves every prime progression. It raises purity, not the actual number of prime solutions.

### 8. Where the projective lattice enters the moment bounds

For one CRT cell from the earlier paper,

$$(a,m)=(Fu+cIv,Iv),\qquad u\in\mathbb Z,\quad v\ge1.$$

Let $A>B$ and $W=(k-1)D$. Before primitive-point and origin exclusions, the exact number of its points in $a\ge A$, $a+Wm\le X$ is

$$\sum_{v=1}^{\lfloor(X-A)/(WI)\rfloor}
\left[
\left\lfloor\frac{X-(W+c)Iv}{F}\right\rfloor
-\left\lceil\frac{A-cIv}{F}\right\rceil+1
\right]_+,$$

where $[t]_+=\max(t,0)$. This follows by solving the two inequalities for $u$. It includes negative basis coefficients; restricting $u$ to positive values would be incorrect.

A defect incidence adds

$$a+jDm\equiv0\pmod q,\qquad a+jDm\ge q^2.$$

When $q>B$ exceeds every prime used in the initial cell and does not divide $D$, reduction of the cell basis modulo $q$ is invertible. The extra nonzero linear equation has kernel of index $q$. Distinct prime labels therefore enlarge the lattice index by their product.

This identifies the geometric counting objects underlying $M_1,\ldots,M_5$. Origin and primitive-point exclusions must still be applied. The number of term-index sets alone reaches $\binom{28}{5}=98280$ at the fifth moment, before the prime labels are considered.

The valuable next estimate would be a signed, aggregate bound for these moments that avoids enumerating every prime-label combination. Replacing such a bound by the area divided by the lattice determinant would be unjustified for thin or poorly aligned regions.

### 9. The height budget also matters

The minimum span is $W=27D=6023507490$. Restricting all terms to size about $10^{15}$ leaves much less two-variable search volume than the phrase “a free difference” suggests.

For the continuous region

$$\mathcal T_X=\{(a,m):a\ge29,\ m\ge1,\ a+Wm\le X\},$$

its area is exactly

$$V_X=\frac{(X-29-W)^2}{2W}\quad(X>29+W).$$

This is an area, not an exact integer-point count. The elementary exact count of unrestricted integer pairs is $\sum_{m=1}^{\lfloor(X-29)/W\rfloor}(X-Wm-28)$ for integer $X$.

The two-variable local-factor product from the earlier paper, truncated at $100000$, is

$$\beta_{100000}\approx3.324621461\times10^{18}.$$

A prime-tuple **model count**, not a proved count, is

$$\mathcal H(X)=\beta_{100000}
\iint_{\mathcal T_X}\frac{da\,dm}{\prod_{j=0}^{27}\log(a+jDm)}.$$

A rougher proxy replaces every denominator by $\log X$. Numerical integration using the individual terms gives:

| Maximum term $X$ | Equal-log model proxy | Integrated model proxy |
|---:|---:|---:|
| $10^{15}$ | 0.0000233 | 0.0000557 |
| $10^{17}$ | 0.00702 | 0.0147 |
| $10^{18}$ | 0.142 | 0.283 |
| $2\times10^{18}$ | 0.356 | 0.701 |
| $5\times10^{18}$ | 1.22 | 2.36 |
| $2^{64}-1$ | 7.19 | 13.59 |

The integration uses an exact change of variables. With $H=X-29-W$,

$$a=29+Htz,\qquad m=1+Ht(1-z)/W,\qquad0<t,z<1,$$

and the Jacobian is $H^2t/W$. Orders 32, 64, 128, and 256 were compared. Their convergence is recorded, but is not a certified quadrature error bound. The truncated local product and finite-height extrapolation introduce separate, unquantified model errors.

This comparison suggests that the target height itself deserves reconsideration. Even the model assigns negligible mass to the whole $10^{15}$ triangle. Near the 64-bit limit it assigns appreciable mass, but the raw pair volume there is approximately $2.82\times10^{28}$. Neither model mass nor its integral is a discovery probability, an existence proof, or evidence that this volume can be searched feasibly.

Specialized AP search work already uses multidifference sieving and prime-tuple estimates [4,5]. Any efficiency claim must be compared with that work, not just with testing every raw pair.

### 10. A precise condition for the next mathematical advance

The unresolved step can now be stated as a single concrete task. Construct a nonempty, bounded, rough AP-28 family and establish signed bounds for its five defect moments that make

$$R-M_1+\frac{51}{56}M_2-\frac{41}{56}M_3
+\frac{13}{28}M_4-\frac5{28}M_5$$

strictly positive, with all error terms controlled.

There are two plausible routes within this formulation:

- obtain enough aggregate arithmetic control of the augmented lattice counts to certify positivity;
- construct a family with a demonstrably favorable defect distribution, then bound the same moments for that family.

The second route requires evidence beyond local avoidance and term-size effects. The first must confront the difficulty of high-order prime/semiprime correlations. General sieve parity obstructions explain why this is substantive; exact finite identities alone do not bypass them [6].

A positive certificate would prove existence within its stated finite family. Producing an explicit pair would then require locating a zero-defect point, for example by subdividing the family and recomputing valid bounds, or by direct verification. The present note establishes neither a positive AP-28 certificate nor that localization cost.

The advance over the previous formulation is a proved completion criterion with explicit coefficients, a verified arithmetic test at smaller length, and a quantitative accounting of the depth, moments, and height that a successful argument would need. The AP-28 arithmetic estimate remains open in this work.

### Reproducibility

`research/completion_certificates.py` checks the integer minorants, exact rational coefficients, interval error rule, semiprime incidences, and the AP-5 example. `research/ap28_completion_analysis.py` regenerates the calibration and height tables. `results/completion-analysis.json` labels exact arithmetic separately from probability models. The accompanying tests also compare the geometric floor formula with exhaustive integer-point counts.

```bash
python3 research/completion_certificates.py
python3 research/ap28_completion_analysis.py
python3 -m pytest -q
```

### Follow-up

[Coupled Defect Moments and Exact Lattice Counts for AP-28](paper_ap28_coupled_bounds.md) sharpens the moment bound, proves two obstructions to naive completion arguments, and replaces the row scan for an individual geometric cell with exact Euclidean floor sums. It does not establish aggregate AP-28 moment bounds.

### References

1. Sibuya, M. (1991). *Bonferroni-type inequalities; Chebyshev-type inequalities for the distributions on [0,n]*. Annals of the Institute of Statistical Mathematics 43, 261–285. [Journal paper](https://www.ism.ac.jp/editsec/aism/pdf/043_2_0261.pdf).
2. Fan, S. (2023). *Numerically explicit estimates for the distribution of rough numbers*. [Author preprint](https://arxiv.org/abs/2306.03347).
3. Tao, T. (2015). *Probabilistic models and heuristics for the primes*, Exercise 28. [Author's notes](https://terrytao.wordpress.com/2015/01/04/254a-supplement-4-probabilistic-models-and-heuristics-for-the-primes-optional/).
4. Mok, A., Bradu, A., Rojas, R., Desai, S., and Zhen, S. (2025). *Developing Software to Find Arithmetic Progressions of 28 Primes*. Illinois Mathematics Lab. [Project report](https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf).
5. Wróblewski, J. (2008). *AP26 search*, version 3. [Author's algorithm description](https://www.math.uni.wroc.pl/~jwr/AP26/AP26v3.pdf).
6. Tao, T. (2014). *A general parity problem obstruction*. [Author's discussion](https://terrytao.wordpress.com/2014/11/21/a-general-parity-problem-obstruction/).
