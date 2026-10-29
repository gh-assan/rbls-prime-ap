# One fixed AP-28 candidate: derivation and rejection

Date: 29 October 2026. **Result: the derived candidate is composite. No AP-28 is obtained.**

Use the AP-27 found by Kai Presler on 2 August 2026, published in [PrimeGrid message 189807](https://www.primegrid.com/forum_thread.php?id=7012&nowrap=true):

`p_j = a+j*d`, `0<=j<=26`,

`a = 973044677408627339`, `d = 174505864*23# = 38931014031589680`.

All 27 source terms were independently rechecked using this repository's deterministic uint64 verifier and SymPy's separate `isprime` implementation. This is a published AP-27, not a new discovery here. The largest term is `1985251042229959019`, within both verifiers' deterministic 64-bit range.

## Derive the only possible direct extension modulo 29

Since `d` is invertible modulo 29, the zero-residue index is

`-a/d = 27 (mod 29)`.

Thus the right extension `a+27*d` is composite, while the left extension at index `-1` passes the 29 test. There is a unique direct extension not rejected by this congruence. It gives the fixed AP-28 candidate

`934113663377037659 + j*38931014031589680`, `0<=j<=27`.

Its last 27 terms are the published primes. Its first term is composite:

`934113663377037659 = 2971 * 314410522846529`.

For completeness, the rejected right endpoint has the exact factorization into two proper integer factors

`2024182056261548699 = 29 * 69799381250398231`.

These integer products settle both direct extensions without relying on a probabilistic compositeness test. The congruence selects the sole remaining direct-extension candidate for verification. No range of starts, differences, or CRT assignments was searched.

## High overlap does not permit a small repair

**Integer progression overlap lemma.** If a 27-term progression of integers with positive difference `d` and a 28-term progression with positive difference `e` have at least 15 common terms, then `d=e`.

To prove it, let `L=lcm(d,e)`. Every difference between two common terms is divisible by `L`, so 15 distinct common terms span at least `14*L`. Their span is at most `26*d` and at most `27*e`. Consequently the positive integers `L/d` and `L/e` are both less than 2. Both equal one, giving `d=e`. The threshold is sharp for integer progressions: the sets `{0,2,...,52}` and `{0,1,...,27}` share 14 terms and have unequal differences.

Any 28-term progression of difference `d` meeting the fixed source progression has a start `a+t*d` for some integer `t`. If `t<0`, its intersection with the source ensures that its interval of indices contains `-1`. If `t>=0`, intersection requires `t<=26`, and its interval contains `27`. Thus every such 28-term progression contains at least one of the two composite neighbors proved above.

It follows that **any prime AP-28, with any positive integer difference, can share at most 14 terms with this fixed AP-27**. Retaining 15 or more source primes while changing a few terms cannot solve the problem. This does not rule out constructions sharing fewer terms, other seeds, or an AP-28 elsewhere.

This check rejects one concrete candidate and its possible high-overlap repairs. It supplies neither a positive finite prime-correlation bound nor a replacement candidate. It is recorded as a failed construction check, not as closure of G2, G3b/G5, or the original witness goal.

Run `python3 -m research.check_published_ap27` to reproduce [the exact certificate](../results/published-ap27-extension-check.json). Tests verify the 27 source primes with an independent implementation, both proper-divisor products, the congruence selection, and the overlap lemma on small integer examples including its sharp threshold.
