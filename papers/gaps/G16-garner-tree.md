# Garner Tree Search Is the Wheel, up to a Constant

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Status:** Experiment for idea 25 of the [domain-ladder brainstorm](../../research/brainstorm-domain-ladder.md). Negative as a discovery method; one small practical constant. No AP-28 is supplied.

### Abstract

In mixed radix, the condition at the $i$-th sieve prime involves only the first $i$ digits (Garner's algorithm), so a tree can fix one digit per prime and prune any class with no representative in the search window. We measure this tree on an AP-10 analog with exact work accounting for five prime orders, every switch depth and sieve bounds from 23 to 541. The best tree uses 77% to 88% of the wheel's work at every bound, a constant saving that does not grow. We prove why: once the modulus exceeds the window, each further level changes the work by exactly $S_i(|G_p|-2)+S_{i+1}$, where $S_i$ counts window cells surviving the first $i$ primes. Deeper trees therefore lose for every prime with at least two allowed residues. The tree is the wheel in other words. The only lasting lesson is to order sieve primes by survival fraction.

### 1. The tree and its exact cost

Fix $k=10$, $d=210$, window $[10^9,10^9+2^{22})$, and sieve primes $2,3,5,7$ and $11\le p\le y$. Let $G_p$ be the allowed residues of the start modulo $p$. Order the primes $p_1,\ldots,p_n$ and let $S_i$ be the window cells surviving $p_1,\ldots,p_i$.

Level $i$ generates every allowed child of every kept class: $\text{generated}_i=\text{kept}_{i-1}\,|G_{p_i}|$. While the modulus $Q_i=p_1\cdots p_i$ is at most the window length, all admissible classes are kept. Beyond it, each class holds at most one window cell, so kept classes are exactly $S_i$. Switching to direct cells at depth $i$ costs

$$W(i)=\sum_{j\le i}\text{generated}_j\;+\;S_i\;+\;\sum_{j\ge i}S_j,$$

the last sum being the early-exit filter checks. These counts agree with an explicitly executed tree in the tests. The wheel is the natural order with the largest $Q_i$ not exceeding the window.

**Proposition.** If $Q_i$ exceeds the window, then $W(i+1)-W(i)=S_i\,(|G_{p_{i+1}}|-2)+S_{i+1}$.

**Proof.** The new level generates $\text{kept}_i\,|G_{p_{i+1}}|=S_i|G_{p_{i+1}}|$ children, the representatives change from $S_i$ to $S_{i+1}$, and the filter loses its first term $S_i$. $\square$

The difference is positive whenever a prime has two or more allowed residues. For AP-10 that is every prime from 13 on; for AP-28 every prime from 31 on. A smarter tree that computes only the child containing a class's single window cell spends exactly $S_i$ there, which is the wheel's filter check. Below the window modulus, the tree enumerates the same classes the wheel does.

### 2. Measurements

Best work over all switch depths, relative to the wheel:

| $y$ | Survivors | Wheel work | Ascending | By survival | Big primes first | Descending | Random |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 23 | 2203 | 21,745 | 0.84 | 0.77 | 0.88 | 2.05 | 1.28 |
| 47 | 332 | 28,030 | 0.87 | 0.80 | 1.54 | 215 | 32.5 |
| 97 | 56 | 29,551 | 0.88 | 0.81 | 1.62 | 695 | 89.7 |
| 199 | 18 | 30,174 | 0.88 | 0.82 | 1.69 | 1,766 | 238 |
| 541 | 1 | 30,556 | 0.88 | 0.82 | 1.73 | 4,465 | 234 |

The proposition's identity holds at every level beyond the window for all orders and bounds. The best ascending tree goes exactly one prime past the window modulus, where all classes are still kept and the overshoot is cheap. The by-survival order sorts primes by $|G_p|/p$, which interleaves 2 between 19 and 23. Wheel work per survivor grows from 9.9 at $y=23$ to 30,556 at $y=541$: the factor $\delta_{\rm wheel}/\delta(y)$ of [G13](G13-calibrated-distance.md), which no tree order changes.

### 3. Conclusion

Garner tree search re-expresses wheel enumeration. Its best case saves a constant 12% to 23% and never a factor that grows with the sieve. Idea 25 is closed. One practical constant survives for any sieve-based AP search: order the filter primes by survival fraction $|G_p|/p$ rather than by size. For AP-28 that order starts 29, 31, 37, 41, 43, 47, 53, then 2.

### Reproduction

`python3 -m research.garner_tree` (a few seconds) writes [garner-tree.json](../../results/garner-tree.json). `tests/test_garner_tree.py` checks the level accounting against an explicit tree for every order, the proposition's identity, and the saved ratios.
