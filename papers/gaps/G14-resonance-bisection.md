# Resonance Bisection: LLL Finds the Right Resonances, but They Do Not Scale

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Status:** Experiment C1 of the [domain-ladder brainstorm](../../research/brainstorm-domain-ladder.md). Negative as a discovery method; one positive tool. No AP-28 is supplied.

### Abstract

Survivors of a sieve are periodic modulo the product $M$ of the sieve primes. The number of survivors in any interval is exactly a sum over frequencies of a product of local Dirichlet kernels. The brainstorm proposed to keep only the *resonant* frequencies, found by LLL, and to bisect toward survivors without enumerating dead cells. On an AP-10 analog we find that the resonance is real. LLL on the CRT dual finds frequencies carrying 20 to 60 times more of the count fluctuation than low-complexity frequencies do: 88% against 4% at sieve bound 23. But the share any fixed budget captures falls steadily as more sieve primes are added, and bisection guided even by the *optimal* frequencies costs hundreds to tens of thousands of times more than wheel enumeration. Resonance bisection is rejected as an AP-28 method.

### 1. Exact Fourier form of sieve counts

Fix $k=10$, $d=210$, and sieve primes $P$ ($2,3,5,7$ and $11\le p\le y$). A start $a$ survives when no term $a+210j$, $0\le j<10$, is divisible by a sieve prime. Let $G_p$ be the surviving residues and $M=\prod_{p\in P}p$. For $h \bmod M$ write $h/M\equiv\sum_p h_p/p \pmod 1$. Then

$$\#\{a\in[s,s+\ell):a\text{ survives}\}=\sum_{h \bmod M}c_h\,e\!\left(\frac{hs}{M}\right)\sum_{u<\ell}e\!\left(\frac{hu}{M}\right),\qquad c_h=\prod_{p\in P}\frac{\hat g_p(h_p)}{p}.$$

For $p\ge11$, $\hat g_p(0)=p-10$ and $\hat g_p(t)$ for $t\ne0$ is minus a Dirichlet kernel of length 10 at $t\cdot210/p$. A frequency is *resonant* when its local kernels are near their peaks and its interval phase $h/M$ is near zero. Writing $h_p=v_p\cdot210^{-1}\bmod p$ turns both conditions into "the $v_p$ are small and $\sum_p v_p\,210^{-1}/p$ is near an integer": a simultaneous approximation problem, solved by LLL.

The implementation reproduces exact counts from the full frequency sum (error below $10^{-8}$), and an exact pair-correlation formula gives the fluctuation variance over all window positions, so the share captured by any frequency set is exact rather than sampled.

### 2. Part A: optimal frequencies, full spectrum known

Sieve bound 23, so $M=223{,}092{,}870$. The window is $2^{20}$ starts beginning at $10^9$ and contains 542 survivors. Frequencies are ranked by $|c_h|\cdot|\text{interval kernel}|$ over the entire spectrum, which is the best any resonance finder could do.

Captured share of fluctuation variance and occupancy accuracy, by node length $\ell$ and number of frequencies $R$:

| $\ell$ | $R=16$ | $R=256$ | $R=4096$ | $R=65536$ |
|---:|---:|---:|---:|---:|
| 4096 | 0.54 (acc 0.91) | 0.85 (0.95) | 0.98 (0.99) | 1.00 (1.00) |
| 1024 | 0.49 (0.81) | 0.79 (0.92) | 0.95 (0.995) | 0.995 (1.00) |
| 256 | 0.31 (0.90) | 0.63 (0.96) | 0.88 (0.996) | 0.98 (1.00) |

End-to-end 4-ary bisection from $2^{20}$ down to leaves of 256 cells:

| $R$ | Survivors found | Fourier terms |
|---:|---:|---:|
| 256 | 414 / 542 | 778,752 |
| 4096 | 531 / 542 | 12,099,584 |
| 65536 | 542 / 542 | 193,069,056 |

A wheel through 17 visits 2,070 cells and checks each against 19 and 23, finding all 542. Even with perfect frequency selection, bisection costs about 380 to 93,000 times more and finds fewer survivors at the cheaper settings.

### 3. Part B: does resonance survive deeper sieves?

At the level $\ell^*$ where a node holds about one survivor, compare two frequency pools. The LLL pool takes all combinations with coefficients in $[-2,2]$ of the 8 shortest reduced vectors. The low-complexity pool takes every frequency active at the small primes plus at most two primes $\ge11$. Share of fluctuation variance captured by the best 65,536 frequencies of each pool:

| $y$ | $\ell^*$ | LLL pool | LLL share | Low-complexity pool | Its share |
|---:|---:|---:|---:|---:|---:|
| 23 | 2048 | 56,861 | 0.881 | 518,070 | 0.037 |
| 29 | 2048 | 75,821 | 0.779 | 982,590 | 0.028 |
| 31 | 4096 | 78,125 | 0.488 | 1,656,690 | 0.018 |
| 37 | 8192 | 78,125 | 0.255 | 2,692,410 | 0.009 |
| 41 | 8192 | 78,125 | 0.183 | 4,145,610 | 0.008 |
| 43 | 8192 | 78,125 | 0.143 | 6,024,270 | 0.007 |
| 47 | 16384 | 78,125 | 0.199 | 8,487,570 | 0.003 |

Larger LLL pools recover part of the loss, at rapidly growing pool cost:

| $y$ | Lattice dimension | Pool | Share (best 65,536) |
|---:|---:|---:|---:|
| 31 | 12 | 47,313 → 4,110,825 | 0.656 → 0.866 |
| 37 | 13 | 417,057 → 8,414,329 | 0.621 → 0.740 |
| 47 | 16 | 1,120,491 → 10,049,427 | 0.314 → 0.445 |

### 4. What this shows

**The positive part.** Resonance in the CRT dual is real, and LLL finds it. With 16 frequencies at $y=23$, LLL captures 61% of the fluctuation that decides where survivors are; the low-complexity frequencies capture 2%. This is the domain where the project's original "LLL plus resonance" intuition is meaningful. Zeta-zero phases near the start were not.

**The negative part.** The information deciding whether a short node holds a survivor is spread over frequency supports that grow with every added sieve prime. Each prime $p$ is active in a significant frequency with weight about $10/p$ for AP-10, or $28/p$ for AP-28, so the number of relevant supports grows like $\prod_p(1+10/p)$. Each support needs its own resonant combination, and the LLL pool must grow exponentially in the lattice dimension to keep up. By contrast, wheel enumeration followed by filtering costs about $\delta_{\rm wheel}/\delta(y)$ cells per survivor, which grows only polylogarithmically in $y$. For AP-28 the comparison is worse still.

**Verdict.** Resonance bisection does not beat the wheel at any tested size and its trend runs the wrong way. It is rejected as an AP-28 discovery method. The LLL resonance finder is kept as a tool: it extracts the structured part of a sieve's spectrum cheaply, which may matter for ideas 4, 5 and 11 of the brainstorm.

### Reproduction

`python3 -m research.resonance_bisection` (a few minutes) writes [resonance-bisection.json](../../results/resonance-bisection.json). `tests/test_resonance_bisection.py` checks the exact Fourier reconstruction of interval counts, the pair-correlation variance against a full period, Parseval, and the frequency generators.
