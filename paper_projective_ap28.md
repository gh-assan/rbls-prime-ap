# A Projective Lattice Approach to Prime Arithmetic Progressions

## Exact local geometry, primitive lattice points, and the remaining AP-28 barrier

**Author:** Ghassan Al Hamoud  
**Date:** 28 October 2026  
**Status:** Research proposal with elementary derivations and reproducible checks. No AP-28 discovery or practical discovery guarantee is claimed.

### Abstract

We investigate the search for 28 primes in arithmetic progression through the two-variable family $L_j(a,m)=a+jDm$, where $D=23\#=223092870$ and $0\le j<28$. Instead of fixing the difference or choosing a numerical region from zeta-zero phases, we study the exact geometry of local obstructions in the projective line over each finite field. For a prime $p>28$ not dividing $D$, precisely $p+1-28$ projective directions survive. Choices of surviving directions combine into rank-two congruence lattices; integer weighted lattice reduction preserves these constraints while favoring smaller terms. We derive the lattice basis, the required primitive-point exclusions, and a cancellation identity showing why improved density per raw start need not improve density per sieved candidate. A two-variable local-factor calculation gives an average singular-factor gain of approximately $3.55$ relative to the fixed difference $D$, before term-size penalties. This is useful but insufficient to justify a practical AP-28 search. The proposal identifies a narrower mathematical question: can primitive points in selected congruence lattices be organized so that a substantial, measurable gain remains after local conditioning and size costs? A reference sieve and exact finite-field checks support the formulation, but do not answer that question.

### 1. The problem and the change of viewpoint

An AP-28 is a pair of positive integers $(a,d)$ for which

$$a,a+d,\ldots,a+27d$$

are all prime. Green and Tao established existence for arbitrary progression length [1]. Finding an explicit AP-28 with practical resources is a different problem. The 2025 Illinois Mathematics Lab report describes a specialized AP-28 search based on modular candidate generation and prime-tuple estimates [2]. It provides relevant prior work, not evidence that the construction proposed here is competitive.

If $a>28$, every prime $p\le28$ must divide $d$. Otherwise the 28 terms cover all residues modulo $p$, and a term exceeding $p$ is divisible by $p$. Consequently we write

$$d=Dm,\qquad D=23\#,\qquad m\ge1.$$

The old fixed-difference search sets $m=1$ and changes only $a$. Here both coordinates vary. We ask how to construct favorable *pairs*, rather than how to test more starts at one chosen difference.

This paper combines finite-field geometry, CRT, geometry of numbers, and local prime-tuple models. These are established tools. The elementary derivations below are presented to make this particular formulation explicit; we do not assert a new existence theorem or priority over the specialized search literature.

### 2. What additional dimensions can and cannot provide

Suppose 28 affine-linear expressions in $r$ integer parameters form an arithmetic progression identically. Write them as $T_j(z)=c_j+v_j\cdot z$. The condition

$$T_{j+2}-2T_{j+1}+T_j=0$$

forces

$$c_j=c_0+j(c_1-c_0),\qquad v_j=v_0+j(v_1-v_0).$$

Thus every such construction factors through just two affine expressions: the start and the difference. Increasing $r$ cannot create more independent affine coordinates for an exact AP. It can still help encode modular choices, organize a search, or share intermediate calculations.

This gives a useful constraint on creativity: a higher-dimensional representation must offer a demonstrable advantage in constructing or organizing the same two-dimensional solution set. A nonlinear parametrization can select a special subset, but does not escape the requirement that all 28 resulting integers be prime.

### 3. Local obstructions are projective directions

Let $p\nmid D$. Modulo $p$, each condition

$$L_j(a,m)=a+jDm\equiv0\pmod p$$

is a line through the origin in $\mathbb F_p^2$.

**Proposition 1.** If $p>k$ and $p\nmid D$, the $k$ forms $a+jDm$, $0\le j<k$, forbid exactly $k$ distinct projective directions. The number of surviving pairs modulo $p$ is

$$G_p=(p-1)(p+1-k).$$

**Proof.** The lines $a=-jDm$ have distinct slopes because $D$ is invertible and $j<p$. Two such lines intersect only at the origin. Their union contains $1+k(p-1)$ points. Subtracting from $p^2$ gives the formula. Each surviving projective direction contains $p-1$ nonzero points. $\square$

For $m\ne0\pmod p$, put $s=a(Dm)^{-1}$. The forbidden values are $0,-1,\ldots,-(k-1)$, so the allowed values are

$$s\in\{1,2,\ldots,p-k\}.$$

There is one additional allowed direction: $m=0$, $a\ne0$. For AP-28 the local possibilities are therefore:

| Prime $p$ | Allowed finite $s$ | Additional direction | Good projective directions | Good pairs in $\mathbb F_p^2$ |
|---|---|---|---:|---:|
| 29 | 1 | $m=0$ | 2 | 56 |
| 31 | 1, 2, 3 | $m=0$ | 4 | 120 |
| 37 | 1 through 9 | $m=0$ | 10 | 360 |
| 41 | 1 through 13 | $m=0$ | 14 | 560 |
| 43 | 1 through 15 | $m=0$ | 16 | 672 |

These are exact counts. They were also checked by enumeration of every pair modulo each listed prime. The machine-readable certificate is `results/projective-certificate.json`.

If $p\mid D$, every form equals $a$ modulo $p$, so $a\ne0$ is the only condition. If $p\le k$ but $p\nmid D$, all finite directions are forbidden and $m=0$ is required. The choice $D=23\#$ absorbs that last requirement for AP-28.

The direction $m=0$ modulo a prime does **not** mean the integer difference vanishes. It means that prime divides its multiplier. Allowing these directions systematically includes differences omitted by a fixed $m=1$ search.

### 4. CRT cells become exact integer lattices

Choose a finite set $S$ of primes greater than 28, none dividing $D$. At each prime choose one allowed projective direction. Split $S$ into:

- $S_f$: a finite slope $a\equiv c_p m\pmod p$, where $c_p=Ds_p\pmod p$;
- $S_\infty$: the direction $m\equiv0\pmod p$.

Set

$$F=\prod_{p\in S_f}p,\qquad I=\prod_{p\in S_\infty}p.$$

CRT produces a unique $c\pmod F$ satisfying $c\equiv c_p\pmod p$. With $F=1$, take $c=0$.

**Proposition 2.** The linear congruences defining the cell have the integer solutions

$$(a,m)=u(F,0)+v(cI,I),\qquad u,v\in\mathbb Z.$$

The lattice determinant is $FI=\prod_{p\in S}p$.

**Proof.** Since $m\equiv0\pmod I$, write $m=Iv$. Then $a\equiv cIv\pmod F$ is equivalent to $a=Fu+cIv$. The displayed basis has determinant $FI$. $\square$

The lattice contains unwanted origins modulo individual primes. A finite slope requires $m\ne0\pmod p$; an infinite slope requires $a\ne0\pmod p$. These exclusions must be restored. Positivity also requires $a>28$ and $m>0$.

There is a stronger global restriction:

$$\gcd(a,Dm)=1.$$

A common factor greater than one would divide all 28 terms. Distinct prime terms cannot share it. Searching arbitrary short vectors without enforcing this primitive-point condition would waste effort and could give misleading local statistics.

Taken over every direction assignment, these cells partition all pairs avoiding the selected local divisors, after origin exclusions. Searching only a subset of cells is a selective heuristic; its completeness or advantage must not be assumed.

### 5. A legitimate role for lattice reduction

For fixed $D$, the largest term is $a+27Dm$. We therefore weight the multiplier coordinate by

$$W=27D.$$

Apply LLL to the integer row basis

$$B_W=\begin{pmatrix}F&0\\cI&WI\end{pmatrix}.$$

The second coordinate of every vector remains divisible by $W$. Dividing it by $W$ recovers a vector in the original congruence lattice. The reference calculation checks the determinant and verifies that the recovered basis differs from the original by an integer unimodular transformation.

This supplies an exact connection between reduction and arithmetic admissibility. Small weighted norm encourages small $a$ and small progression span. It does not enforce positivity, find every point in a bounded positive cone, or imply primality. A reduced basis must be followed by controlled enumeration of integer combinations in the required region.

Minkowski-type short-vector arguments concern signed lattice points. They do not guarantee a primitive positive vector whose 28 forms are prime. We do not use them to make that inference.

### 6. The density gain that disappears after sieving

For a fixed difference $d$, let

$$\nu_p(d)=\begin{cases}1,&p\mid d,\\\min(k,p),&p\nmid d.\end{cases}$$

Define finite products

$$S_P(d)=\prod_{p\le P}\frac{1-\nu_p(d)/p}{(1-1/p)^k},\qquad
\delta_B(d)=\prod_{p\le B}(1-\nu_p(d)/p).$$

For a locally admissible tuple, $\delta_B$ is the exact periodic fraction of starts surviving all primes through $B$. The singular product is used in a conjectural local intensity

$$h(a,d)\approx\frac{S_P(d)}{\prod_{j=0}^{k-1}\log(a+jd)}.$$

When $p>k$ changes from not dividing $d$ to dividing it, its raw-start singular factor increases by

$$\frac{p-1}{p-k}.$$

For AP-28, adding factors 29 and 31 gives gains 28 and 10. But the sieve survival fraction gains those same factors if those primes are already sieved.

**Proposition 3.** For $P\ge B$ and positive $\delta_B$,

$$\frac{S_P(d)}{\delta_B(d)}=
\prod_{p\le B}(1-1/p)^{-k}
\prod_{B<p\le P}\frac{1-\nu_p(d)/p}{(1-1/p)^k}.$$

**Proof.** Cancel the matching numerators for primes $p\le B$. $\square$

In particular, if two differences differ only in prime factors at most $B$, this normalized finite singular factor is identical. Larger term logarithms can then make the nominally richer difference *worse per surviving candidate*. This identity prevents double-counting the value of small-prime avoidance.

There can still be differences in candidate-generation cost, cache reuse, or attainable coverage. They require separate analysis. A useful objective is expected successes per unit work, not just successes per raw integer.

For scale, the reference model gives:

| Start $a$ | Difference $d$ | Local intensity | Relative to $d=23\#$ at the same $a$ |
|---:|---:|---:|---:|
| $10^{15}$ | $23\#$ | $7.925\times10^{-26}$ | 1 |
| $10^{15}$ | $29\#$ | $2.219\times10^{-24}$ | 28.0 |
| $10^{15}$ | $31\#$ | $2.214\times10^{-23}$ | 279.4 |
| $10^9$ | $23\#$ | $2.488\times10^{-20}$ | 1 |
| $10^9$ | $29\#$ | $2.305\times10^{-20}$ | 0.926 |
| $10^9$ | $31\#$ | $7.263\times10^{-21}$ | 0.292 |

These are truncated heuristic intensities, not measured discovery probabilities. The small-start examples show why the full product of logarithms matters. The reciprocal of an intensity at one location cannot be extrapolated unchanged across an enormous range of starts or differences.

### 7. What freeing the difference buys on average

For $p\nmid D$, Proposition 1 gives the two-variable survival fraction

$$\gamma_p=\frac{(p-1)(p+1-k)}{p^2}.$$

Its normalized local factor is

$$\beta_p=\frac{\gamma_p}{(1-1/p)^k}
=\frac{1-(k-1)/p}{(1-1/p)^{k-1}}.$$

For $p\mid D$, it is $\beta_p=(1-1/p)^{1-k}$. When $D$ contains every prime through $k$, the finite product satisfies the exact identity

$$\prod_{p\le P}\beta_p=
S_{k-1,P}(D)\prod_{p\mid D}(1-1/p)^{-1},$$

provided $P$ includes all prime divisors of $D$.

For $k=28$, $D=23\#$, and $P=100000$, the ratio of this product to $S_{28,P}(D)$ is approximately **3.54944**. This calculation averages pairs across residues; it does not guarantee uniform finite-box behavior or equal term sizes. It is also not an improvement factor over a search that already varies its differences.

The magnitude matters. Merely adding a free difference coordinate does not explain an enormous probability increase per pair. More search volume creates more possible pairs, but remains computational work. The theory of linear equations in primes provides the broader setting for multivariable patterns [3,4]; its asymptotic results do not supply a practical search budget for this proposed family.

### 8. Three possible mathematical advances

The formulation leaves three concrete avenues rather than a promise that the search is solved.

**Primitive points in positive cones.** Can one choose and enumerate congruence cells so that their small positive primitive points have substantially smaller term products than a conventional sieve reaches for the same work? A useful result would compare counts in a specified cone with explicit dependence on the CRT modulus and direction assignment. Finding a short signed vector is insufficient.

**Multiscale local geometry.** Can adjacent levels of the projective CRT tree be organized so that a large fraction of branches is excluded by geometric size bounds before candidate enumeration? A gain would come from proving that certain cells miss the bounded positive region, rather than testing their integers one by one. The bounds must account for lattice orientation and translation.

**Structure beyond local avoidance.** Is there an observable statistic on the constructed primitive points that predicts simultaneous primality *after conditioning on the same small-prime constraints and term sizes*? A claimed gain here would need stronger evidence than a high unconditioned density. Sieve theory's parity barrier cautions against assuming that more small-factor information automatically detects primes; the present work does not resolve that barrier.

These questions mix geometry of numbers, discrete optimization, and analytic number theory. Any positive answer must be assessed against existing modular AP search methods, not against a deliberately weak brute-force baseline.

### 9. Evidence and implementation boundaries

The accompanying code has two distinct roles.

`research/projective_lattice.py` constructs the exact cells and weighted bases. Exhaustive finite-field checks establish the counts in Section 3, and integer transformation checks establish lattice preservation. It does **not** implement a complete projective-cell search or demonstrate an AP-28 advantage.

`prime_ap.py` and `search_prime_ap.py` provide a one-difference reference oracle. They construct starts with CRT, sieve them in bounded numeric segments, and verify surviving terms with deterministic Miller–Rabin for integers below $2^{64}$, using the first twelve prime bases [5]. Every start in the specified half-open interval is accounted for. Terms may extend beyond that interval. A small-prime prefix is tested directly so that a term equal to a sieving prime is not incorrectly rejected.

A fixed five-million-start demonstration at $a\in[10^9,10^9+5000000)$ with $d=23\#$ found 11 AP-9s. All 99 reported terms were independently checked with SymPy. One example is

$$1000376633+j\cdot223092870,\qquad0\le j<9.$$

This demonstrates the reference sieve, not the projective proposal or an AP-28 extrapolation. A ten-million-start AP-28 smoke test at $10^{15}$ found none and sent no candidates to final primality testing. Given its tiny modeled expectation, that miss provides effectively no evidence about discovery feasibility.

The matched direct/sieved experiment stores every repeat and miss in `results/comparison.json`. Its five windows each contain 100000 raw starts; two were selected to recover the historical AP-7 and AP-8. These are regression and local throughput experiments, not unbiased discovery-yield experiments. They compare the same Python primality verifier with and without modular candidate generation, not a specialist GPU implementation. Prime-pattern sieving already has substantial prior algorithmic literature [6].

The short-pilot difference planner reports conjectural hits per second, including observed pilot work. Its rankings need longer repeated pilots before interpretation. It cannot turn a tiny local expectation into a credible discovery forecast.

### 10. Why the old resonance argument does not transfer

The original lattice approximately minimizes $\|q\alpha_i\|$ with $\alpha_i=t_i/(2\pi)$. The code subsequently uses $y=q\lfloor C\log(10^{15})/q\rfloor/C$. A small error for $q\alpha_i$ does not imply a small error for $y\alpha_i$.

For the reproduced first vector, $q=70109$. The three unscaled phase errors are approximately $0.00393$, $0.00544$, and $0.00139$ cycles. At the generated $y=34.53849776$, they are approximately $0.30180$, $0.44242$, and $0.48400$ cycles. The intended alignment has been lost.

Moreover, even a corrected alignment objective would need an explicit-formula argument linking its sign, weights, and scale to *joint* primality. A few low zeros do not resolve the individual-prime scale here. The new formulation therefore uses LLL on congruence lattices with exact arithmetic meaning, rather than assuming a spectral prime-density benefit.

### 11. Assessment and the criterion for continuing

This is a mathematically coherent research direction with a substantial missing step. It has exact local geometry and a precise lattice construction. It does not yet have a theorem or experiment showing the orders-of-magnitude reduction needed for an AP-28 discovery campaign.

The next mathematical deliverable should be a quantitative result for primitive points in the positive CRT lattices, or a predictive statistic that survives the conditioning test in Section 6. Until such a result exists, scaling the prototype into a long computation would be premature. A successful AP-28 construction would require the actual pair $(a,d)$ and independent verification of every term; none is supplied here.

### Follow-up

[From Local Admissibility to Prime Completion](paper_ap28_completion.md) develops a finite defect-moment certificate for the unresolved step, with exact supporting checks. It does not establish a positive AP-28 certificate.

### References

1. Green, B., and Tao, T. (2008). *The primes contain arbitrarily long arithmetic progressions*. Annals of Mathematics 167, 481–547. [Author preprint](https://arxiv.org/abs/math/0404188).
2. Mok, A., Bradu, A., Rojas, R., Desai, S., and Zhen, S. (2025). *Developing Software to Find Arithmetic Progressions of 28 Primes*. Illinois Mathematics Lab; adviser Ravi Fernando, mentor Zishen Qu. [Project report](https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf).
3. Green, B., and Tao, T. (2010). *Linear equations in primes*. Annals of Mathematics 171, 1753–1850. [Author preprint](https://arxiv.org/abs/math/0606088). The original paper states conditional general results; see the subsequent higher-order Fourier program for their resolution.
4. Tao, T. (2010). *The transference principle, and linear equations in primes*. [Author's lecture notes](https://terrytao.wordpress.com/2010/06/05/254b-lecture-notes-7-the-transference-principle-and-linear-equations-in-primes/).
5. Sorenson, J., and Webster, J. (2017). *Strong pseudoprimes to twelve prime bases*. Mathematics of Computation 86, 985–1003. [Author preprint](https://arxiv.org/abs/1509.00864).
6. Sorenson, J. P., and Webster, J. (2020). *Two algorithms to find primes in patterns*. Mathematics of Computation 89, 1953–1968. [Author preprint](https://arxiv.org/abs/1807.08777).
