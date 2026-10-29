# Removing Prime Powers by Finite Group Structure

**Author:** Ghassan Al Hamoud

**Date:** 29 October 2026

**Status:** The prime-power correction is eliminated on the stated finite family. A positive AP-28 correlation and an explicit AP-28 remain unproved.

### Abstract

The preceding analytic criterion subtracts a very coarse upper bound for tuples containing proper prime powers. We remove that correction by constructing residue classes that contain no perfect powers anywhere in the 64-bit range. The construction uses power subgroups in finite unit groups. It retains exactly 152,755,199 of the 255,467,520 coprime classes modulo 1,561,650,090; no progression candidates are enumerated to obtain this count. On progressions preserving one of these classes, a positive von Mangoldt product necessarily comes from 28 primes. We give the complete finite proof, an explicit composite passing the conditions, and a reason the construction cannot be extended to all heights with the same modulus. The result closes a correction step, not the missing AP-28 prime-correlation bound.

### 1. The modulus and its unit groups

Set

$$D=23\#=223092870,\qquad M=7D=1561650090,\qquad H=2^{64}-1.$$

The extra factor 7 makes 49 divide the difference. Euler's theorem and the Chinese remainder theorem provide the finite group tools [1,2]. For this particular modulus, cyclicity can be checked directly from the following generators:

| Modulus | Unit-group order | Generator |
|---|---:|---:|
| 3 | 2 | 2 |
| 5 | 4 | 2 |
| 49 | 42 | 3 |
| 11 | 10 | 2 |
| 13 | 12 | 2 |
| 17 | 16 | 3 |
| 19 | 18 | 2 |
| 23 | 22 | 5 |

The component modulo 2 has one element. To verify a listed generator of claimed order $t$, check $g^t=1$ and $g^{t/q}\ne1$ for each prime divisor $q$ of $t$, in the corresponding modulus. This proves the claimed order without enumerating the group.

Let $G=(\mathbb Z/M\mathbb Z)^\times$. Its order is

$$\varphi(M)=2\cdot4\cdot42\cdot10\cdot12\cdot16\cdot18\cdot22
=255467520.$$

For a prime $\ell$, write $G^\ell=\{b^\ell:b\in G\}$. Define

$$S_0=G\setminus\bigl(G^2\cup G^3\cup G^5\cup G^7\cup G^{11}\bigr).$$

Membership in $S_0$ means that the residue is not a power of any of these five orders in the full unit group.

### 2. Explicit modular tests

For a unit $r$ modulo $M$, membership in $S_0$ is equivalent to all five conditions below:

1. For at least one $p\in\{3,5,7,11,13,17,19,23\}$, $r^{(p-1)/2}\not\equiv1\pmod p$.
2. For at least one $p\in\{7,13,19\}$, $r^{(p-1)/3}\not\equiv1\pmod p$.
3. $r^2\not\equiv1\pmod{11}$.
4. $r^6\not\equiv1\pmod{49}$.
5. $r^2\not\equiv1\pmod{23}$.

These are, respectively, the exclusions for powers of order 2, 3, 5, 7, and 11. For example, a seventh power of a unit modulo 49 has sixth power equal to one, since $\varphi(49)=42$. The converse follows from the cyclic group of order 42.

For squares, checking modulo 7 suffices for the component modulo 49: the square criterion in a cyclic group of order 42 is the same parity condition on its generator exponent as in its reduction modulo 7. The analogous reduction gives the cube test modulo 7. The table lists every component where the respective power map has nontrivial index.

These tests use modular powers of one residue. They do not test the primality of a progression.

### 3. Counting the retained classes without listing them

In a cyclic group of order $t$, the image of the $\ell$-th-power map has index $\gcd(\ell,t)$. Hence the five indices in $G$ are

$$[G:G^2]=256,\quad [G:G^3]=27,\quad [G:G^5]=5,\quad
[G:G^7]=7,\quad [G:G^{11}]=11.$$

The associated membership conditions are independent under the uniform measure on $G$. This is an exact group fact, not an independence assumption about primes. To prove it, express a uniform element in each cyclic component as $g^t$ with uniform exponent. For distinct primes dividing the component order, divisibility of the exponent is independent by CRT. Combining the components preserves this independence. Equivalently, the conditions depend on distinct primary components of the finite abelian group.

It follows that

$$\frac{|S_0|}{\varphi(M)}
=\left(1-\frac1{256}\right)\left(1-\frac1{27}\right)
 \left(1-\frac15\right)\left(1-\frac17\right)\left(1-\frac1{11}\right)
=\frac{1105}{1848},$$

so

$$|S_0|=152755200.$$

No scan over these residue classes enters the argument.

### 4. The remaining exponent and the finite theorem

The exponent 13 requires one additional exclusion. Put

$$N_*=29^{13}=10260628712958602189,\qquad
r_*=N_*\bmod M=839436809,$$

and define

$$S=S_0\setminus\{r_*\}.$$

The exceptional residue belongs to $S_0$. Direct modular certificates for its five conditions are

$$N_*\equiv2\pmod3,\quad N_*^4\equiv3\pmod{13},\quad
N_*^2\equiv4\pmod{11},\quad N_*^6\equiv29\pmod{49},\quad
N_*^2\equiv8\pmod{23}.$$

Consequently

$$|S|=152755199,\qquad
\alpha:=\frac{|S|}{\varphi(M)}=\frac{152755199}{255467520}>0.5979.$$

This fraction counts unit residue classes. It is not a measured probability that a progression is prime.

**Theorem 1.** If $2\le n\le H$ and $n\bmod M\in S$, then $n$ is not a perfect power $b^e$ with integers $b,e\ge2$.

**Proof.** Suppose $n=b^e$. Since $n$ is a unit modulo $M$, so is $b$. If $e$ has a prime divisor $\ell\in\{2,3,5,7,11\}$, then $n=(b^{e/\ell})^\ell$ and its residue lies in $G^\ell$, contradicting membership in $S_0$.

Otherwise the least prime divisor of $e$ is at least 13, so $e\ge13$. The only integer $b$ with $2\le b\le30$ coprime to $M$ is 29. Moreover,

$$31^{13}=24417546297445042591>H,\qquad29^{14}>H.$$

Thus the only possible remaining perfect power is $b^e=29^{13}=N_*$. Its residue $r_*$ was removed. This is also impossible. $\square$

This theorem excludes powers with composite bases as well as proper prime powers.

### 5. What this fixes in the analytic AP-28 criterion

Consider

$$\mathcal F_X=\{(a,m)\in\mathbb Z^2:a\ge2,\ m\ge1,
\ a+27Mm\le X,\ a\bmod M\in S\},\qquad X\le H.$$

All 28 terms have the same residue modulo $M$. Theorem 1 therefore excludes every proper prime power from every term of every member of this family.

Define the actual weighted correlation

$$T_S(X)=\sum_{(a,m)\in\mathcal F_X}
             \prod_{j=0}^{27}\Lambda(a+jMm).$$

Since each term is at least two and is not a proper prime power,

$$\Lambda(n)=\begin{cases}\log n,&n\text{ prime},\\0,&n\text{ composite}\end{cases}
\quad\text{on this family}.$$

Hence

$$T_S(X)>0\quad\Longleftrightarrow\quad
\mathcal F_X\text{ contains an AP-28}.\tag{1}$$

The prime-power correction from [the seventh note](G7-structural-analytic-route.md) is exactly zero here. This is a proved removal of that term, not a smaller heuristic estimate.

For $X\ge27M+2$, put

$$V_M(X)=\frac{(X-2-27M)^2}{54M}.$$

The local constant $\beta_D$ from the earlier notes is unchanged by replacing $D$ with $M$: their sets of prime divisors coincide. The expected weighted main term for the selected family is

$$\alpha V_M(X)\beta_D.$$

To justify this normalization algebraically, fix a unit residue $r$ and substitute $a=r+Mu$. The cone area in $(u,m)$ is $V_M(X)/M$. For $p\mid M$, all forms are nonzero modulo $p$, increasing the old local constant by the factor $M/\varphi(M)$. Other local factors remain the same. The main term for that residue is therefore $V_M(X)\beta_D/\varphi(M)$. Summing over $S$ gives the displayed expression. This computes the main term; it does not bound its finite-height error.

**Corollary 2.** If an arithmetic proof establishes

$$|T_S(X)-\alpha V_M(X)\beta_D|\le E_S(X),\qquad
E_S(X)<\alpha V_M(X)\beta_L,$$

where $\beta_L$ is the earlier rigorous lower enclosure for $\beta_D$, then an AP-28 exists in $\mathcal F_X$.

No numerical bound meeting this condition is established here. Published asymptotic estimates for fixed linear systems do not certify it at this finite height merely by being asymptotic. They also do not supply the actual pair.

### 6. Why this is not a primality construction

An explicit retained residue is

$$r_0=M/2+2=780825047.$$

It is odd and equals 2 modulo each odd prime-power component of $M$. Its five exclusion witnesses are

$$2\pmod3,\quad2^2=4\pmod7,\quad2^2=4\pmod{11},\quad
2^6=15\pmod{49},\quad2^2=4\pmod{23}.$$

Also $r_0\not\equiv r_*\pmod7$. Thus $r_0\in S$.

Nevertheless,

$$19520626127=31\cdot629697617\equiv r_0\pmod M.$$

Both factors exceed one. This is a composite passing every new condition. It was constructed by solving a single congruence for the cofactor, not by searching progression candidates. The example prevents confusing perfect-power exclusion with primality.

The remaining task is the actual joint prime correlation in (1), or a different structure that constructs the pair directly. Single-term character estimates and exact residue counts do not prove that joint lower bound.

There is a stronger finite limitation. **Every unit class modulo $M$ contains an explicitly constructible composite first term of a 28-term progression below $58M+31=90575705251$.** Indeed, choose $b\equiv31^{-1}r\pmod M$ with $2\le b\le M+1$; if the least positive representative is 1, replace it by $M+1$. Then $a=31b$ is composite, $a\equiv r\pmod M$, and the progression with difference $M$ ends at

$$a+27M\le31(M+1)+27M=58M+31.$$

For $r\in S$, every term of this counterfamily is power-free in the stated range, while its first term is composite. Thus the residue conditions alone cannot serve as a universal primality proof for the resulting progressions. This does not rule out a prime progression in the same classes or a stronger argument selecting one.

### 7. The height restriction is essential

No nonempty collection of unit residue classes of one fixed modulus can exclude perfect powers at every height. Given a unit residue $r$, choose $b\ge2$ with $b\equiv r\pmod M$. Euler's theorem gives

$$b^{1+\varphi(M)}\equiv r\pmod M.$$

This is a perfect power. Exponents $1+t\varphi(M)$ produce arbitrarily large examples in the same class.

Thus it would be incorrect to combine this finite power-exclusion theorem with an unspecified eventual positivity threshold and assert that the latter lies inside its validity range. A numerical bound below $H$, or a new argument valid at a different stated height, is still necessary.

### Verification and references

Run `python3 research/power_exclusion.py` for the exact constants in [the certificate](../../results/power-exclusion-checks.json). The accompanying tests verify the displayed generators, the local power-subgroup tests, the exact count, the exceptional exponent, the composite counterexample, and refusal of unsupported heights. The code performs no AP candidate search.

1. NIST DLMF, [Euler–Fermat theorem and the totient function](https://dlmf.nist.gov/27.2), especially equation 27.2.8.
2. NIST DLMF, [Dirichlet characters](https://dlmf.nist.gov/27.8). Character orthogonality is an equivalent formulation of these finite power-subgroup filters. The finite counts and the 64-bit specialization above are proved directly.
