# How Far Is an AP-28? A Calibration Against Actual Record Counts

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Status:** Calibration and route assessment. The model numbers are heuristic. The PrimeGrid counts and local sieve fractions are actual data and exact products. No AP-28 is supplied.

### Abstract

PrimeGrid's program has found 71 AP-26s, 4 AP-27s and no AP-28. A two-parameter window model of that program reproduces the observed AP-26 to AP-27 ratio from an independently computed neighbor probability: 15.9 predicted against 17.75 observed. The same model predicts about 20 maximal AP-27s per AP-28, with a data-only range of 8 to 86. Below $2^{64}$ the density model expects about 13.6 AP-28s among $2.8\times10^{28}$ admissible cone cells, so isolating one takes about 91 bits of information. Exact local sieve fractions show what congruence conditions can supply cheaply: 36 bits through 541, leaving $2.7\times10^{16}$ cells per expected AP-28. We conclude that no known mathematical method produces an AP-28 without a search of roughly PrimeGrid's size, and that this is a limit of current mathematics, not of this repository's papers.

### 1. Actual data

PrimeGrid's [AP26/AP27 statistics](https://www.primegrid.com/stats_ap26.php), accessed 29 October 2026:

| Length | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Found | 1723364 | 413368 | 93527 | 20660 | 4144 | 663 | 71 | 4 | 0 |

The four AP-27s are dated 23 September 2019, 26 May 2023, 10 December 2023 and 2 August 2026. [G12](G12-record-extension-census.md) proves none extends. The [record table](https://www.pzktupel.de/PAP/aprecords.php), updated 12 October 2026, still lists 27 as the longest known length.

### 2. A window model of the program

The program fixes a 24-term core, already sieved, and tests the 28-term window $n-2D,\ldots,n+25D$ ([G12, Section 3](G12-record-extension-census.md)). Suppose the core is prime and each of the four outer terms is independently prime with probability $q$. Enumerating the 16 outer patterns gives the maximal lengths

$$\frac{P_{26}}{P_{27}}=\frac{3-q}{2q},\qquad \frac{P_{27}}{P_{28}}=\frac{2(1-q)}{q}.$$

`tests/test_ap28_distance.py` checks both identities exactly with rational $q$.

**Data estimate.** Solving $(3-q)/(2q)=71/4$ gives $q=12/146\approx0.082$ and $P_{27}/P_{28}\approx22.3$. The exact 95% Poisson interval for 4 events, $[1.09,10.24]$, widens this to between 7.9 and 85.5 maximal AP-27s per AP-28.

**Independent model estimate.** For the one neighbor of an AP-27 that survives modulo 29, the prime-tuple heuristic gives

$$q(N)=\frac{1}{\log N}\prod_{p\le23}\frac p{p-1}\cdot\frac{29}{28}\prod_{p\ge31}\frac p{p-1}\cdot\frac{p-27}{p-26}.$$

The product over $p\ge31$ is $0.598$ (primes below $10^7$). At the record heights $2\times10^{17}$ to $2\times10^{18}$, $q$ lies between 0.090 and 0.095, giving 19.0 to 20.3 maximal AP-27s per AP-28.

**Check.** The model value $q(10^{18})=0.091$ predicts $P_{26}/P_{27}=15.9$. PrimeGrid observed 17.75, well inside Poisson noise. This is an actual-count consistency check of the density model at the relevant height. It is evidence, not the finite-height theorem G3b/G5 asks for.

### 3. What this means in time

PrimeGrid found its four AP-27s over seven years. At that rate, and with about 20 AP-27 finds expected per AP-28, the expected wait for the program's first AP-28 is several decades of PrimeGrid throughput. A dedicated AP-28 sieve reduces candidates by about 7.75 times according to the [Illinois report](https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf). That shortens the wait by at most a constant factor and does not change its order. The exact rate of PrimeGrid's search is not public in the sources read here, so these are order-of-magnitude statements.

### 4. The information budget

Below $X=2^{64}-1$ with $23\#\mid d$, the cone of [G7](G7-structural-analytic-route.md) has $V(X)=2.82\times10^{28}$ cells. The model count of AP-28s is $13.59$, inside the rigorous enclosure $[13.270,13.876]$ of [G11](G11-sparsity-confidence-audit.md). For comparison the model gives 3572 AP-26s and 241 AP-27s. Isolating one AP-28 therefore needs $\log_2(V/13.59)\approx90.7$ bits.

Congruence information is the cheapest kind. At $p\le23$ only $a$ must be a unit; at $p\ge29$ the surviving fraction is exactly $(p-1)(p-27)/p^2$. The cumulative information is:

| Primes through $y$ | Bits | Cells left per expected AP-28 |
|---:|---:|---:|
| 23 | 2.6 | $3.4\times10^{26}$ |
| 59 | 17.7 | $9.6\times10^{21}$ |
| 541 | 36.2 | $2.7\times10^{16}$ |
| $10^4$ | 51.5 | $6.4\times10^{11}$ |
| $10^6$ | 67.9 | $7.8\times10^{6}$ |
| $10^7$ | 74.1 | $1.0\times10^{5}$ |

Large $y$ would leave few cells, but reaching them is the problem. The surviving classes of $(a,m)$ modulo $\prod_{p\le y}p$ outnumber the cells of the box from $y=47$ on, so most classes contain no cell at all. Meet-in-the-middle matching of CRT classes for a fixed difference costs at least $\sqrt{\varphi(23\#)\prod_p(p-28)}$, which exceeds the number of survivors it outputs from $y=83$ on. Up to that point CRT enumeration is output-sensitive; PrimeGrid already enumerates through 59, and pushing to 79 would add only about 3.7 bits. Beyond it, the only known way to apply a congruence is to visit the cells, which is a sieve, which is a search.

### 5. Why no search-free construction is available

1. **Existence below a checkable height is unproved.** Green and Tao bound the first prime AP-$k$ only by a tower of exponentials [1]. Quantitative refinements [G7, G10] still need heights far beyond any where a witness could be checked. The expectation of about 13 AP-28s below $2^{64}$ is a heuristic, not a theorem.
2. **Even one prime is not constructible deterministically.** No deterministic polynomial-time algorithm is known that outputs a prime with a prescribed number of digits; this was the subject of Polymath4 [2]. An AP-28 asks for 28 primes under a linear constraint.
3. **Congruences never force primality.** Every finite set of local conditions admits composite progressions ([G5](G5-finite-height-remainder.md), [G8](G8-power-exclusion.md)). Section 4 measures how much those conditions can say.
4. **Structured selections do no better than local densities.** The Green–Tao–Ziegler theory shows that, after the local W-trick, primes do not correlate with bounded-complexity structured sequences [3]. Lattice, LLL, or zeta-zero targeting is a selection of this kind and asymptotically gains nothing beyond local factors. The repository's own LLL experiments agree ([review](../../research/review-2026-10-28.md)).
5. **Known near-records do not extend** ([G12](G12-record-extension-census.md)).

### 6. Verdict

The analytic gaps G2 and G3b/G5 would require an explicit finite-height lower bound for a 28-form prime pattern. No such bound is known for any pattern of this kind at reachable heights, and no current technique is close. The constructive route needs either that bound or a search. An explicit AP-28 is an open computational problem that the largest volunteer prime search has not solved after a decade.

A path to an actual AP-28 exists only if the search-free requirement is relaxed. The realistic options are to contribute to PrimeGrid's AP27 search, whose program already tests every window an AP-28 could occupy, or to run a dedicated AP-28 sieve in the style of the Illinois report. Both are search methods. Either way, success on personal hardware is unlikely without decades of collective computation.

### Reproduction

`python3 -m research.ap28_distance` (about one minute) writes [ap28-distance.json](../../results/ap28-distance.json). `tests/test_ap28_distance.py` checks the window identities, the Poisson interval, the quadrature against G11's enclosure and the local-information table.

### References

1. Green, B., and Tao, T. *The primes contain arbitrarily long arithmetic progressions*. Annals of Mathematics 167 (2008). The introduction gives the tower bound for the first AP-$k$.
2. Tao, T., Croot, E., and Helfgott, H. *Deterministic methods to find primes*. Mathematics of Computation 81 (2012).
3. Green, B., and Tao, T. *Linear equations in primes*, Annals of Mathematics 171 (2010); Green, Tao and Ziegler, *An inverse theorem for the Gowers $U^{s+1}[N]$-norm*, Annals of Mathematics 176 (2012).
4. PrimeGrid AP26/AP27 statistics: <https://www.primegrid.com/stats_ap26.php>
5. Mok, Bradu, Rojas, Desai, Zhen. *Developing Software to Find Arithmetic Progressions of 28 Primes*, Illinois Mathematics Lab, May 2025: <https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf>
