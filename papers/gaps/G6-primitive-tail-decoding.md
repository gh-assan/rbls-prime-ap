# Primitive Tail Intersections as Rational Reconstruction

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Scope:** A local counting result supporting G2. No positive AP-28 score, feasible global label enumeration, or AP-28 witness is established.

### Abstract

The earlier finite-height obstruction showed that fifth-order tail-prime intersections are too sparse for uniform relative volume estimates. Primitivity gives a stronger result: sufficiently high-index homogeneous congruence lattices contain at most one primitive point in the positive AP cone. For AP-28 below $2^{64}$, any five distinct tail primes beyond a cube-root sieve yield a modulus large enough for complete bounded rational reconstruction. One specified intersection can therefore be decoded exactly, followed by its remaining membership tests, without a global Möbius correction. We prove the size condition and verify all 66 nonempty fifth-order intersections in an exhaustively enumerated small family. This resolves one local counting issue; obtaining a positive aggregate AP-28 bound remains open.

### 1. Geometry and the role of primitivity

Let

$$\mathcal T=\{(a,m):a\ge A>0,\ m\ge1,\ a+Wm\le X\},$$

where $W>0$. Assume the region is nonempty. For two points in this region,

$$|am'-a'm|\le\frac{X(X-A-W)}{W}<\frac{X^2}{W}.$$

For example, to bound $am'-a'm$, use $a\le X-Wm$, $a'\ge A$, then $m\ge1$ and $m'\le(X-A)/W$. Exchanging the points bounds the opposite sign.

If both points lie in a homogeneous integer lattice of determinant $Q$, then $Q\mid am'-a'm$. Consequently:

**Proposition 1.** If $Q>X(X-A-W)/W$, that lattice contains at most one point of $\mathcal T$ with $\gcd(a,m)=1$.

**Proof.** The determinant of any two such points must be zero. Their positive ratios $a/m$ coincide. Two positive primitive integer representatives of the same ratio are identical. $\square$

Primitivity is essential. The points $(5,1),(10,2),(15,3),(20,4)$ all satisfy $a\equiv5m\pmod{211}$. A large determinant does not prevent several collinear geometric points. Only the first is primitive.

### 2. Tail labels encode a rational residue

A tail label $(j,q)$ imposes

$$a+jDm\equiv0\pmod q.$$

For distinct prime labels $q_1,\ldots,q_s$, CRT supplies

$$a\equiv cm\pmod N,\qquad N=\prod_iq_i,$$

with $c\equiv-j_iD\pmod{q_i}$. For a primitive point, $\gcd(m,N)=1$: a prime dividing both would also divide $a$.

This is the standard rational-reconstruction problem for $a/m$ from its residue modulo $N$. Rational reconstruction by the Euclidean algorithm is classical [1]. The contribution here is the AP-28 size check and the complete local filtering contract, not a new general reconstruction algorithm.

### 3. Complete decoding with asymmetric bounds

Suppose

$$1\le a\le A_*,\qquad1\le m\le M_*,\qquad N>2A_*M_*.$$

Write $a=cm-Nu$. Since $a<N$ and $0\le c<N$, one has $u\ge0$, and $\gcd(u,m)=1$ follows from $\gcd(a,m)=1$. Moreover,

$$\left|\frac cN-\frac um\right|
=\frac a{Nm}
\le\frac{A_*}{Nm}
<\frac1{2M_*m}\le\frac1{2m^2}.$$

By the classical continued-fraction criterion used in rational reconstruction [1], $u/m$ is a convergent of $c/N$. Enumerate those convergents, recover $a=cm-Nu$, and check the numerator and denominator bounds, positivity, and gcd conditions. The number of Euclidean steps is $O(\log N)$; integer bit costs depend on the sizes of the operands.

Uniqueness follows independently by bounding the determinant of two possible fractions. The decoder therefore returns the sole positive primitive pair or certifies that none exists. It rejects input bounds outside its proved size regime rather than calling an unsupported case empty.

For the AP cone, safe bounds are

$$A_*=X-W,\qquad M_*=\left\lfloor\frac{X-A}{W}\right\rfloor.$$

After decoding, test the actual cone, $\gcd(a,Dm)=1$, the inequalities $q_i^2\le a+j_iDm$, any base-cell restrictions, and the declared small-prime sieve. If the unique possible pair fails one of these tests, the filtered primitive intersection is empty.

This determines one summand exactly. It does not require a density approximation or an expensive primitive-point sum for that summand.

### 4. Why five tail primes suffice throughout the 64-bit AP-28 regime

Set $D=223092870$ and $W=27D=6023507490$. Let $B>28$, $B^3>X$, $X\le2^{64}-1$, and take five distinct primes $q_i>B$. Then

$$N>B^5>X^{5/3}.$$

The exact integer inequalities

$$2642246^3>2^{64}-1,\qquad W>2\cdot2642246$$

give $W>2X^{1/3}$, and hence

$$N>X^{5/3}>\frac{2X^2}{W}\ge2A_*M_*.$$

Thus every specified fifth-order tail intersection in the stated domain satisfies the complete reconstruction condition. Any additional initial congruences can be checked after decoding; they cannot introduce a second primitive candidate.

This statement is stronger than the previous small-volume observation. It makes the primitive count genuinely zero or one and provides an exact decision procedure for that specified cell.

### 5. Arithmetic verification and its limits

The completely enumerated seven-term family has $D=210$, $B=29$, $X=20000$, and $1\le m\le10$. Its fifth defect moment is 66. Those 66 nonempty prime-labeled intersections involve 26 distinct candidates; all 66 are recovered correctly by the decoder. Three are also checked by the earlier independent Möbius/floor-sum primitive counter.

A nontrivial denominator example has

$$a=9143,\qquad m=2,$$

with labels

$$(0,41),(1,73),(2,67),(3,101),(4,79).$$

CRT gives $N=1600036849$ and $c=800022996$. The convergent $u/m=1/2$ reconstructs

$$2c-N=9143.$$

These are **defect intersections**: recovered candidates have at least five composite terms. They are not prime-progression discoveries. They validate the arithmetic needed to count negative contributions to a completion certificate.

The complete catalog comes from direct enumeration of this small family. The decoder is not claimed to have found the catalog without that enumeration. Additional tests exhaust all small bounded fractions, test large asymmetric bounds with composite moduli, and verify rejection outside the proved regime.

### 6. The remaining aggregate problem

The fifth moment is still a sum over possible label sets. Knowing that each term is a decidable zero-or-one value does not make the number of possible terms small. Most intersections may be empty, and finding the relevant ones remains work.

The next mathematical or computational advance must organize this collection without testing an infeasible number of label combinations, or use a different route to a verified witness. The present result closes a local counting issue, not aggregate positivity.

A positive score still requires actual coupled arithmetic bounds, such as

$$L_R-U_{M_1}+\frac56L_{M_2}-\frac12U_{M_3}>0,$$

for valid bounds on one specified finite family. The rational decoder alone supplies none of those aggregate bounds.

### Reproduction and reference

`research/primitive_tail_decoding.py` implements the exact decoder. Run `python3 research/run_tail_decoding_checks.py`; its results are recorded in [tail-decoding-checks.json](../../results/tail-decoding-checks.json).

1. Wang, P. S., Guy, M. J. T., and Davenport, J. H. *P-adic Reconstruction of Rational Numbers*. [Primary paper](https://www.cecm.sfu.ca/~mmonagan/teaching/TopicsinCA19/GuyDavenWang.pdf). It presents the Euclidean reconstruction argument and its connection to continued-fraction approximation. The asymmetric inequality above specializes that classical criterion to the stated bounds.
