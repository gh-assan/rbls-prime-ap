# A Sharp Character-Error Threshold and the Remaining Arithmetic Gap

**Author:** Ghassan Al Hamoud

**Date:** 29 October 2026

**Status:** The modular minorant's optimality is proved. The finite prime-correlation bound, constructive recovery, and an AP-28 witness remain open.

### Abstract

The preceding paper produced a signed character minorant with nonprincipal-to-principal coefficient ratio $6015973/693733$. We prove that this exact ratio is optimal for the same five bad subgroups under a uniform absolute character-error budget. An explicit probability measure supported entirely on rejected residues supplies a matching dual certificate. At the threshold, even controlling every nonprincipal character permits zero mass on the safe set. The result closes the minorant-optimization question and identifies arithmetic information as the remaining obstacle. A separate audit checks why two published quantitative estimates cannot simply be inserted as numerical bounds at the present height. Neither argument establishes the missing AP-28 correlation or constructs its witness.

### 1. Fix the existing residue conditions

Use the group and subgroups from [the ninth paper](G9-character-minorant.md):

$$G=(\mathbb Z/M\mathbb Z)^\times,\qquad M=1561650090,$$

$$B_2=\langle G^2,r_*\rangle,\qquad B_\ell=G^\ell\quad(\ell=3,5,7,11),$$

with indices

$$n_1,\ldots,n_5=(128,27,5,7,11).$$

The safe set is $R=G\setminus\bigcup_iB_i$. Let

$$P=1-\sum_i1_{B_i},\qquad
b=1-\sum_i\frac1{n_i}=\frac{693733}{1330560},$$

$$L=4+b=\frac{6015973}{1330560},\qquad
\rho=\frac bL=\frac{693733}{6015973}.$$

The preceding paper proved $P\le1_R$, with principal Fourier coefficient $b$ and nonprincipal coefficient mass $L$. The convenient error factor nine was a rounding of the exact ratio $L/b$. The exact ratio is the quantity optimized here.

### 2. The independent quotient coordinates

Put $K=\bigcap_iB_i$. Because the subgroup indices are pairwise coprime prime powers, the natural map identifies

$$G/K\cong\prod_{i=1}^5G/B_i.$$

For completeness, if two subgroup indices are coprime, their product subgroup is all of $G$, and the index of their intersection is the product of their indices. Induction proves the stated identification. The quotient has order $1330560$ and each fiber in $G$ has size 192.

Write a quotient point as $(x_1,\ldots,x_5)$, using zero for the identity coordinate. Membership in $B_i$ means $x_i=0$. Thus a safe point has no zero coordinates.

### 3. An explicit dual measure with no safe mass

For each $i$, let $\nu_i$ be uniform on quotient points satisfying

$$x_i=0,\qquad x_j\ne0\quad(j\ne i),$$

and lift it uniformly through the fibers of $G\to G/K$. Every point in its support belongs to exactly one bad subgroup.

Define

$$w_i=\frac1{n_i}+\rho\left(1-\frac1{n_i}\right),\qquad
\nu=\sum_iw_i\nu_i.$$

The exact weights are:

| Coordinate index $n_i$ | $6015973w_i$ |
|---:|---:|
| 128 | 735313 |
| 27 | 890853 |
| 5 | 1758181 |
| 7 | 1454053 |
| 11 | 1177573 |

All weights are positive. Their sum is

$$\sum_iw_i=(1-b)+\rho(4+b)=1.$$

Thus $\nu$ is a probability measure, $\nu(R)=0$, and $P=0$ on its entire support.

This is an abstract residue distribution. It is not asserted to be the distribution of actual prime-progressions or their von Mangoldt weights.

### 4. Bound every nonprincipal Fourier coefficient

A character nontrivial on $K$ has zero expectation under $\nu$, by averaging over each fiber. For a character of $G/K$, let $T$ be its nonempty set of nonprincipal component characters. Set $a_i=n_i-1$.

The mean of a nonprincipal character over the nonzero elements of a finite group of order $n_i$ is $-1/(n_i-1)$, by character orthogonality [1]. Therefore

$$\mathbb E_\nu\chi
=\frac{(-1)^{|T|}}{\prod_{i\in T}a_i}
  \left(1-\sum_{i\in T}w_in_i\right).\tag{1}$$

For $|T|=1$, this equals $\rho$. For $t=|T|\ge2$, its absolute value is

$$\frac{t-1+\rho\sum_{i\in T}a_i}{\prod_{i\in T}a_i}.\tag{2}$$

Here the five $a_i$ are $127,26,4,6,10$. For every subset of size $t\ge2$,

$$\prod_{i\in T}a_i-\sum_{i\in T}a_i\ge14(t-1).\tag{3}$$

For pairs, the minimum occurs at 4 and 6 and equals $24-10=14$. When adding a further factor $a\ge4$ to a product $A\ge24$, the left side increases by $(a-1)A-a\ge68$, which is more than the required increase of 14. This proves (3) by induction.

Since $\rho>1/14$, equation (3) makes (2) at most $\rho$. We have proved the global bound

$$|\mathbb E_\nu\chi|\le\rho
\quad\text{for every nonprincipal character of }G.\tag{4}$$

Equality holds for all 173 nonprincipal characters in the previous minorant. Checking the 31 possible nonempty active-component sets reproduces the exact inequalities, but the induction above proves them without listing the full character table.

### 5. Matching lower bound for every residue minorant

For a real function $F:G\to\mathbb R$, write

$$\widehat F(\chi)=\mathbb E_{r\in G}F(r)\overline{\chi(r)},\qquad
F(r)=\sum_\chi\widehat F(\chi)\chi(r).$$

Suppose $F\le1_R$ and its principal coefficient $\mu=\widehat F(\chi_0)$ is positive. Because $\nu$ is supported outside $R$, one has $\mathbb E_\nu F\le0$. Fourier inversion and (4) then give

$$\mu\le\left|\sum_{\chi\ne\chi_0}\widehat F(\chi)\mathbb E_\nu\chi\right|
\le\rho\sum_{\chi\ne\chi_0}|\widehat F(\chi)|.$$

Consequently every such minorant satisfies

$$\frac{\sum_{\chi\ne\chi_0}|\widehat F(\chi)|}
        {\widehat F(\chi_0)}
\ge\frac1\rho=\frac{6015973}{693733}.\tag{5}$$

The existing $P$ attains equality, since $b=\rho L$ and $\mathbb E_\nu P=0$.

**Theorem 1.** For this fixed safe set $R$, the exact optimal nonprincipal-to-principal coefficient ratio among all pointwise minorants with positive mean is $6015973/693733$.

This includes minorants with additional characters or different values on the rejected set. The proof is a direct matching primal/dual argument, not a numerical optimizer result. No general novelty claim is made for Fourier duality itself.

### 6. A sharp information threshold

Let $\eta$ be any probability measure on $G$. If

$$\operatorname{Re}\mathbb E_\eta\chi\le\delta<\rho$$

for the 173 nonprincipal characters in $P$, then

$$\eta(R)\ge\mathbb E_\eta P\ge b-L\delta>0.$$

At $\delta=\rho$, the measure $\nu$ satisfies these bounds, and even the stronger absolute bounds for every nonprincipal character, but has $\nu(R)=0$. Hence $\rho$ is the exact threshold for a guarantee based only on that uniform character information.

For actual AP tuple weights, such a probability measure is defined only after proving their total weight $T_0$ is positive. Neither positivity of $T_0$ nor a bound below $\rho$ is established by this extremal argument. Arithmetic restrictions might exclude the abstract dual measure; proving such restrictions would be additional mathematical information.

The optimization loop should therefore stop changing residue minorants inside this uniform-error framework. Further progress must improve the actual arithmetic bounds, retain nonuniform signed information, change the mathematical structure with a new proof, or directly construct the pair.

### 7. A separate audit of proposed numerical inputs

Tao and Teräväinen [2] define

$$Q(N)=\exp((\log N)^{1/10})$$

and state their Theorem 1.4 with $2\le w\le Q(N)$. For $1<N<2^{64}$,

$$\log N<64,\quad(\log N)^{1/10}<2,\quad
Q(N)<e^2<(11/4)^2=121/16<8.$$

Their model uses primes $p<w$. A direct substitution that includes prime 23 therefore requires $w>23$ and falls outside this stated range at the natural 64-bit scale. This rejects that substitution, not the theorem or every possible application. Larger ambient parameters or different models require their own complete error calculation.

Their Theorem 1.6 gives an effective asymptotic for fixed finite-complexity linear systems, but no numerical constants and height cutoff establishing the required inequality have been extracted in this project. Leng's stronger logarithmic error rate [3, Theorem 5] has a stated ineffective implied constant. Neither statement, without further work, supplies the numerical $E_0$ and twisted bounds required here.

These checks prevent assigning unspecified constants convenient values or assuming an asymptotic regime includes the target height. They do not prove that sufficiently strong finite estimates are impossible.

### 8. Closure status

The optimality of the modular certificate is now closed for the stated residue conditions and uniform-error metric. The parameter audit also rules out one direct attempt to insert a published uniformity estimate.

The central gaps remain actual finite prime-correlation positivity and mathematical recovery of an explicit AP-28. A proof-and-review loop has no established finite termination guarantee on those research questions. The dual distribution is not an AP-28 impossibility proof, and these optimization results do not close G2 or G3b/G5.

### Verification and references

Run `python3 -m research.character_optimality` for [the exact certificate](../../results/character-optimality-checks.json). Tests verify rational dual weights and profiles, the matching objective, an independent Fourier transform of a small product-group example, rejection of quotient sizes where this dual fails, and the elementary parameter inequality. No AP candidates are enumerated.

1. NIST DLMF, [Dirichlet characters and orthogonality](https://dlmf.nist.gov/27.8).
2. Tao, T., and Teräväinen, J. [Quantitative bounds for Gowers uniformity of the Möbius and von Mangoldt functions](https://arxiv.org/html/2107.02158v4), equation 1.1, Theorems 1.4 and 1.6, and the model convention preceding Proposition 1.2.
3. Leng, J. [Efficient Equidistribution of Nilsequences](https://arxiv.org/html/2312.10772v5), Theorem 5 and its following remark.
