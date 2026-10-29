# No Published AP-26 or AP-27 Record Extends to AP-28

**Author:** Ghassan Al Hamoud  
**Date:** 29 October 2026  
**Status:** Closed at the stated finite scope. Every published AP-26/AP-27 record checked here is maximal toward AP-28. No AP-28 is supplied.

### Abstract

The only mathematical objects currently known to lie close to an AP-28 are the published record progressions of 26 and 27 primes. We prove that a prime AP-28 sharing at least 15 terms with such a record must have the same difference and contain one of the record's two adjacent neighbors. For eight published records, including all four known AP-27s, both neighbors have an exact proper divisor or are nonpositive. Hence **every prime AP-28 shares at most 14 terms with each of these records**. Modulo 29 exactly one full-containment window survives for each record, and for records produced by Wróblewski's program, as described in the Illinois report, that window is the 28-term window the program already tests. Extending records is therefore structurally closed, not merely unlucky.

### 1. Current public status

The record table maintained at [pzktupel.de](https://www.pzktupel.de/PAP/aprecords.php), last updated 12 October 2026, lists 27 as the longest known length. PrimeGrid's AP28 badge was still unclaimed in its [badge list](http://www.primegrid.com/forum_thread.php?id=7799), and a [May 2025 Illinois report](https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf) describes software adapting Wróblewski's AP-26 sieve to look for the first AP-28. No published source found here gives an AP-28 or a search-free construction of one. All records below were found by sieve searches.

### 2. Overlap forces the same difference

**Lemma 1.** Let an $L$-term integer progression with difference $d>0$, $L\le28$, and a 28-term integer progression with difference $e>0$ share at least 15 terms. Then $d=e$.

**Proof.** Let $\ell=\operatorname{lcm}(d,e)$. Any two common terms differ by a multiple of $\ell$, so 15 distinct common terms span at least $14\ell$. The span is at most $(L-1)d\le27d$ and at most $27e$. Thus $\ell/d$ and $\ell/e$ are positive integers below $27/14<2$, so both equal one. $\square$

**Corollary.** Suppose the record terms $a+jd$, $0\le j<L\le27$, are prime and both neighbors $a-d$ and $a+Ld$ are composite or less than 2. Then every prime AP-28, with any positive difference, shares at most 14 terms with the record.

**Proof.** With at least 15 common terms, Lemma 1 gives the same difference, so the AP-28 is $a+jd$, $s\le j<s+28$, for an integer $s$. Its index interval meets $[0,L-1]$ and is longer. If $s<0$, it contains $-1$; if $s\ge0$, then $s\le L-1$ and $s+27\ge L$, so it contains $L$. Either way it contains a blocked neighbor. $\square$

The bound is sharp for integer progressions: $\{0,2,\ldots,52\}$ and $\{0,1,\ldots,27\}$ share 14 terms.

### 3. Exactly one window survives modulo 29

Every listed difference is divisible by $23\#$ but not by 29. Let $i_0$ be the unique index class with $29\mid a+i_0d$. Since the $L$ record terms are prime and exceed 29, $i_0\notin\{0,\ldots,L-1\}$ modulo 29.

**Lemma 2.** For $L\in\{26,27\}$, exactly one window $s\in[L-28,0]$ avoids $i_0$ modulo 29.

**Proof.** A 28-term window misses exactly one residue class modulo 29, namely $s-1$. The admissible $i_0$ are $L,\ldots,28$, so $i_0+1$ runs over $L+1,\ldots,29$, which are congruent to $L-28,\ldots,0$. Each $s$ in that range matches exactly one $i_0$. $\square$

Wróblewski's program normalizes its core start $n\equiv3D\pmod{29}$ and tests the window $n-2D,\ldots,n+25D$ [IML report, Sections 2-3]. Relative to $n$, the zero class is $26\equiv-3$, which this window avoids. By Lemma 2 it is the unique surviving window containing any progression the program reports. So every AP-26 or AP-27 found by that program has already had its only modular AP-28 extension tested by the program itself.

### 4. Exact certificates

All $L$ terms of each record were verified with the repository's deterministic 64-bit Miller-Rabin verifier and independently with SymPy.

| Record | $L$ | $d/23\#$ | $i_0$ mod 29 | Neighbor $-1$ | Neighbor $L$ |
|---|---:|---:|---:|---|---|
| Gahan 2019 | 27 | 81292139 | 27 | divisor 31 | divisor 29 |
| Greer 2023 | 27 | 170826477 | 28 | divisor 29 | divisor 353 |
| Kwok 2023 | 27 | 155368778 | 27 | divisor 31 | divisor 29 |
| Presler 2026 | 27 | 174505864 | 27 | divisor 2971 | divisor 29 |
| Perichon 2010 | 26 | 23681770 | 27 | divisor 43 | divisor 113 |
| Fry 2012 | 26 | 1666981 | 27 | divisor 6807329 | divisor 31 |
| Jayaputera 2025 | 26 | 397344516 | 26 | divisor 137 | divisor 29 |
| Carquillat 2026 | 26 | 531515022 | 27 | nonpositive | divisor 31 |

Each divisor $p$ is checked as $n=p\cdot(n/p)$ with $1<p<n$. The certificate also records one blocking term for each of the 20 full-containment windows. By the Corollary:

**Theorem.** Every prime AP-28, with any positive difference, shares at most 14 terms with each of these eight published records.

The fixed check of the Presler record in [the earlier note](../../research/fixed-ap27-candidate-check.md) is the special case of one row.

### 5. What this closes

The route "derive an AP-28 from a known near-record" is closed for every record listed: no extension, no high-overlap repair, and no unchecked modular window remains. Section 3 explains why: the program that found these records already tests the only extension compatible with 29.

This is a complete finite result. It supplies no positive AP-28 bound and no replacement candidate. It does not close G2 or G3b/G5.

### Reproduction

`python3 -m research.record_extensions` writes [record-extension-checks.json](../../results/record-extension-checks.json). `tests/test_record_extensions.py` checks every term independently, every blocking factorization, the window enumeration, the uniqueness modulo 29, and the overlap lemma on small integer progressions.

### Sources

1. Record table, last updated 12 October 2026: <https://www.pzktupel.de/PAP/aprecords.php>
2. OEIS [A327760](https://oeis.org/A327760) (Gahan), [A363980](https://oeis.org/A363980) (Greer), [A374949](https://oeis.org/A374949) (Kwok).
3. PrimeGrid announcement of the Presler AP-27: <https://www.primegrid.com/forum_thread.php?id=7012&nowrap=true>
4. Mok, Bradu, Rojas, Desai, Zhen; advisers Fernando and Qu. *Developing Software to Find Arithmetic Progressions of 28 Primes*, Illinois Mathematics Lab, May 2025: <https://ravif.web.illinois.edu/PrimeGrid/IML_AP28_report.pdf>
