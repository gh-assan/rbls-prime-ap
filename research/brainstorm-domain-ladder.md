# Brainstorm: climbing a ladder of domains for AP-28

Date: 29 October 2026. **Status: unproved candidate methods only.** Nothing here is a result. Each idea moves the problem into a new domain, proposes a way to find `(a,d)` there, and names the first cheap experiment. Ideas are deliberately mixed across levels at the end.

The common yardstick for every experiment: on a small analog with known ground truth (for example all AP-10 or AP-12 below `10^12`), measure **primality tests and total operations per progression found**, against Wróblewski's wheel-and-sieve baseline. A method that wins there by a growing factor is worth scaling.

Notation: `a + j*D*m`, `D = 23#`, `0 <= j < 28`, cells `(a,m)` in the box below `2^64`.

---

## Level 0: integers

The object: a point `(a,m)` in a 2D box such that 28 linear forms are prime.

## Level 1: residues (CRT)

Modulo each prime `p >= 29`, the bad cells are **28 lines through the origin** of `F_p^2`. Equivalently the ratio `a/m mod p` must avoid 28 of the `p+1` projective directions.

1. **Run transform.** Choose `m` so that `D*m ≡ c (mod p)` with a small `c` for many `p`. Then the progression behaves modulo `p` like `a, a+c, ..., a+27c`; for `c=1` it is 28 *consecutive integers*. Avoidance becomes a Jacobsthal-type question about runs of integers free of the primes in `S`. *Test:* does the run picture let tables of Jacobsthal-optimal runs choose `a` better than random admissible classes?
2. **Collapsed lines.** A one-parameter family `(a(t), m(t))` whose reduction passes through the origin mod `p` meets all 28 bad lines at one point, so only one `t` class is lost instead of 28. Use quadratic or higher parameterizations to get this for many `p` at once. *Test:* compute the family's singular series and point count per unit height.
3. **Direction scheduling with a budget.** Treat the choice of a good direction per prime as a code; pick directions whose CRT lift is *short* (see Level 3).

## Level 2: additive Fourier on Z/M

Fourier transform of one bad line is a dual line. For fixed `m`, the good set modulo `p` has transform `p-28` at `0` and **minus a Dirichlet kernel** `D_28(eta*D*m/p)` elsewhere. Over all primes the transform is a **product of Dirichlet kernels**, an Euler-product-shaped object in the frequency variable.

4. **Fourier bisection sieve.** Survivor counts in a sub-box equal a sum over frequencies of (product of kernels) times (box kernel). Most kernel products are tiny; only *resonant* frequencies matter. Evaluate counts of sub-boxes from the resonant frequencies and bisect (contract of [G4](../papers/gaps/G4-witness-localization.md)) down to survivors, never enumerating dead cells. *Test:* how many frequencies are needed for counts accurate enough to bisect at AP-10 scale?
5. **Sparse Fourier recovery.** Sieve survivors in the box are a *k-sparse* 2D signal (about `10^5` per expected AP-28 after primes to `10^7`). Sparse FFT algorithms (Hassanieh–Indyk–Katabi–Price 2012) recover a k-sparse signal from about `k log n` transform samples. The transform of the periodic part is free (product formula); the question is sampling the *box-restricted* transform. *Test:* can hashing filters be built from the product structure so that each bucket sample costs polylog?
6. **Reciprocity for incomplete sums.** Dedekind sums and quadratic Gauss sums over intervals are evaluated in `O(log)` steps by reciprocity laws. Look for a reciprocity law for exponential sums over sieve survivors in an interval. *Test:* try the 1D case of one forbidden residue per prime.
7. **Meissel–Lehmer for patterns.** Primes up to `x` are counted in about `x^{2/3}` time without listing them, using the recursion `Phi(x,a) = Phi(x,a-1) - Phi(x/p_a,a-1)`. No sublinear counter is known even for **twin primes**, because divisibility of `n+2` does not rescale. Find a recursion that does rescale for linear patterns, for example by working in the 2D cone where `(a,m) -> (a/p, m/p)` maps lines through the origin to themselves. With bisection this gives a non-enumerating AP-28 locator. *Test:* attempt an exact recursion for 2-term patterns `a, a+Dm` in the cone.

## Level 3: dual lattices and Diophantine approximation

Resonant frequencies are those where `xi*c_p/p` is near an integer for many `p` at once: a **simultaneous approximation** problem, the native domain of LLL. This is the principled form of the original RBLS idea: "resonance" lives in the dual of the CRT problem, not in zeta-zero phases near the start.

8. **Resonance LLL.** Build the lattice whose short vectors are frequencies resonant across many primes; feed them to idea 4. *Test:* compare the mass captured by LLL-found frequencies against all frequencies for a small modulus.
9. **Farey lifting with Euler continuants.** A CRT class `r mod M` has a point in the box exactly when `r/M` is close to a Farey fraction `u/m` with `m` small. Euler's continuant algorithm (continued fractions) finds it in `O(log M)`. Sample classes from the product set already biased toward Farey neighborhoods. Fourier dual of Farey neighborhoods is Ramanujan/Kloosterman sums. *Test:* is there a cheap way to draw elements of a CRT product set conditioned on a small first partial quotient?
10. **CRT list decoding, inverted.** Boneh (2000) finds *smooth* integers in short intervals by CRT list decoding with Coppersmith lattices: divisibility is an *agreement* constraint. We need roughness, an *avoidance* constraint. **Euler's theorem converts avoidance into agreement:** `x` is coprime to `P` exactly when `P` divides `x^phi(P) - 1`. Look for low-degree polynomials vanishing on most good residues so that Coppersmith bounds survive. *Test:* minimal degree of a polynomial mod `p` vanishing on at least half the good set.

## Level 4: multiplicative characters and Euler products

11. **Character-sum steering.** The [G9](../papers/gaps/G9-character-minorant.md) minorant uses 174 characters. Instead of bounding them, *steer*: pick sub-boxes where the twisted sums are most positive, computed with fast character-sum algorithms, and bisect. *Test:* correlation between twisted sums on sub-boxes and actual AP-10 counts.
12. **Hybrid Euler–Hadamard product.** Gonek–Hughes–Keating write `zeta = P_X * Z_X`: a short Euler product times a zero product. Move the cutoff `X` to put cheap information on the prime side (sieve) and fine-scale density fluctuations on the zero side. *Test:* predictive power of the zero side for prime counts in windows of size `10^4..10^6` near `10^12`.
13. **Euler's idoneal numbers.** Euler certified large primes by unique representation as `x^2 + n*y^2` with idoneal `n` (largest known 1848). Use idoneal forms as a batch primality certificate for 28 terms, and look for AP families compatible with a common form. *Test:* which progressions mod `4n` keep all terms representable by one idoneal form?

## Level 5: Mellin transform and zeros

14. **Stationary-phase targeting.** Expand each `Lambda(a+jd)` by the explicit formula. A 28-tuple of zeros contributes an oscillatory integral over the box with phase `sum_j gamma_j log(a+jd)`. Its **stationary points** solve `sum gamma_j/(a+jd) = 0` and `sum j*gamma_j/(a+jd) = 0`: locations where the zero contributions align. Choose tuples whose aligned sign pushes prime density up. *Test:* at AP-6 scale near `10^9`, do stationary points of low zeros predict excess progressions?
15. **Beta and Selberg integrals.** The integral of `prod_j (a+jd)^{rho_j - 1}` over a cone is a generalized Beta/Selberg integral. Euler's Beta function `B(x,y) = Gamma(x)Gamma(y)/Gamma(x+y)` gives closed forms, so an *explicit formula for AP-28 counts in a sub-box* may be a sum of Gamma ratios over zero tuples. Feed it to bisection. *Test:* derive the closed form for 3-term progressions first.

## Level 6: algebra and number fields

16. **Heegner progressions (Euler's `x^2+x+41` for APs).** Take `a(t) = t^2 + e`, `d = c` with `23# | c`. Then a prime `p | c` never divides any term for any `t` when `-e` is a non-residue mod `p`; for `p` not dividing `c`, all 28 values `-(e+jc)` must be non-residues. Use pseudosquare-type `e` to avoid many primes at once. *Test:* measure hit rate per primality test against the plain wheel. Expectation: equal to the wheel unless the quadratic structure is exploited further, so pair it with idea 13 or 25.
17. **Maynard weights as a sampler.** Maynard–Tao sieve weights concentrate on `(a,d)` where many of the 28 forms are prime. Draw candidates from the weight distribution (constructible from its divisor-sum form) instead of uniformly. *Test:* primes per candidate among the 28 forms, weighted versus wheel.
18. **Binary form `F(a,d) = prod (a+jd)`.** Use the geometry of numbers of the degree-28 form (its Hessian and covariants) to find regions where `F` has unusually few small prime factors. *Test:* compare `omega(F)` distributions across reduced-form orbits.

## Level 7: function fields

19. **q-analog bootstrap.** Over `F_q[t]` with large `q`, progressions of irreducibles are plentiful and nearly explicit (Chebotarev, large-`q` equidistribution). Study which structural features make them explicit there and look for integer shadows: polynomial families `f(t) + j*c` whose integer values inherit them. *Test:* write down an explicit AP-28 of irreducibles over some `F_q[t]` and list the properties it uses.

## Level 8: adelic and ergodic

20. **Solenoid rotation.** The progression is an orbit of translation by `d` on the solenoid (profinite times real). Choose `d` so the rotation has interval structure at many primes (idea 1), then pick `a` by a Kronecker/three-gap argument so the 28-step orbit avoids every zero neighborhood. *Test:* simulate avoidance rates for rotations with structured `d`.
21. **Maier matrices.** Maier's matrix method proves that prime counts in short intervals near multiples of primorials oscillate by constant factors. A 28-term bias of a few percent per term compounds. *Test:* per-candidate primality rate (after the wheel) for terms placed at Maier-favorable offsets. Expectation: the bias is per interval, not per coprime candidate; measure before believing.

## Level 9: combinatorics

22. **Algorithmic density increment.** Run the Roth/Szemerédi density-increment proof as an algorithm on W-tricked primes; each step chooses a sub-progression of higher relative density, and the AP appears in the final structure. *Test:* run it on AP-8 below `10^10` and record which structures it chooses beyond the wheel.
23. **Algorithmic containers.** The greedy max-degree container algorithm on the 28-AP hypergraph of sieve survivors. *Test:* on AP-8, does its trace localize progressions faster than enumeration?
24. **Covering, reversed.** Ford–Green–Konyagin–Maynard–Tao build long prime gaps by choosing residues that *cover* an interval. Reverse it: choose residues for a middle range of primes to cover everything near the progression *except* its 28 terms, pinning roughness where needed. *Test:* box size of the resulting CRT class at AP-10 scale.

## Level 10: computation

25. **Garner tree search.** In mixed radix (Garner's algorithm) the condition at the `i`-th prime involves only the first `i` digits. Order primes so the box constraint bites early and run branch-and-bound with interval pruning, like Schnorr–Euchner lattice enumeration but with avoidance constraints. *Test:* nodes visited per survivor versus wheel enumeration.
26. **Message passing.** Belief propagation or survey propagation on the factor graph of CRT digits and divisibility constraints. *Test:* does it find survivors of a 12-prime sieve in a box faster than enumeration?
27. **Amplitude amplification.** Grover search over sieve survivors gives a square-root speedup: about `1.6*10^8` oracle calls per expected AP-28 after primes to 541. Needs fault-tolerant hardware; worth a resource estimate only.

---

## Random combinations

- **C1 Resonance bisection** = 4 + 8 + G4. Dirichlet-kernel products give sub-box counts; LLL finds the resonant frequencies; bisection walks to an AP. The original RBLS idea, moved to the domain where resonance is real. **Tested in [G14](../papers/gaps/G14-resonance-bisection.md): resonance is real and LLL finds it, but the captured share falls as sieve primes are added and bisection costs 380x to 93,000x the wheel. Rejected as a discovery method; LLL resonance finder kept as a tool.**
- **C2 Run-transform counting** = 1 + 7. After `d ≡ 1 (mod p)` the pattern is 28 consecutive integers; look for a Meissel–Lehmer recursion for consecutive runs, which might rescale better than general patterns.
- **C3 Euler engine** = 10 + 9 + 13. Euler's theorem converts avoidance to divisibility, Euler continuants lift CRT classes into the box, and idoneal forms certify the result.
- **C4 Explicit formula for sub-box counts** = 14 + 15 + 12 + G4. Stationary phase picks zero tuples, Beta integrals give closed forms, the hybrid product controls the cutoff, bisection localizes.
- **C5 Sparse tree recovery** = 5 + 25. The Garner tree supplies hashed samples of the box-restricted transform; sparse recovery reads off survivor positions.
- **C6 Heegner–Maier family** = 16 + 21 + Proth-type certificates. Quadratic families placed at Maier offsets, certified cheaply.
- **C7 Weighted tree** = 17 + 25. Maynard weights guide which branches of the Garner tree to expand first.

## First experiments, in order

1. ~~**C1 Resonance bisection**~~ at AP-10 scale: done in [G14](../papers/gaps/G14-resonance-bisection.md), rejected.
2. **Idea 7 / C2** on 2-term patterns in the cone: any exact rescaling recursion would be new mathematics with large payoff.
3. **Idea 25 Garner tree** with box pruning: cheap to implement, gives a clean nodes-per-survivor number.
4. **Idea 17 Maynard sampler** and **idea 16 Heegner family**: cheap per-test hit-rate measurements.

Each experiment reports tests and operations per progression found against the wheel baseline, and is committed as its own round.
