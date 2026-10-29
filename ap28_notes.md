# AP-28: mathematical direction and search limits

The new paper is [A Projective Lattice Approach to Prime Arithmetic Progressions](paper_projective_ap28.md). It treats `(a,m)` as variables in `a+j*23#*m`, proves exact local direction counts and a CRT lattice basis, and states the remaining obstacle: a practical reduction in work after sieving and term-size costs.

The one-difference reference implementation is `search_prime_ap.py`. It sieves start intervals and checks their terms directly. The start interval can be shorter than a progression's span. It stores no prime set spanning all 28 terms.

```bash
python3 search_prime_ap.py --k 28 --start 1000000000000000 --count 10000000
```

This is a correctness smoke test with negligible discovery expectation. A run with no match is not evidence against existence or a serious feasibility experiment.

For all terms above 28, `d` must be divisible by `23# = 223092870`. The smallest span is `27*d = 6023507490`. The old `rbls_gpu_pipeline_ap28.py` instead collects every prime in a whole term window; its billion-number setting cannot contain one AP-28 and now fails before GPU initialization. Increasing that window alone does not fix its memory cost or establish a speed advantage.

A partial prime-tuple model near `10^15` at the minimum difference gives a local intensity near `7.9e-26` per raw start. Its reciprocal is about `1.3e25`; it cannot be extrapolated as a constant waiting distance over an interval that large. Adding 29 and 31 to the difference raises raw intensity there, but also raises the fraction of candidates surviving a sieve containing those primes. The new paper derives this cancellation.

There is currently no demonstrated practical AP-28 discovery budget in this repository. The projective-lattice prototype checks mathematical certificates; a complete multi-cell enumeration and a proven or measured advantage remain research work.
