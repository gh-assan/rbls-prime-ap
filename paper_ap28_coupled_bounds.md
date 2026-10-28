# Coupled Defect Moments and Exact Lattice Counts for AP-28

## Sharp certificates, a finite-height obstruction, and a lower-order alternative

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Series:** Third note in the projective-lattice and prime-completion investigation  
**Status:** Exact finite results and reproducible checks. No positive AP-28 arithmetic certificate or AP-28 witness is established.

### Abstract

The preceding note reduced prime completion to a signed inequality involving five defect moments. This paper examines whether that reduction can be made effective. We prove three finite statements. First, a sharper polynomial improves the earlier independent-model lower bound from $153/8000$ to the optimal five-moment value $9/400$, with an exact matching primal distribution. Second, an explicit finite-difference perturbation constructs a five-wise independent defect model that never has zero defects, showing why low-order agreement with independence cannot generally certify complete primality. Third, throughout the 64-bit AP-28 domain, every individual five-tail-prime intersection has a volume-to-index ratio below $0.00022$. Consequently, uniform small-relative-error estimates for those individual pieces are impossible. We replace the earlier row-by-row geometric count with exact Euclidean floor sums and verify a signed certificate on a genuine AP-7 family, proving at least 72 prime progressions where independent verification finds 78. A cubic alternative and a multiplier cap reduce parts of the arithmetic burden, but still require aggregate AP-28 estimates not supplied here. The results close specific certification and counting gaps while identifying a route that cannot work as originally hoped.

### 1. The common arithmetic setting

For AP-28 write

$$L_j(a,m)=a+jDm,\qquad D=23\#=223092870,\qquad W=27D=6023507490.$$

As in the preceding paper, let $\mathcal R$ be a specified finite family with

$$B<a,\qquad m\ge1,\qquad a+Wm\le X,\qquad B>28,\quad B^3>X,$$

such that every term has no prime divisor at most $B$ and $\gcd(a,Dm)=1$. Every term is prime or semiprime. Let $C$ count its composite terms, and set

$$R=|\mathcal R|,\qquad M_r=\sum_{\mathcal R}\binom Cr,\qquad N_{28}=\#\{C=0\}.$$

The previous paper gave a valid degree-five minorant but left two substantive gaps: the required arithmetic moment bounds were unavailable, and their geometric incidence sums could contain extremely sparse pieces.

This note combines established discrete moment methods [1,2], limited independence [3], and Euclidean floor-sum techniques [4]. The explicit specializations below are proved directly. No priority claim is made for these general methods.

### 2. Treat the moments as one feasible histogram

For a nonempty family, put $\mu_r=M_r/R$. Any possible normalized defect histogram $y_0,\ldots,y_k$ satisfies

$$y_c\ge0,\qquad\sum_{c=0}^k\binom cr y_c=\mu_r\quad(0\le r\le s),$$

where $\binom cr=0$ for $r>c$. Therefore the sharp probability bound from these moments alone is the finite optimization problem

$$\mathcal L_s(\mu)=\min y_0\quad\text{subject to the displayed constraints}.$$

This uses the requirement that all moments come from one nonnegative histogram. Arbitrary independent choices inside separate moment intervals need not satisfy it.

The dual form is elementary. If

$$P(c)=\sum_{r=0}^s b_r\binom cr\le1_{\{c=0\}}\quad(0\le c\le k),$$

then every feasible histogram obeys $y_0\ge\sum b_r\mu_r$. To prove sharpness it is enough to exhibit a feasible histogram attaining that value. No numerical optimizer is needed to verify such a primal/dual pair.

With certified intervals $\ell_r\le\mu_r\le u_r$, any such polynomial gives

$$y_0\ge\sum_{b_r\ge0}b_r\ell_r+\sum_{b_r<0}b_ru_r.$$

Optimizing the polynomial can improve this interval bound. It cannot make unproved interval endpoints valid arithmetic information.

#### A sharp improvement to the earlier calibration

For the first five moments of $\operatorname{Bin}(28,1/10)$, choose

$$P_5(c)=\frac{(1-c)(c-3)(c-4)(c-6)(c-7)}{504}.$$

At positive integers, its paired factors are nonnegative and $1-c\le0$. Also $P_5(0)=1$. Its binomial expansion is

$$P_5(c)=1-\binom c1+\frac{58}{63}\binom c2
-\frac{16}{21}\binom c3+\frac{11}{21}\binom c4
-\frac5{21}\binom c5.$$

The resulting lower bound is $9/400=0.0225$. To prove it is the **optimal bound from these five moments**, assign the following probabilities:

| Defect count $c$ | 0 | 1 | 3 | 4 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|
| $20000y_c$ | 450 | 6104 | 7560 | 4410 | 756 | 720 |

They sum to one, reproduce all six moments $\mu_0,\ldots,\mu_5$, and place mass $9/400$ at zero. The polynomial is tight on their support. This proves sharpness by direct rational arithmetic.

The earlier $153/8000$ bound was sufficient but not optimal. The improvement is a statement about this supplied moment vector, not a gain in prime-search probability. The actual independent-model probability is still $(9/10)^{28}\approx0.0523348$; the five moments do not determine it.

### 3. A limited-independence obstruction

An exact construction shows that other independent-model moment vectors cannot force any mass at zero.

**Theorem 1.** Let $k\ge1$, $0\le s<k$, $0<p<1$, put $n=s+1$, and suppose

$$\frac{p}{1-p}\ge\frac nk.$$

There is a probability law supported on $\{1,\ldots,k\}$ whose binomial moments through order $s$ equal those of $\operatorname{Bin}(k,p)$.

**Proof.** Start with $w_c=\binom kc p^c(1-p)^{k-c}$ and define

$$w'_c=w_c-(1-p)^k(-1)^c\binom nc\quad(0\le c\le n),$$

leaving $w'_c=w_c$ for $c>n$. The new mass at zero is zero. For odd $c$, mass increases. For even $c>0$,

$$\frac{w_c}{(1-p)^k}=\binom kc\left(\frac p{1-p}\right)^c
\ge\binom nc,$$

because $\binom kc/\binom nc\ge(k/n)^c$. Thus every mass remains nonnegative.

For $0\le r<n$, the finite-difference identity

$$\sum_{c=0}^n(-1)^c\binom nc\binom cr=0$$

shows that the moments, including total mass, are unchanged. $\square$

Conditional on $C=c$, choose the $c$ defect positions uniformly among the $k$ positions. For a specified set of $r\le s$ positions,

$$\Pr(\text{all are defective})=\frac{\mathbb E\binom Cr}{\binom kr}=p^r.$$

Inclusion–exclusion then gives the correct probability for every pattern of ones and zeros on those positions. The indicators are $s$-wise independent, yet at least one is always defective.

For $k=28$, $s=5$, the sufficient condition is $p\ge3/17$. In particular, $p=2/5$ gives an exact five-wise independent law with **no zero-defect outcome**. Its full rational weights are recorded in `results/coupled-analysis.json`.

This is an abstract defect law, not an arithmetic AP-28 family. Its implication is an information limit: matching independent joint probabilities through five positions does not, by itself, establish simultaneous primality of all 28 positions.

The single-integer roughness calibration from the preceding paper has

$$p(\theta)=1-\frac1{1+\log((1-\theta)/\theta)},\qquad B=X^\theta.$$

For $1/3\le\theta\le0.4$, this ranges from approximately $0.4094$ down to $0.2885$, above $3/17$. Thus even **exact** moments equal to that calibration cannot yield a positive five-moment certificate. Arithmetic structure beyond that calibration, or different depth/order choices, would be necessary. This statement uses the calibration, not a proved distribution of AP defects [5].

### 4. A finite-height obstruction to separate geometric estimates

A least-prime-factor incidence imposes

$$a+jDm\equiv0\pmod q,\qquad q>B,\qquad q^2\le a+jDm.$$

For a CRT cell of determinant $Q$, distinct new primes $q_1,\ldots,q_r$ coprime with $Q$ multiply the determinant to $Q\prod q_i$. Origin and roughness exclusions may further reduce the set.

Let $V$ be the area of the containing region $a\ge29$, $m\ge1$, $a+Wm\le X$. The region is empty for $X\le29+W$. Otherwise

$$V=\frac{(X-29-W)^2}{2W}<\frac{X^2}{2W}.$$

**Proposition 2.** If $X\le2^{64}-1$, $B^3>X$, and $r=5$, then for each such intersection

$$\eta:=\frac{\text{its geometric area}}{Q\prod_{i=1}^5q_i}
<\frac{X^{1/3}}{2WQ}
<\frac{0.00022}{Q}.$$

**Proof.** Use $\prod q_i>B^5>X^{5/3}$ and the area bound. For the final numerical bound, $2642246^3>2^{64}-1$ and

$$\frac{2642246}{2W}=\frac{1321123}{6023507490}<0.00022.$$

All inequalities therefore have an exact integer or rational justification. $\square$

This is stronger than saying that lattice orientation might cause trouble. If $0<\eta<1/2$ and $N$ is an integer count, then

$$|N-\eta|\ge\eta.$$

If $N=0$ equality holds; if $N\ge1$ the error is even larger. An estimate $N=\eta(1+o(1))$ for every individual piece cannot hold in this regime.

There is a second consequence. For a collection of such predictions,

$$\sum_i|N_i-\eta_i|\ge\sum_i\eta_i.$$

An aggregate estimate obtained only by adding absolute errors of individual pieces cannot achieve small relative error. Cancellation, exact evaluation, or a genuinely aggregate argument is necessary. One-sided aggregate bounds are not ruled out.

This obstruction applies to the proposed **individual-piece approximation strategy**. It does not rule out AP-28, exact finite searches, or stronger analytic methods.

### 5. Replace the row scan by exact Euclidean counts

The earlier formula counted a cell by summing one contribution per multiplier. That is exact but can contain billions of rows. A floor-sum identity removes this dependence for an individual geometric cell.

Define

$$S(n,M,a,b)=\sum_{i=0}^{n-1}\left\lfloor\frac{ai+b}{M}\right\rfloor.$$

First remove integer quotients of $a$ and $b$ by division with remainder; their contributions are

$$\left\lfloor\frac aM\right\rfloor\frac{n(n-1)}2
+\left\lfloor\frac bM\right\rfloor n.$$

For the normalized case $0<a<M$, $0\le b<M$, put $Y=\lfloor(an+b)/M\rfloor$ and $T=an+b-MY$. Exchanging the order of lattice-point counting gives

$$S(n,M,a,b)=S(Y,a,M,T).$$

Indeed, the original count is

$$\sum_{j=1}^Y\left(n-\left\lceil\frac{Mj-b}{a}\right\rceil\right),$$

and substituting $j=Y-i$ gives the claimed sum. If $a=0$, the normalized sum is zero. Repeating these steps follows the Euclidean algorithm. The number of iterations is $O(\log M)$; the bit cost also depends on the sizes of the integer arguments. Standard floor-sum algorithms implement this reciprocity [4].

For a cell

$$(a,m)=(Fu+cIv,Iv),$$

suppose an interval of integer $v$ has active lower boundary

$$a\ge h-\ell Iv,$$

and upper boundary $a\le X-WIv$. Its row contribution is

$$\left\lfloor\frac{X-(W+c)Iv}{F}\right\rfloor
+\left\lfloor\frac{(c+\ell)Iv-h}{F}\right\rfloor+1.$$

Summing the interval needs only two floor sums and its length.

For several defect constraints, the lower boundary is the maximum of the lines $A$ and $q_j^2-jDIv$. Split the multiplier range at their pairwise rational crossings. Continuous feasibility also bounds the upper multiplier, so the displayed row count is nonnegative on each retained interval. At integer crossings either tied line gives the same boundary value.

With a fixed number of constraints, the number of intervals is bounded independently of $X$. The reference checker uses all pairwise crossings, then exact signed integer floor sums. It counts a geometric congruence cell, including the $q_j^2$ inequalities, without visiting each multiplier or assuming that area approximates an integer count.

**Scope:** exclusions not encoded in the supplied cell remain to be imposed. In particular, this counter does not silently add complete roughness or global primitivity. Nor does it sum over the enormous collection of possible tail-prime labels. Those are separate arithmetic problems.

As a check, start from $a\equiv m\pmod{11}$ and add

$$a+420m\equiv0\pmod{31},\qquad a+1050m\equiv0\pmod{37}.$$

CRT gives $a\equiv8570m\pmod{12617}$. In $a\ge30$, $1\le m\le10$, $a+1260m\le20000$, with the respective square thresholds, the exact counter and independent enumeration both give **11** points. This is a geometric test before the remaining roughness exclusions, not 11 prime progressions.

### 6. A signed certificate on an actual AP-7 family

Take $k=7$, $D=210$, $B=29$, $X=20000$, and $1\le m\le10$. Include every integer start $a>B$ with $a+6Dm\le X$ whose seven terms avoid prime factors at most $B$.

Because $m\le B$ and every prime factor of $D$ is at most $B$, roughness already forces $\gcd(a,Dm)=1$. Also $29^3>20000$, so the prime/semiprime defect identities apply.

Least-prime-factor incidences give the exact histogram

$$(n_0,\ldots,n_7)=(78,230,320,225,81,21,4,1),$$

independently checked against primality tests. The binomial moments are

$$(M_0,\ldots,M_7)=(960,2005,1772,874,281,66,11,1).$$

The first-moment bound is negative. Instead use

$$P(c)=\frac{(1-c)(c-2)(c-3)(c-5)(c-6)}{180},$$

which yields

$$N_7\ge M_0-M_1+M_2-M_3+\frac{14}{15}M_4-\frac23M_5
=\frac{1069}{15}.$$

Since $N_7$ is an integer, this proves **at least 72** prime progressions. Direct checking finds 78. The ordinary fifth-order Bonferroni bound gives 68.

The weights

$$\left(\frac{1069}{15},\frac{1347}5,225,\frac{1034}3,
\frac{232}5,\frac{49}{15}\right)$$

at defect counts $(0,1,2,3,5,6)$ reproduce the first six unnormalized moments. Thus the rational lower bound is sharp over nonnegative real histogram weights. Fixed-size integer histograms permit rounding and may permit further improvements; no integer-optimality claim is made.

One verified example is $47+210j$, $0\le j<7$. The calculation establishes actual signed arithmetic moments at smaller length. It does not establish the corresponding AP-28 moments or a scalable way to obtain them.

### 7. A lower-order target and an automatic primitive-point restriction

The five-tail obstruction suggests testing fewer moments at greater initial roughness. A valid cubic is

$$P_3(c)=\frac{(1-c)(c-3)(c-4)}{12}
=1-\binom c1+\frac56\binom c2-\frac12\binom c3.$$

For actual AP-28 arithmetic moments it gives the sufficient condition

$$\boxed{R-M_1+\frac56M_2-\frac12M_3>0.}$$

In the independent model with defect probability $1/20$, this normalized expression is $731/4000=0.18275$, even though $1-\mu_1=-0.4$. With $\mu_0=1$ exact, common absolute errors below $0.18275/(7/3)$ in the other three normalized moments would preserve positivity around that model vector. These are requirements for arithmetic bounds, not bounds already obtained.

The single-integer calibration corresponds to

$$\theta=\frac1{1+e^{1/19}}\approx0.486845.$$

At $X=2^{64}-1$, it has $B\approx2.39618\times10^9$. The upper-area proxy for a triple tail intersection at base determinant one is approximately $2.05$, compared with about $9.10\times10^{-18}$ for the earlier five-moment $q=0.9$ calibration. A nontrivial base determinant and the square thresholds make these pieces smaller. The cubic reduces one burden, but does not make individual density approximations reliable.

There is a useful exact restriction. If every prime factor of $D$ is at most $B$, $a$ is $B$-rough, and $m\le B$, then

$$\gcd(a,Dm)=1.$$

Any prime dividing $Dm$ would be at most $B$, so it cannot divide $a$. The cap therefore removes the need for a separate global gcd exclusion in a completely rough family. It does not remove the roughness sieve itself.

The cap need not discard much geometric area at this depth. Let $A=B+1$, assume $H=X-A-W>0$, and put $\rho=\min(1,W(B-1)/H)$. Within the same lower-start triangle, the fraction of area with $m\le B$ is

$$2\rho-\rho^2.$$

For $X=2^{64}-1$ and $B=2396179891$, this is approximately **0.952666**. This is retained *area*, not a guarantee of retaining that fraction of the prime progressions.

Without the multiplier cap, primitivity is not automatic: with $B=7$, $D=6$, $a=121$, $m=11$, the terms $(121,187,253)$ are all $B$-rough but share the factor 11.

### 8. Which gaps are closed, and which remain

This paper establishes the following finite advances:

- a matching primal/dual certificate proves the sharp five-moment calibration bound;
- an explicit five-wise independent countermodel identifies information the moments can fail to contain;
- an integer-count argument rules out a naive individual-piece relative approximation throughout the 64-bit five-tail regime;
- Euclidean reciprocity replaces a multiplier-length row scan for each geometric cell;
- a genuine AP-7 family supplies exact signed moments and a nontrivial positive certificate;
- a cubic target and a multiplier cap reduce moment order and one primitive-point complication.

The remaining AP-28 task is **aggregate arithmetic control**. For a specified rough family, obtain valid bounds for one of the displayed signed functionals, or evaluate it exactly without enumerating an infeasible number of label combinations. A near-independent low-order fit is not sufficient in the regimes ruled out by Theorem 1. An unsigned sum of separate geometric errors is not sufficient in the regime of Proposition 2.

A concrete direction is to keep the signed functional intact while summing prime-label incidences, applying cancellation or shared arithmetic structure before taking absolute values. The present work provides no bound for that signed remainder. It would be incorrect to treat the cubic model margin, the retained area, or the faster individual counter as such a bound.

Consequently, no practical AP-28 discovery budget or positive AP-28 certificate follows yet. The narrower result is that some tempting routes are now ruled out precisely, and the arithmetic quantity requiring a genuinely stronger argument has been reduced and made explicit.

### Reproducibility

`research/coupled_moments.py` verifies the rational moment certificates and the AP-7 family. `research/lattice_floor_counts.py` implements exact Euclidean counts. `research/run_coupled_analysis.py` writes the independently labeled certificates and proxies to `results/coupled-analysis.json`. Tests compare mixed five-variable pattern probabilities, exact primal/dual constraints, signed floor sums, half-plane envelopes, and augmented congruences against independent finite calculations.

```bash
python3 research/run_coupled_analysis.py
python3 -m pytest -q
```

### References

1. Prékopa, A. (1990). *The discrete moment problem and linear programming*. Discrete Applied Mathematics 27, 235–254. [Publisher record](https://www.sciencedirect.com/science/article/pii/0166218X9090068N); [author's bibliography](https://rutcor.rutgers.edu/Prekopa/Discrete%20Moment%20Problems.html).
2. Sibuya, M. (1991). *Bonferroni-type inequalities; Chebyshev-type inequalities for the distributions on [0,n]*. Annals of the Institute of Statistical Mathematics 43, 261–285. [Journal paper](https://www.ism.ac.jp/editsec/aism/pdf/043_2_0261.pdf).
3. Benjamini, I., Gurel-Gurevich, O., and Peled, R. (2012, arXiv posting). *On K-wise Independent Distributions and Boolean Functions*. [Author manuscript](https://arxiv.org/abs/1201.3261). Related endpoint moment problems also appear in Peled, R., Yadin, A., and Yehudayoff, A. (2011), *The maximal probability that k-wise independent bits are all 1*. [Author preprint](https://arxiv.org/abs/0801.0059).
4. AtCoder Library. *Math: floor_sum*. [Official specification and complexity](https://atcoder.github.io/ac-library/production/document_en/math.html). The accompanying Python checker uses exact arbitrary-precision integers, without the machine-width limits of that specification.
5. Tao, T. (2015). *Probabilistic models and heuristics for the primes*, Exercise 28. [Author's notes](https://terrytao.wordpress.com/2015/01/04/254a-supplement-4-probabilistic-models-and-heuristics-for-the-primes-optional/).
