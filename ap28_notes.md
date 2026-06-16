# AP-28 Search — Algorithm Changes

## Why the new approach?

The AP-7 brute-force method (testing every number) would need ~10^25 candidates for AP-28.
That's not feasible. Instead:

## New Algorithm

1. **LLL + Riemann zeros** → target region ~10^15 (same as before)
2. **GPU finds primes** in a window around the target
3. **CPU scans prime positions** for AP-28 patterns using hash-set lookups

For AP-28, the admissible primorial step is `23# = 223,092,870`, because
23 is the largest prime less than or equal to 28. A step of `19# = 9,699,690`
would be impossible for AP-28: the first 23 terms would cover every residue
class modulo 23, forcing one term to be divisible by 23.

With `d = 223,092,870`, one AP-28 spans more than 6.0 billion integers. The
current script keeps the original 1 billion-number prototype setting but now
exits early with a warning instead of reporting a meaningless AP-28 miss. A
real AP-28 run needs a larger segmented scan that does not keep the entire
prime list in memory at once.

This is much faster because we only test primality once per number (not 28 times),
and the post-scan only looks at actual primes (~29 million out of 1 billion numbers).

## Files

| File | Purpose |
|------|---------|
| `rbls_gpu_pipeline_ap28.py` | New AP-28 pipeline script |
| `ap28_search_*.txt` | Run log (minimal, only results & progress) |
| `ap28_search_*_ap.txt` | Any AP progressions found (if any) |

## How to run

```powershell
cmd.exe /c "`"...vcvars64.bat`" && .venv\Scripts\python.exe rbls_gpu_pipeline_ap28.py 2>&1"
```

The script writes all results to timestamped files automatically.
No per-number logging — just chunk progress and final results.
