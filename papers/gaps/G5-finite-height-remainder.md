# Finite-Height Remainders and Hidden Tail Divisors

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Gap G5, also G3b:** Open. This note proves a concrete obstruction to one inference from local data; it does not bound the arithmetic remainder for a complete AP-28 search family.

### Abstract

A rigorous local-factor constant does not establish a finite-height count. We demonstrate the distinction with an actual arithmetic family near $10^{15}$: all 28 terms avoid every prime at most 37, yet the first term is always divisible by 41. The Chinese remainder construction extends to every fixed finite initial sieve at sufficiently large heights. A full prime-tuple model that includes the forced tail divisor correctly has a zero local factor, so this example does not contradict that model. It shows why finite local profiles or an accurately computed unconditioned constant cannot certify a selected family's prime count. We state the exact additional remainder estimate required for closure and record which attempted arguments do not supply it.

### 1. The unbounded quantity

For a precisely specified family $\mathcal R_X$, let $N_{28}(X)$ be its actual prime-progression count. A model may suggest a main term $H(X)$, but existence requires information about

$$E(X)=N_{28}(X)-H(X).$$

If $H(X)>0$, a proved lower bound $E(X)>-H(X)$ would imply existence. Neither a conjectured positive main term nor an enclosure of its Euler-product constant supplies that lower bound.

For the cubic certificate, an equivalent finite target is to control

$$S_X=R-M_1+\frac56M_2-\frac12M_3$$

well enough to prove $S_X>0$. The required control concerns the actual family and its selection rules, not only a model with the same small-prime density.

### 2. An actual locally admissible but composite family

For AP-28 set

$$D=223092870,\qquad Q=29\cdot31\cdot37=33263.$$

Impose

$$a\equiv1\pmod D,\qquad a\equiv D\pmod Q,\qquad a\equiv0\pmod{41}.$$

The moduli are pairwise coprime. CRT gives

$$a\equiv125393140162291\pmod{304250263527210}.$$

A start just above $10^{15}$ in this class is

$$a_*=1038143930743921
=41\cdot25320583676681.$$

Consider $a_*+t\cdot304250263527210+jD$ for $0\le t<10$, $0\le j<28$.

For $p\mid D$, each term equals 1 modulo $p$. For $p\in\{29,31,37\}$, each term equals $(j+1)D$ modulo $p$, which is nonzero because $1\le j+1\le28<p$. Thus **every term passes the entire sieve through 37**.

But every starting term is divisible by 41 and exceeds 41. All ten candidate progressions therefore have a composite term. Their largest terms remain below $2^{64}$.

The statement is established by exact congruences and division, not by a probabilistic primality test. The complete parameters and cofactors are in [gap-checks.json](../../results/gap-checks.json).

### 3. The general CRT obstruction

Fix $k$, a difference $D$ containing every prime at most $k$, and a finite $B\ge k$. Let $Q$ be the product of primes $k<p\le B$ not dividing $D$, and choose a prime $q>B$ not dividing $D$. Impose

$$a\equiv1\pmod D,\qquad a\equiv D\pmod Q,\qquad a\equiv0\pmod q.$$

If $D$ contains extra primes above $k$, all primes dividing $D$ use the first congruence and are omitted from $Q$. The moduli are again coprime. Each term $a+jD$, $0\le j<k$, avoids every prime at most $B$, while the first term is composite once $a>q$.

This produces infinitely many such starts without any assertion about the primality of the other terms. The construction uses only CRT [1]. Its required height can grow enormously with $B$; it does **not** assert that such counterfamilies fit below a fixed height for every sieve bound. A sieve through the square root of a bounded term can, of course, completely decide its primality.

### 4. What is and is not refuted

The example refutes the inference that avoiding a fixed finite set of prime obstructions, together with favorable sizes, is by itself a certificate of simultaneous primality in a selected family.

It does not refute the complete singular-series model. Parameterize this particular family by $t$. The first linear form is identically zero modulo 41, so its full local factor at 41 is zero. A correctly conditioned model includes that obstruction.

Nor is it evidence that the unrestricted two-variable AP-28 count has an unexpectedly large negative remainder. The selected family has an explicit extra constraint that the unrestricted family lacks.

The lesson is precise: a selection procedure must preserve and document its arithmetic conditioning. Undetected tail restrictions cannot be replaced by an unconditioned local constant.

### 5. Attempts that do not close this gap

- **A more accurate Euler product:** [G3](G3-euler-product-errors.md) bounds the constant, but does not bound $E(X)$.
- **An individual lattice volume estimate:** the third paper proves that five-tail intersections in the 64-bit regime are too sparse for uniform small relative error.
- **Agreement with independent low-order moments:** the third paper gives an exact five-wise independent countermodel with no zero-defect outcome.
- **A faster exact count of one cell:** this leaves the number of relevant cells, origin corrections, and tail labels to control.
- **A logarithmic localization query count:** [G4](G4-witness-localization.md) still needs a valid positive score and an adequate arithmetic oracle.

These are proved or explicit limitations of particular arguments. They are not a theorem that the underlying AP-28 task is impossible.

### 6. What would close the gap

A complete resolution would need at least one of the following, for a stated family and domain:

1. a verified AP-28 witness;
2. a positive exact completion score with complete coverage and a valid localization route;
3. signed arithmetic bounds with errors small enough to make a valid completion certificate positive;
4. a proved finite-height count lower bound greater than zero, followed by a constructive witness procedure.

No such AP-28 result is supplied in this series so far. This note closes an incorrect inference, not the prime-count remainder. The gap remains explicitly open in [the ledger](../../GAP_LEDGER.md).

### Reproduction and reference

`research/hidden_tail_family.py` constructs and verifies the arithmetic family. `research/run_gap_checks.py` records it alongside the completed finite checks.

1. AtCoder Library, *Math: crt*. [Official CRT specification](https://atcoder.github.io/ac-library/production/document_en/math.html). The construction and its congruence verification are proved directly above.
