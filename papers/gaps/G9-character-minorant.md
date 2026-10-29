# Signed Character Minorants for Finite AP-28 Certificates

**Author:** Ghassan Al Hamoud

**Date:** 29 October 2026

**Status:** The modular error-transfer step is resolved. Actual finite prime-correlation bounds and an AP-28 witness remain unproved.

### Abstract

The power-exclusion construction selects more than 152 million unit residue classes. Applying a separate arithmetic error bound to every class would incur an unnecessarily large loss. We construct a signed minorant with exactly 174 character coefficients. It also absorbs the exceptional thirteenth-power residue into a quadratic subgroup, so no separate exceptional-class correlation is needed. Its principal coefficient is positive, and the ratio of its nonprincipal coefficient mass to that coefficient is less than nine. This gives an explicit finite sufficient condition involving one principal correlation and 173 twisted correlations. The arithmetic estimates required by that condition are not supplied here. A separate Parseval argument shows why a uniform absolute-error version cannot complete witness localization near a single occupied class.

### 1. The finite family and the aggregation problem

Use the notation of [the power-exclusion paper](G8-power-exclusion.md):

$$M=7\cdot23\#=1561650090,\quad H=2^{64}-1,\quad
G=(\mathbb Z/M\mathbb Z)^\times,$$

$$|G|=255467520,\qquad r_*=29^{13}\bmod M=839436809.$$

For $X\le H$, the goal remains an explicit pair in

$$\Omega_X=\{(a,m)\in\mathbb R^2:a\ge2,\ m\ge1,\ a+27Mm\le X\}.$$

The preceding paper selected residues avoiding $G^2,G^3,G^5,G^7,G^{11}$, then removed the single class $r_*$. Its finite power-exclusion theorem is valid, but summing numerical remainders separately over 152,755,199 classes would be a poor way to transfer an analytic bound.

We replace that sum by a short exact character identity. This is a bound on how arithmetic errors would combine. It is not an estimate of the arithmetic errors themselves.

### 2. Absorb the exceptional power into a subgroup

Define five bad subgroups:

$$B_2=\langle G^2,r_*\rangle=G^2\cup r_*G^2,\qquad
B_\ell=G^\ell\quad(\ell=3,5,7,11).$$

The equality for $B_2$ follows because $r_*^2\in G^2$. Moreover, $r_*\notin G^2$, since it is 2 modulo 3. Thus the two square cosets are disjoint and

$$[G:B_2]=128.$$

The other four indices are unchanged:

$$I_2=128,\quad I_3=27,\quad I_5=5,\quad I_7=7,\quad I_{11}=11.$$

Put

$$R=G\setminus\bigcup_{\ell\in\{2,3,5,7,11\}}B_\ell.$$

This is a subset of the preceding safe set: it avoids every listed power subgroup and excludes $r_*$. Therefore every integer in $[2,H]$ with residue in $R$ is not a perfect power.

The enlarged $B_2$ depends only on the quadratic component of $G$. The other four conditions depend on their respective odd primary components, so the exact independence argument from the preceding paper still applies. Consequently

$$\frac{|R|}{|G|}=\prod_\ell(1-I_\ell^{-1})
=\frac{1651}{2772},\qquad |R|=152156160.$$

The modest loss of safe residue classes eliminates the need for an isolated point-mass correction in the character expansion. This is a finite group count, not a prime-density assertion.

### 3. A signed lower weight

For a unit residue $r$, define

$$P(r)=1-\sum_\ell1_{B_\ell}(r).$$

Extend $P$ by zero off the unit group. If $r\in R$, then $P(r)=1$. Otherwise at least one bad event occurs and $P(r)\le0$. Hence

$$-4\le P(r)\le1_R(r).\tag{1}$$

This is the first Bonferroni minorant for five subgroup events. Its negative values are essential: using the product of the five complementary indicators would introduce many more character combinations.

### 4. Exactly 174 characters and an explicit error budget

For a subgroup $B\le G$, let $B^\perp$ be its annihilator: the characters that equal one on $B$. Character orthogonality [1] gives

$$1_B(r)=\frac1{[G:B]}\sum_{\chi\in B^\perp}\chi(r).$$

For $r\in B$ every summand is one. For $r\notin B$, translating the character sum by a character detecting its nonidentity quotient class makes the sum vanish. This proves the identity.

Let $\chi_0$ be the principal character modulo $M$. Substituting the subgroup identities into $P$ gives

$$P(a)=b\chi_0(a)-\sum_\ell\frac1{I_\ell}
                 \sum_{\substack{\chi\in B_\ell^\perp\\\chi\ne\chi_0}}\chi(a),\tag{2}$$

where

$$b=1-\sum_\ell I_\ell^{-1}
=\frac{693733}{1330560}>\frac12.$$

Every nonprincipal character in the $\ell$-family has order $\ell$. Families for distinct primes therefore have no nonprincipal characters in common. There are exactly

$$1+\sum_\ell(I_\ell-1)=1+127+26+4+6+10=174$$

characters in (2). The nonprincipal coefficient mass is exactly

$$L=\sum_\ell\frac{I_\ell-1}{I_\ell}
=4+b=\frac{6015973}{1330560}.$$

Its ratio to the principal coefficient satisfies

$$\frac Lb=\frac{6015973}{693733}<9.\tag{3}$$

All these constants follow from five subgroup indices. Neither the residue classes nor a full character table need be listed.

Conjugate characters have the same real correlation because the tuple weights are real. The 127 nonprincipal quadratic characters are real, while the remaining 46 characters form 23 conjugate pairs. Thus the 174 coefficients involve only 151 distinct real correlations, including the principal one. The coefficient mass is unchanged by pairing them.

### 5. The finite arithmetic certificate

Define the actual nonnegative tuple weight

$$W(a,m)=\prod_{j=0}^{27}\Lambda(a+jMm),$$

and the actual twisted correlations

$$T_\chi(X)=\sum_{(a,m)\in\Omega_X\cap\mathbb Z^2}\chi(a)W(a,m).$$

Let $T_0=T_{\chi_0}$. There is no uncounted positive contribution from nonunit starts. If a prime dividing $M$ also divides $a$, it divides every term. Positive $W$ would then require all terms to be powers of that prime. Three distinct powers of one prime cannot form an increasing AP: after dividing $q^u+q^w=2q^v$ by its smallest power, reduction modulo $q$ gives $1=0$. Thus $T_0$ equals the full untwisted von Mangoldt sum on the cone.

By (1)-(2), the selected prime sum satisfies

$$\sum_{\substack{(a,m)\in\Omega_X\cap\mathbb Z^2\\a\bmod M\in R}}W(a,m)
\ge bT_0-\sum_\ell\frac1{I_\ell}
       \sum_{\substack{\chi\in B_\ell^\perp\\\chi\ne\chi_0}}\operatorname{Re}T_\chi.\tag{4}$$

Conjugate characters occur together, so the right side is real. The selected sum contains no proper prime powers when $X\le H$. A strictly positive right side therefore proves an AP-28 in this family.

For $X\ge27M+2$, put

$$V_M(X)=\frac{(X-2-27M)^2}{54M},$$

and retain the rigorous Euler-product lower bound $\beta_L$ from the earlier papers. Suppose valid finite arithmetic estimates establish

$$T_0(X)\ge V_M(X)\beta_L-E_0(X),$$

$$\operatorname{Re}T_\chi(X)\le\epsilon(X)
\quad\text{for the 173 nonprincipal characters in (2)},$$

with $E_0,\epsilon\ge0$. Then (4) is at least

$$b\bigl(V_M(X)\beta_L-E_0(X)\bigr)-L\epsilon(X).$$

**Theorem 1.** Assume $27M+2\le X\le H$ and the actual arithmetic bounds above. The strict inequality

$$E_0(X)+9\epsilon(X)<V_M(X)\beta_L\tag{5}$$

proves an AP-28 below $X$.

**Proof.** Equation (3) makes the lower bound in (4) strictly positive. The power-exclusion theorem converts its positive selected von Mangoldt contribution into a tuple of 28 primes. $\square$

More generally, different upper bounds for different real parts may be inserted directly into (4). Only their weighted one-sided sum is required. Large negative correlations help the lower bound and need not be bounded in absolute value.

Theorem 1 does **not** supply $E_0$ or $\epsilon$. They are 28-term arithmetic correlations. Bounds for one prime at a time, finite group orthogonality, or Euler-product tails do not establish them. No numerical values meeting (5) are proved here.

### 6. Why a uniform absolute bound cannot finish localization

There is a precise limit if the stronger assumption $|T_\chi|\le\epsilon$ is used. Aggregate the nonnegative weights by the quadratic quotient $G/B_2$, of size $N=128$, and write its masses as $v_q$. Suppose $T_0>0$ and exactly $J$ quotient classes are occupied. Orthogonality and Cauchy-Schwarz give

$$\sum_{\substack{\chi\in B_2^\perp\\\chi\ne\chi_0}}|T_\chi|^2
=128\sum_qv_q^2-T_0^2
\ge\left(\frac{128}{J}-1\right)T_0^2.$$

Therefore any uniform absolute upper bound satisfies

$$\frac\epsilon{T_0}\ge\sqrt{\frac{128-J}{127J}}.\tag{6}$$

Even if $T_0$ were known exactly, a positive bound using $bT_0-L\epsilon$ would require $\epsilon/T_0<b/L$. Combining this with (6) forces

$$J>\frac{128(L/b)^2}{127+(L/b)^2}
=\frac{36191931136729}{760255050769},$$

so $J\ge48$ is necessary for that particular absolute-error certificate. This does not assert that 48 classes are occupied in the AP-28 domain, and it does not exclude the one-sided or signed versions of (4).

At a singleton, every character has absolute amplitude $T_0$. The uniform-amplitude lower bound becomes $(b-L)T_0=-4T_0$. Yet at a safe singleton, subgroup orthogonality gives

$$\sum_\ell\frac1{I_\ell}\sum_{\chi\ne\chi_0}T_\chi
=-\left(\sum_\ell I_\ell^{-1}\right)T_0,$$

and the exact signed expression (4) equals $T_0$. The lost information is the character phase, not the size of the coefficients.

Thus an initial uniform error bound cannot simply be assumed to remain sufficient through bisection to one witness. Constructive recovery still needs valid, sufficiently sharp child estimates or another structural way to retain the signed information.

### 7. What is closed, and what remains open

The modular error-aggregation problem is now explicit and bounded: a signed minorant uses 174 character correlations with a relative error multiplier below nine. It absorbs the exceptional power into a subgroup and avoids summing a remainder separately over millions of residue classes.

The finite arithmetic problem remains: prove lower and upper correlation estimates that make (4) or (5) positive in an explicit range. A witness must then be recovered mathematically. This note supplies neither that positivity nor the pair, so G2, G3b/G5, and the AP-28 construction goal remain open.

### Verification and reference

Run `python3 -m research.character_minorant` to reproduce [the exact constants](../../results/character-minorant-checks.json). The tests check the quadratic exception pattern, subgroup membership, coefficient arithmetic, a direct Fourier transform on a small independent finite group, and the distinction between signed and absolute bounds. No progression discovery search is run.

1. NIST DLMF, [Dirichlet characters and orthogonality, equation 27.8.6](https://dlmf.nist.gov/27.8). The character identities are standard. The subgroup choice, finite constants, and sufficient inequality above are derived explicitly here; no new general character-orthogonality theorem is claimed.
