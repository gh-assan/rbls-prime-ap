# Resonance-Biased Lattice Sieving: An Exploratory Heuristic for Locating Prime Arithmetic Progressions

**Author:** Ghassan Al Hamoud
**Location:** Berlin, Germany
**Date:** May 2026

### Abstract

The search for long arithmetic progressions of primes (AP-$k$) is a computationally intensive problem usually approached through discrete sieving, wheel constraints, and large-scale parallel search. This note describes Resonance-Biased Lattice Sieving (RBLS), an exploratory heuristic that uses a low-dimensional lattice construction from the phases of the first Riemann zeta zeros to choose reproducible starting regions for prime-progression searches. The method is not presented as a theorem or as a proven statistical accelerator. Its current value is experimental: it combines an analytic target generator with deterministic Miller-Rabin sieving, and it produced verified AP-7 and AP-8 examples near $10^{15}$ with common difference $210$. A subsequent AP-9 search over roughly $7 \times 10^9$ raw candidates did not find a progression. Reinterpreted against a Hardy-Littlewood-style baseline, these results are compatible with ordinary AP densities and should be viewed as a starting point for controlled baseline experiments rather than evidence of a large speedup.

---

### 1. Introduction

The Green-Tao theorem establishes that the primes contain arbitrarily long arithmetic progressions. The theorem is non-constructive, and practical searches for long prime progressions rely on careful arithmetic constraints and high-throughput computation. Record searches, including PrimeGrid AP searches, use primorial structure and massive parallelism to reduce a very sparse search problem to a tractable distributed computation.

This note proposes and tests a heuristic targeting layer, Resonance-Biased Lattice Sieving (RBLS). The idea is to use a small number of low-frequency Riemann-zero phases to select a logarithmic region, then run an ordinary discrete AP sieve in that region. RBLS does not replace primality testing, does not prove elevated prime density, and does not currently establish a statistically significant advantage over standard structured search. The contribution is a reproducible experimental pipeline and a set of observations that can be tested against random and residue-class baselines.

### 2. Theoretical Framework

#### 2.1 Analytic Phase Motivation

The explicit formula for prime-counting functions expresses fluctuations in prime distribution through the non-trivial zeros of $\zeta(s)$. A short truncation of the zero sum is far too coarse to predict individual primes near $10^{15}$, but it can be used as a source of low-frequency phase information.

For a progression starting at $a$ with common difference $d$, the phase contributed by a zero with imaginary part $t_i$ depends on

$$t_i \log(a + jd).$$

When $d \ll a$,

$$\log(a + jd) = \log a + j\frac{d}{a} + O\left(\frac{j^2d^2}{a^2}\right).$$

Thus, over the short spans considered here, the terms in the progression share almost the same logarithmic phase. RBLS uses this observation only as a heuristic for choosing a search region.

#### 2.2 LLL Target Generation

Let $\alpha_i = t_i / 2\pi$ for the first three non-trivial zeros. The implementation constructs an integer lattice from the scaled values $\lfloor C\alpha_i \rceil$, with $C = 10^8$:

$$M = \begin{bmatrix}
C & 0 & 0 & 0 \\
0 & C & 0 & 0 \\
0 & 0 & C & 0 \\
\lfloor C\alpha_1 \rceil & \lfloor C\alpha_2 \rceil & \lfloor C\alpha_3 \rceil & 1
\end{bmatrix}.$$

LLL reduction returns short vectors whose final coordinate is treated as a candidate denominator $q$. The code then scales $q$ to a logarithmic magnitude close to $\log(10^{15})$ and converts the resulting $y$ to a target $a_{\text{target}} = \lfloor e^y \rfloor$.

This construction should be interpreted cautiously. Scaling an LLL-derived denominator to a prescribed magnitude does not by itself prove strong phase alignment at that magnitude. In the current implementation, it is best described as a deterministic target generator inspired by simultaneous Diophantine approximation.

#### 2.3 Parameter Choices

**Number of zeros ($N=3$):** Three zeros give the smallest non-trivial lattice used in this implementation. This is a computational choice, not an optimized theoretical parameter. In particular, the current experiments do not prove that three zeros are better than two, four, or five. A publishable statistical claim would require a sensitivity study over $N$.

**Scaling constant ($C=10^8$):** The scale $C$ maps floating-point approximations of $\alpha_i$ into integer lattice entries. It is large enough to preserve several decimal places while keeping the lattice small and fast to reduce. Robustness to $C$ should be measured directly rather than assumed.

**Lattice dimension:** The current 4D lattice contains three zero-phase coordinates and one denominator coordinate. Higher-dimensional versions may encode more zeros, but simultaneous approximation becomes more restrictive and may produce targets that are not meaningfully better for this application.

**Primorial step:** For an AP-$k$ at large magnitude, the common difference must be divisible by every prime $p \leq k$ unless the progression starts at the prime $p$ itself. Otherwise the $k$ consecutive residues $a, a+d, \ldots, a+(k-1)d \pmod p$ include $0$, forcing one term to be composite. For AP-7, this requires $d$ to be divisible by $2,3,5,7$, so the smallest admissible primorial step is $210$. AP-8 and AP-9 also use $d=210$.

### 3. Computational Methodology

The pipeline has two stages.

1. **Target generation:** Python and SymPy construct the lattice above, run LLL, and produce one or more starting regions near $10^{15}$.
2. **Discrete search:** CUDA/PyCUDA or Numba evaluates candidate starts. For each candidate $a$, it tests

$$a,\; a+d,\; a+2d,\; \ldots,\; a+(k-1)d$$

using deterministic Miller-Rabin witnesses valid for 64-bit integers. The GPU and CPU implementations use overflow-safe modular multiplication; variants use either shift/add multiplication or equivalent 64-bit-safe modular arithmetic.

Because $d=210$ is even, even starting values are skipped in the optimized CPU/M1 searches.

### 4. Empirical Results

#### 4.1 AP-7 Benchmark

In May 2026, the RBLS pipeline generated a target region near

$$a_{\text{target}} \approx 999,721,403,904,414.$$

The GPU search evaluated batches of $10,000,000$ raw candidate starts and found a valid AP-7 in the sixth batch, after roughly $60,000,000$ raw candidates. The recorded GPU execution time was 139.44 seconds.

| Index ($n$) | Term ($a_n$) | Status |
| --- | --- | --- |
| 0 | 999,721,467,601,817 | Prime |
| 1 | 999,721,467,602,027 | Prime |
| 2 | 999,721,467,602,237 | Prime |
| 3 | 999,721,467,602,447 | Prime |
| 4 | 999,721,467,602,657 | Prime |
| 5 | 999,721,467,602,867 | Prime |
| 6 | 999,721,467,603,077 | Prime |

The progression is

$$a_n = 999,721,467,601,817 + 210n,\qquad 0 \leq n \leq 6.$$

All seven terms were verified independently with CPU-side Miller-Rabin and trial division checks.

#### 4.2 AP-8 Follow-Up

The AP-8 search used the same primorial step $d=210$ and the same target-generation mechanism. The M1/Numba implementation searched odd starting values in batches of $5,000,000$ raw candidates. A valid AP-8 was found in the 46th of 50 allocated batches, after approximately $2.28 \times 10^8$ raw candidate positions from the starting target.

| Metric | Value |
|--------|-------|
| Batch size | $5,000,000$ raw candidates |
| Batches allocated | 50 |
| Batch containing discovery | 46 |
| Raw candidate range allocated | $250,000,000$ |
| Approximate odd candidates tested before discovery | $1.14 \times 10^8$ |
| Search time | about 6 minutes 51 seconds |

| Index ($n$) | Term ($a_n$) | Status |
| --- | --- | --- |
| 0 | 999,721,631,514,707 | Prime |
| 1 | 999,721,631,514,917 | Prime |
| 2 | 999,721,631,515,127 | Prime |
| 3 | 999,721,631,515,337 | Prime |
| 4 | 999,721,631,515,547 | Prime |
| 5 | 999,721,631,515,757 | Prime |
| 6 | 999,721,631,515,967 | Prime |
| 7 | 999,721,631,516,177 | Prime |

The progression is

$$a_n = 999,721,631,514,707 + 210n,\qquad 0 \leq n \leq 7.$$

All eight terms were verified with deterministic Miller-Rabin and independently checked with SymPy's `isprime()`.

#### 4.3 AP-9 Negative Result

The AP-9 searches used $d=210$ and covered approximately $7 \times 10^9$ raw candidate starts across multiple target windows. No AP-9 was found. Under the corrected baseline in Section 5, this miss is not decisive evidence against the code or the heuristic; it is compatible with expected AP-9 rarity at this magnitude.

### 5. Statistical Interpretation

The original independence estimate must be handled carefully. For fixed $d=210$, all terms in the progression share the same residue modulo each prime dividing $d$. Therefore the factor $\phi(d)/d$ is not paid independently for every term.

A more appropriate baseline is the Hardy-Littlewood prime $k$-tuple heuristic. For the tuple

$$H_k = \{0,d,2d,\ldots,(k-1)d\},$$

the approximate probability that a raw starting value near $x$ gives an AP-$k$ is

$$P(\text{AP-}k) \approx \frac{\mathfrak{S}(H_k)}{(\log x)^k},$$

where $\mathfrak{S}(H_k)$ is the singular series

$$\mathfrak{S}(H_k)=\prod_p \frac{1-\nu_p(H_k)/p}{(1-1/p)^k},$$

and $\nu_p(H_k)$ is the number of distinct residues occupied by $H_k$ modulo $p$.

Using a truncated singular-series computation for $d=210$ near $x=10^{15}$ gives the following rough expectations:

| $k$ | Partial $\mathfrak{S}(H_k)$ | Expected raw starts per success | Observed result |
|-----|------------------------------|---------------------------------|-----------------|
| 7 | $\approx 2.59 \times 10^3$ | $\approx 2.26 \times 10^7$ | Found after $\sim 6.0 \times 10^7$ raw starts |
| 8 | $\approx 7.13 \times 10^3$ | $\approx 2.84 \times 10^8$ | Found after $\sim 2.28 \times 10^8$ raw starts |
| 9 | $\approx 1.61 \times 10^4$ | $\approx 4.34 \times 10^9$ | Not found after $\sim 7.0 \times 10^9$ raw starts |

These estimates are approximate, but they materially change the interpretation. The AP-7 and AP-8 discoveries validate that the implementation can find genuine progressions, yet they do not establish a large speedup over structured baseline search. The AP-9 miss is also not surprising enough to invalidate the pipeline.

#### 5.1 Required Baselines

To test whether RBLS provides a real advantage, future work should compare LLL-selected windows against controls using the same implementation and stopping rules:

1. Random windows near $10^{15}$.
2. Deterministic grid windows with the same residue constraints.
3. Multiple LLL targets generated by changing $N$, $C$, and the target magnitude.

The primary metric should be candidates-to-first-success, with censored runs handled by a survival-analysis or rank-based test. Reporting only successful runs would overstate the evidence.

#### 5.2 Local Prime Density

A second test is local prime density. For each target window $[a,a+W]$, count primes and compare with both $W/\log a$ and matched random windows. This tests whether the target generator predicts prime-rich regions independently of the AP search.

### 6. Scalability and Limitations

#### 6.1 Primorial Growth

For progression length $k$, the required primorial step is

$$d = \prod_{p \leq k} p.$$

| $k$ | $d$ | $\phi(d)/d$ | Spread $(k-1)d$ |
|-----|-----|-------------|------------------|
| 7 | 210 | 0.2286 | 1,260 |
| 8 | 210 | 0.2286 | 1,470 |
| 9 | 210 | 0.2286 | 1,680 |
| 14 | 30,030 | 0.1918 | 390,390 |
| 28 | 223,092,870 | 0.1636 | 6,023,507,490 |

As $k$ grows, direct AP testing becomes increasingly expensive because each surviving candidate can require many primality tests.

#### 6.2 Phase Drift

For AP-28 with $d \approx 2.23 \times 10^8$ and $a \approx 10^{15}$, the total logarithmic span is approximately

$$\frac{27d}{a} \approx 6.0 \times 10^{-6}.$$

This is small, so first-order phase drift is not the immediate bottleneck for the experiments here. The larger limitation is that the present LLL scaling procedure has not yet been shown to select statistically better windows.

#### 6.3 Direct Test vs. Prime-Find-Then-Scan

For larger $k$, a "prime-find then scan" strategy can be preferable. It tests each integer once, collects primes in a window, and scans the resulting set for arithmetic patterns. This trades repeated Miller-Rabin evaluations for hash lookups over the prime set. The AP-28 prototype follows this direction, but a corrected AP-28 run requires a window wider than $6.0 \times 10^9$ integers for the minimal admissible step, so a practical implementation should use segmented storage rather than keeping the full prime set in memory.

#### 6.4 Scope

The same experimental framework could be adapted to other prime constellations, but each pattern would need its own admissibility constraints, baseline model, and control experiments.

### 7. Conclusion

RBLS is best viewed as an exploratory computational framework. It successfully found verified AP-7 and AP-8 progressions near $10^{15}$ and produced a useful negative AP-9 experiment. After correcting the statistical baseline, the current evidence supports the correctness of the search implementation but does not yet prove that the LLL target generator improves over ordinary structured sampling.

The next step is therefore not a stronger claim, but a cleaner experiment: run matched random and deterministic baseline windows, report all misses, and compare candidates-to-success under identical stopping rules. If RBLS consistently outperforms those controls, the resonance hypothesis becomes a serious empirical result. Until then, the method should be published as an open, reproducible heuristic and a call for independent testing.

### Acknowledgements

The GPU-accelerated AP-7 search was conducted on an NVIDIA Tesla T4 hosted on Windows. The AP-8 and AP-9 M1 searches were executed on Apple Silicon using Numba JIT compilation with parallel CPU execution. The author thanks the open-source maintainers of SymPy, PyCUDA, and Numba.

### References

1. Green, B., & Tao, T. (2008). The primes contain arbitrarily long arithmetic progressions. *Annals of Mathematics*, 167(2), 481-547.
2. Lenstra, A. K., Lenstra, H. W., & Lovász, L. (1982). Factoring polynomials with rational coefficients. *Mathematische Annalen*, 261(4), 515-534.
3. Hardy, G. H., & Littlewood, J. E. (1923). Some problems of 'Partitio Numerorum'; III: On the expression of a number as a sum of primes. *Acta Mathematica*, 44, 1-70.
4. Davenport, H. (2000). *Multiplicative Number Theory* (3rd ed.). Springer-Verlag.
5. Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function. *Proceedings of Symposia in Pure Mathematics*, 24, 181-193.
6. Lagarias, J. C., & Odlyzko, A. M. (1987). Computing $\pi(x)$: An analytic method. *Journal of Algorithms*, 8(2), 173-191.
7. Pomerance, C., Selfridge, J. L., & Wagstaff, S. S. (1980). The pseudoprimes to $25 \cdot 10^9$. *Mathematics of Computation*, 35(151), 1003-1026.
