# Meissel–Lehmer for Prime Patterns: the Exact Recursion Exists but Does Not Collapse

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Status:** Experiment C2 / idea 7 of the [domain-ladder brainstorm](../../research/brainstorm-domain-ladder.md). Negative as a discovery method, with a precise reason. No AP-28 is supplied.

### Abstract

Primes up to $x$ can be counted without listing them because Legendre's recursion collapses: removing a prime factor turns the problem into the same problem at a smaller scale. A sublinear counter for prime *patterns* would let the bisection contract of [G4](G4-witness-localization.md) locate an AP-28 without search. We give the exact analogue of Legendre's recursion for any pattern, implement it with the strongest memoization that local data allows, and verify it against direct sieving on 39 sizes. For a single form the number of distinct subproblem states equals the number of sieve primes. For twins, 3-term and 5-term progressions it grows faster than $x$: exponents 1.16, 1.21 and 1.30 against 0.82 for primes. We prove why: a substitution fixes the bad residue set of a single form but records the substituted residue for every pattern of two or more forms. No sublinear counter for any pattern of two or more forms is known, even for twin primes; this experiment finds no new foothold.

### 1. The exact recursion

Let $\Phi(x,S)$ count $t\in[0,x)$ whose residue modulo each sieve prime $q$ avoids a bad set $S_q$. The pattern $t+o_1,\ldots,t+o_k$ starts with $S_q=\{-o_i \bmod q\}$. Remove the largest sieve prime $p$. Every $t$ with $t\bmod p\in S_p$ is $t=ps+r$ for exactly one $r\in S_p$, and the conditions at the remaining primes become conditions on $s$:

$$\Phi(x,S)=\Phi(x,S\setminus p)-\sum_{r\in S_p}\Phi\!\left(\left\lceil\tfrac{x-r}{p}\right\rceil,\,S^{(p,r)}\right),\qquad S^{(p,r)}_q=\{(b-r)p^{-1}\bmod q:b\in S_q\}.$$

If $S_p$ is all of $\mathbb Z/p$, then $\Phi=0$. With no primes left, $\Phi(x,\varnothing)=x$. The identity is exact for any finite pattern. The implementation interns states, memoizes on (scale, state), and counts leaves of size at most 16 directly. All 39 measured counts agree with an independent direct sieve.

### 2. Why a single form collapses and a pattern does not

**Single form.** For $t$ alone, $S_q=\{0\}$ and the only root is $r=0$, so $S^{(p,0)}_q=\{0\}$ again. The state forgets the substitution, and every subproblem is determined by its scale and the number of primes left. This is multiplicativity: for $q\nmid p$, $q\mid ps$ exactly when $q\mid s$. It is what lets Meissel–Lehmer reuse one table of $\Phi(y,b)$ for all $y\le x^{2/3}$ and reach $O(x^{2/3})$ work.

**Two or more forms.** After substitutions with product $d$ and combined residue $R$, the bad set at a remaining prime $q$ is $\{-(R+o_i)d^{-1}\bmod q\}$. For twins its two elements differ by $\pm2d^{-1}$, which fixes $d\bmod q$ up to sign, and then the elements fix $R\bmod q$. Hence:

**Proposition.** For the twin pattern, a state determines $(d \bmod q,\,R\bmod q)$ at every remaining prime $q>2$, up to the single reflection $(d,R)\mapsto(-d,-R-2)$. Once the product of the remaining primes exceeds the range of $(d,R)$, distinct substitutions give distinct states up to that reflection.

So memoization can merge at most pairs of subproblems. The same argument applies to every pattern with two distinct offsets, since any two offsets $o\ne o'$ produce the difference $(o-o')d^{-1}$. The recursion then needs about one subproblem per pair $(d,R)$ with $d\le x$, and their number grows faster than the $x$ cells a sieve visits.

### 3. Measurements

Distinct memoized subproblems and distinct states, with sieve primes up to $\sqrt{x}$:

| Pattern | $x$ | Subproblems | States |
|---|---:|---:|---:|
| primes $t$ | 65,536 | 2,448 | 55 |
| twins $t,t+2$ | 65,536 | 10,930 | 17,530 |
| 3-AP, $d=6$ | 65,536 | 20,142 | 42,335 |
| 5-AP, $d=30$ | 65,536 | 43,250 | 139,644 |
| primes $t$ | 16,777,216 | 215,735 | 565 |
| twins | 262,144 | 56,912 | 114,888 |

Growth exponents of the subproblem count, fitted on the largest four sizes: primes 0.82, twins 1.16, 3-AP 1.21, 5-AP 1.30. For primes the state count is exactly the number of sieve primes plus one at every size, as Section 2 predicts. The prime exponent is that of plain memoized Legendre; full Meissel–Lehmer improves it to $2/3$ using the same collapse. For patterns the exponent exceeds 1 and rises with the number of forms, so the exact recursion scales worse than direct sieving, and each subproblem also costs a state transform over all remaining primes. The trend worsens toward AP-28.

### 4. What this rules out, and what would be needed

The analytic route to sublinear prime counting, Lagarias–Odlyzko, rests on the Euler product of $\zeta$, the same multiplicativity in another form. A pattern indicator such as $1_{\mathbb P}(n)1_{\mathbb P}(n+2)$ has no Euler product. Both known sublinear methods therefore stop at a single form. This experiment confirms that the combinatorial one does not extend through memoization by local data, the most it could use.

A sublinear pattern counter would need a new identity expressing a pattern count through quantities that *do* collapse, such as single-form counts in progressions, with exactly controlled remainders. No such identity is known for twin primes. Finding one would be a major result independent of AP-28, which is why this idea scored high in the brainstorm. Our recursion supplies none, so idea 7 and combination C2 are closed as tested here. The consecutive-run variant (idea 1 combined with this recursion) falls under the same proposition: after a substitution the run $t,\ldots,t+27$ becomes the pattern $\{ps+r+i\}$, which records $r$.

### Reproduction

`python3 -m research.pattern_counting` (about 20 seconds) writes [pattern-counting.json](../../results/pattern-counting.json). `tests/test_pattern_counting.py` checks exactness for every pattern, the single-form state collapse, the twin substitution remembering its residue, and the growth exponents.
