# Certified Euler-Product Errors for the AP-28 Model

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Gap G3a:** The truncation error in the stated local-factor products is resolved.  
**Gap G3b:** The discrepancy between the resulting finite-height model and actual AP-28 counts remains open.

### Abstract

Earlier notes used a local-factor product truncated at 100000 without a rigorous enclosure of its infinite tail. We derive elementary, explicit bounds for the two-variable AP-28 product and for its ratio to the fixed-difference singular series. Positive rational factors are multiplied with outward rounding, so both the finite calculation and the infinite-tail correction are enclosed rigorously. The resulting two-variable constant lies between approximately $3.31294\times10^{18}$ and $3.32463\times10^{18}$. The variable-versus-fixed local-factor ratio lies between $3.549438062740978869797$ and $3.550396938396844835386$. These are bounds on constants, not on an actual finite-height AP-28 count. We separate the two errors explicitly.

### 1. The product being bounded

Let $r=k-1=27$ and $D=23\#$. The two-variable local factor is

$$\beta_p=\begin{cases}
(1-1/p)^{-r},&p\mid D,\\
\dfrac{1-r/p}{(1-1/p)^r},&p\nmid D.
\end{cases}$$

Define $\beta_P=\prod_{p\le P}\beta_p$ and $\beta_\infty=\prod_p\beta_p$. Every prime at most 28 divides $D$, so all factors are positive. The tail bounds below also establish positive convergence.

The local product is the one used in the earlier two-variable count model and is consistent with the prime-tuple modeling approach in the AP-28 literature [1]. Its definition does not imply a finite-height count formula.

### 2. A rigorous tail inequality

For $p>P$ with $P$ containing all prime factors of $D$, put $t=1/p$ and

$$f(t)=r\log(1-t)-\log(1-rt)=-\log\beta_p.$$

Then

$$f'(t)=\frac{r(r-1)t}{(1-t)(1-rt)}.$$

For $0\le t<1/r$, integration gives

$$0\le f(t)\le\frac{r(r-1)t^2}{2(1-t)(1-rt)}.$$

Also $\sum_{p>P}p^{-2}\le\sum_{n>P}n^{-2}\le1/P$. Consequently

$$0\le-\log\frac{\beta_\infty}{\beta_P}\le
\varepsilon_P:=\frac{r(r-1)}{2P(1-1/(P+1))(1-r/(P+1))}.$$

For $\varepsilon_P<1$ this gives the convenient rational enclosure

$$\boxed{\beta_P(1-\varepsilon_P)\le\beta_\infty\le\beta_P.}$$

The lower bound uses $e^{-x}\ge1-x$. It is slightly weaker than the exponential enclosure but avoids numerical evaluation of an exponential.

At $r=27$, $P=100000$,

$$\varepsilon_P=\frac{3510070200351}{999740000000000}.$$

This is an unconditional bound on the omitted product, without an assumption about the distribution of primes in short intervals.

### 3. A sharper ratio bound

Let $S_{28,P}(D)$ be the partial singular series for the fixed difference $D$. At primes dividing $D$ its factor equals that in $\beta_P$. At other primes,

$$\frac{\beta_p}{S_{28,p}(D)}
=\frac{(1-27/p)(1-1/p)}{1-28/p}
=1+\frac{27}{p(p-28)}.$$

Thus, for $R_P=\beta_P/S_{28,P}(D)$, the infinite tail is positive. The inequality $\log(1+x)\le x$ gives

$$0\le\log\frac{R_\infty}{R_P}\le
\eta_P:=\frac{27}{P(1-28/(P+1))}.$$

Since $e^x\le1/(1-x)$ for $0\le x<1$,

$$\boxed{R_P\le R_\infty\le\frac{R_P}{1-\eta_P}.}$$

At $P=100000$, $\eta_P=2700027/9997300000$. This is more informative for the ratio than dividing separate broad enclosures for the two constants.

### 4. Outward-rounded finite calculations

Each finite factor is an exact positive rational. For example, when $p\nmid D$,

$$\beta_p=\frac{(p-27)p^{26}}{(p-1)^{27}}.$$

The checker maintains a lower product rounded downward and an upper product rounded upward at every multiplication and division. Decimal conversion of the integer numerators and denominators is exact. Directed rounding therefore encloses the rational product inductively; no binary floating-point approximation is accepted as a proof bound.

Using 60-digit working precision and rounding the displayed endpoints outward gives

$$3.312948771602789797972\times10^{18}
\ \le\beta_\infty\le\ 
3.324621461220568134309\times10^{18},$$

and

$$3.549438062740978869797
\ \le R_\infty\le\ 
3.550396938396844835386.$$

The exact rational endpoints underlying these displayed decimal bounds are stored in [gap-checks.json](../../results/gap-checks.json). The finite partial ratio is approximately $3.5494380627409788697974$; the infinite ratio is at least that partial value.

Tests compare small products against exact rational arithmetic, nest higher-precision enclosures, and check that later partial products remain within the predicted earlier tail enclosure.

### 5. Why this does not certify a finite AP-28 count

Let

$$I(X)=\iint_{\mathcal T_X}\frac{da\,dm}{\prod_{j=0}^{27}\log(a+jDm)}.$$

The previous numerical model uses $\beta_PI(X)$. Its relation to an actual count can be written as the exact bookkeeping identity

$$N_{28}(X)-\beta_PI(X)
=\underbrace{N_{28}(X)-\beta_\infty I(X)}_{\text{arithmetic discrepancy}}
+\underbrace{(\beta_\infty-\beta_P)I(X)}_{\text{Euler-tail error}}.$$

This paper bounds the second term, provided the integral itself is enclosed. Numerical quadrature has a separate error and also needs certification if it enters a proof. No bound for the first term follows from the Euler-product calculation.

In particular, replacing the earlier model constant by this rigorous interval does not prove that there are roughly 13.59 AP-28s below the 64-bit limit, or even one. An accurate constant can multiply an unproved finite-height approximation.

**Resolution:** G3a is closed for the stated products and parameters. G3b remains an arithmetic gap. [Finite-height remainders and hidden tail divisors](G5-finite-height-remainder.md) treats that gap separately; it is also connected to [signed aggregation](G2-signed-aggregation.md). No count-level claim has been upgraded to a theorem.

### References and reproduction

1. Mok et al. (2025). *Developing Software to Find Arithmetic Progressions of 28 Primes*, Section 5. [Primary project report](https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf).
2. The product definitions are derived in [the projective-lattice paper](../../paper_projective_ap28.md). The tail inequalities above are proved directly and are not asserted to be new general Euler-product techniques.

Run `python3 research/euler_tail_bounds.py` or `python3 research/run_gap_checks.py` to reproduce the enclosures.
