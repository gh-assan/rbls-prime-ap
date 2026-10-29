# Finite assessment of a newer transference route

Date: 29 October 2026. **Outcome: the direct route below cannot supply the proposed finite certificate. No AP-28 or positive arithmetic lower bound is supplied.**

The primary source is Teräväinen and Wang, [On the Green–Tao theorem for sparse sets](https://arxiv.org/html/2603.09281v1), 10 March 2026. Its dense-model argument uses a small interval `U^(2k)` error for a majorant and a bounded model, followed by a progression-density theorem. The introduction explicitly retains a scale threshold in its Varnavides step. This assessment tests those inputs at a stated height; it does not challenge the asymptotic theorem or cover every relative method.

## 1. Check the published parameters before substituting ours

Write `H=2^64-1` for the current implementation height. This is a working range, not a restriction on the original construction goal.

Theorem 6.2 specifies `W=product_{p <= (log H)^c0} p`, with `0<c0<1/100`. Since `1<log H<64<2^100`, its cutoff is less than 2: **the prescribed `W` here is 1**. The theorem does not permit substituting `W=D=23#=223092870` into that displayed formula at this height. Using `W=1` does not exclude progressions with difference divisible by `D`; this is a parameter check, not a nonexistence argument.

We examine both the published `W=1` case and a hypothetical adaptation to the desired `W=D`. For either `W`, use the common interval

`1 <= n <= N_W = floor(H/W)-1`, with prime values `W*n+b`, `1<=b<=W`, `(b,W)=1`.

Every such value lies below `H`. These are precisely the two common intervals assessed here, not a partition or complete treatment of the full two-variable cone. Put `k=28` and `s=2k=56`, as in the stated majorant hypothesis.

## 2. The interval norm also controls individual peaks at this scale

Use the source's interval normalization: zero-extend the function and divide its unnormalized cube norm by that of `1_[N]`. The exact number of integer `s`-cubes in `[N]` is

`C_s(N) = sum_{j=0}^{min(s,N-1)} 2^j binom(s,j) binom(N,j+1)`.

To prove the formula, choose the `j` nonzero increments and their signs. If their absolute values sum to `r`, there are `binom(r-1,j-1)` positive compositions and `N-r` possible base points. Summing gives `binom(N,j+1)`. The zero-increment case contributes `N`.

For any complex `h` and `s>=2`,

`||h||_U^s[N] >= C_s(N)^(-1/2^s) ||h||_infinity`.

Indeed, in the recursion for the unnormalized cube sum, each fixed-last-increment contribution is a nonnegative `(s-1)`-order norm power. Retain the zero increment. The remaining function is `|h|^2`, whose cube products are nonnegative; retaining all remaining zero increments gives `sum_x |h(x)|^(2^s)`. A point mass gives equality in the displayed norm-to-supremum comparison. It is not necessary to estimate a large prime correlation to prove this inequality.

If `B` is the bit length of `C_s(N)`, the exact factor is strictly greater than `1-B/2^s`, using `exp(-t)>=1-t` and `log(2)<1`. The calculations give:

| Interval | `N_W` | `B` |
|---|---:|---:|
| Published `W=1` | 18,446,744,073,709,551,614 | 3450 |
| Desired `W=D` | 82,686,390,082 | 1869 |

Both lower factors exceed `100/101`. Consequently, on either interval,

`||nu-1||_U^56[N_W] < 1  =>  nu(n) < 201/100 = 2.01`.

This is a finite necessary condition for the indicated hypothesis, rather than an estimate for a particular Selberg majorant.

It already obstructs the full unscaled prime weight `f_b(n)=(phi(W)/W)*theta_*(W*n+b)`:

- For `W=1`, the full weight at `n=10`, `b=1` is `log(11)>9/4>2.01`.
- For `W=D`, any nonzero prime weight on the common interval exceeds `16*phi(D)/D=1769472/676039>2.01`, because `D*n+b>D>exp(16)`. This assertion is conditional on a nonzero prime weight; an empty prime class has no such peak.

Thus a majorant of these peaks cannot satisfy the norm bound below one. An asymptotic estimate with an unspecified multiplier may exceed one at this height and does not contradict this fact. Its multiplier cannot simply be set to one. Scaling or thinning the prime weight changes the mean and needs another check.

## 3. Scaling the weight does not repair a density-only final step

Consider any nonnegative prime-supported `f<=nu` obeying the preceding norm hypothesis. Suppose a model `g:[N_W]->[0,2]` has the explicit absolute mean error `|mean(g)-mean(f)|<=1/100`. This is an assumption being audited, not an estimate established for the actual prime weight. Let `h=g/2`.

The [Brun–Titchmarsh inequality, Lemma 11.1 of Lenstra and Pomerance](https://math.dartmouth.edu/~carlp/aks111216.pdf) gives

`pi(H;W,b) <= 2H / (phi(W)*log(H/W))`.

Together with `nu<2.01`, it bounds the mean of `h` from above by

`( (201/100)*2H/(L_W*phi(W)*N_W) + 1/100 ) / 2`,

where `L_1=44<log H` and `L_D=25<log(H/D)`. The bounds are below `0.051` for `W=1` and below `0.5` for `W=D`.

Now define `A_N` to contain the positive integers at most `N` whose base-29 digits all lie in `{0,...,26}`. This set has no nonconstant 28-term arithmetic progression. If the difference is nonzero modulo 29, the 28 residues are distinct and cannot fit into 27 allowed final digits. Otherwise divide the progression, after subtracting its common final digit, by 29. Iterating through the finite number of digits forces a zero difference. Leading zero digits are allowed throughout the argument.

An exact digit-prefix count gives:

| Interval | `|A_N|` | Density, for readability |
|---|---:|---:|
| `W=1` | 7,526,968,007,116,178,141 | 0.408037... |
| `W=D` | 50,756,571,120 | 0.613844... |

These exact densities exceed the respective upper bounds on `mean(h)`. For every positive `delta` at most either mean upper bound, the function `delta*N/|A_N| * 1_A_N` lies in `[0,1]`, has mean `delta`, and has **zero nonconstant AP-28 count**. Therefore a universal positive progression bound that uses only that mean and boundedness cannot hold at these scales. This is a finite counterexample, not merely a complaint that published constants are unavailable.

The actual model `g` might possess additional useful structure. The counterexample does not assert that it is AP-free. A different counting argument retaining arithmetic information could succeed; the generic density-only step assessed here cannot certify it.

## 4. Consequence for the research direction

The newer result does not close the missing finite arithmetic step by direct substitution, with either of the two stated `W` choices. There are two separately checked obstacles: the majorant condition is incompatible with the unscaled prime peaks, and a scaled/thinned version subject to the stated mean control does not reach a density for which a universal positive AP-28 count is possible on these intervals.

This assessment rules out one proposed finite proof architecture. It proves neither absence of an AP-28 nor impossibility of a mathematical construction. It does not rule out larger heights or a method using the model's specific structure rather than a universal density bound. The goal is still the original explicit, independently verified progression, obtained without brute-force discovery. Neither a numerical count lower bound nor a witness-recovery rule has been obtained here.

The practical decision is to stop treating a generic uniformity estimate plus a density theorem as the current finite construction plan. Retain the full `D`-family target, but require a new arithmetic estimate that controls its actual joint prime weight, or a direct structural candidate with a primality proof. An additional conditional reformulation does not satisfy that gate.

Run `python3 -m research.transference_audit` for [the exact certificate](../results/transference-audit-checks.json). Rational bounds for `e` prove the logarithmic comparisons; no floating-point logarithm is used. Independent tests check the cube formula from its defining sum, including complex phases and sharp point masses, digit counts at boundaries, and the finite-field step of the AP-free proof. This code performs proof checks and digit-prefix counting; it does not enumerate prime progression candidates.
