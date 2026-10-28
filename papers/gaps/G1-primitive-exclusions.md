# Primitive-Point Exclusions in Congruence Lattices

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Gap G1:** Exact finite correctness is resolved below. The cost of applying the formula at AP-28 scale is not resolved.

### Abstract

Projective congruence lattices contain unwanted points whose start and difference share a divisor. We derive an exact finite correction using Möbius inversion and give a constructive lattice-intersection formula for every correction term. A general triangular basis is necessary: the integer-slope form used for the original CRT cells need not survive intersection with divisibility constraints. The corrected cells can be counted by the exact Euclidean routine from the third paper. The formula closes the correctness gap concerning primitive points and projective origins, but its number of correction terms can be too large for a practical AP-28 calculation.

### 1. The object to count

Let a rank-two lattice have basis

$$(F,0),\qquad(K,I),\qquad F,I>0,$$

so that $a=Fu+Kv$, $m=Iv$. The integer $K$ is unrestricted. Let $\mathcal P$ be a bounded region with $a\ge A>0$, $m\ge1$, and $a+Wm\le X$, optionally with the extra half-planes used for tail incidences.

For a fixed positive $D$, the required condition is

$$\gcd(a,Dm)=1.$$

It is equivalent to the two conditions $\gcd(a,D)=1$ and $\gcd(a,m)=1$. A correction must impose both, including their overlap.

### 2. A general divisibility intersection

Impose $A_0\mid a$ and $t\mid m$. Define

$$v_0=\frac{t}{\gcd(I,t)},\quad M=Iv_0,\quad K_0=Kv_0,$$

$$g=\gcd(F,A_0),\qquad h=\frac{g}{\gcd(g,K_0)}.$$

Set $L=A_0/g$. When $L>1$, choose

$$U\equiv-\frac{K_0h}{g}(F/g)^{-1}\pmod L;$$

when $L=1$, choose $U=0$.

**Proposition 1.** The intersected lattice has basis

$$(F',0),\qquad(K',I'),$$

where

$$F'=FL,\qquad I'=Mh,\qquad K'\equiv FU+K_0h\pmod{F'}.$$

**Proof.** The constraint on $m$ is equivalent to $v=v_0w$. Solvability of $Fu+K_0w\equiv0\pmod{A_0}$ requires $g\mid K_0w$, hence $w=hz$. Dividing the congruence by $g$ gives $u=Uz+Lr$. Substitution gives the displayed basis. Every step is reversible. Reducing $K'$ modulo $F'$ changes only the basis representative. $\square$

The result is not necessarily $a=F'u+c'I'v$ with integer $c'$. For example, intersecting $(F,I,K)=(2,3,3)$ with $5\mid a$ gives $(F',I',K')=(10,3,5)$. The ratio $K'/I'$ is not integral. An exact counter must retain the triangular coefficient $K'$ rather than assume that the original integer slope is preserved.

### 3. The finite primitive-point formula

Let $D_0=\operatorname{rad}(D)$ and let $M_{\max}$ be an upper bound on the multiplier in $\mathcal P$, for example $\lfloor(X-A)/W\rfloor$. Write $N(\Lambda\cap\mathcal P)$ for an exact geometric count before gcd restrictions.

**Theorem 2.** The number of primitive points is

$$\boxed{
\sum_{s\mid D_0}\mu(s)
\sum_{t=1}^{M_{\max}}\mu(t)
N\!\left(\Lambda\cap\mathcal P\cap
\{\operatorname{lcm}(s,t)\mid a,\ t\mid m\}\right).
}$$

**Proof.** The standard divisor identity $\sum_{d\mid n}\mu(d)=1_{\{n=1\}}$ [1] gives

$$1_{\{\gcd(a,Dm)=1\}}=
\left(\sum_{s\mid D_0,\ s\mid a}\mu(s)\right)
\left(\sum_{t\mid a,\ t\mid m}\mu(t)\right).$$

Every common divisor $t$ is at most $m\le M_{\max}$. Summing this finite identity over the lattice region and exchanging the sums proves the formula. The two conditions on $a$ combine into an lcm. $\square$

Every inner count is a triangular-lattice count supplied by Proposition 1. Half-planes remain inequalities in the original $(a,m)$ coordinates and can be passed unchanged to the geometric counter.

This formula also restores the projective origin exclusions. On a finite-slope cell, $m\equiv0\pmod p$ would force $a\equiv0\pmod p$; an infinite-slope cell already has $m\equiv0$ and must exclude $a\equiv0$. Global primitivity removes both origins. Distinct allowed projective directions then partition primitive points without overlap.

### 4. A useful restricted family

If every prime divisor of $D$ is at most $B$, $a$ is $B$-rough, and $1\le m\le B$, primitivity is automatic: every prime factor of $Dm$ is at most $B$, whereas none divides $a$.

This restriction can eliminate the global correction for an already fully rough candidate family. It is not permission to drop the roughness or origin tests while constructing that family.

### 5. Exact checks and cost

For the intersected lattice $(10,3,5)$, the region $a\ge1$, $m\ge1$, $a+2m\le100$, and $D=6$, both the formula and independent enumeration give **20** primitive points. This is a generic lattice check, not an AP-28 count. Random finite cases also check extra half-planes and negative triangular coefficients.

At most $2^{\omega(D)}M_{\max}$ correction counts appear before skipping zero Möbius coefficients. For AP-28, $D=23\#$ has nine prime factors, while $M_{\max}$ can be billions. Exactness therefore does not establish affordability.

**Resolution:** the finite primitive/origin correction is complete. Efficient complete AP-28 aggregation remains [G2](G2-signed-aggregation.md).

### Reproduction and references

The proof checker is `research/primitive_cells.py`; the shared counter now accepts general triangular bases. [Recorded checks](../../results/gap-checks.json) and `tests/test_gap_papers.py` compare the formula against independent gcd enumeration.

1. NIST Digital Library of Mathematical Functions, §27.5, especially (27.5.2). [Möbius divisor identity](https://dlmf.nist.gov/27.5).
2. [Coupled Defect Moments and Exact Lattice Counts for AP-28](../../paper_ap28_coupled_bounds.md), Section 5, supplies the exact floor-sum counter.
