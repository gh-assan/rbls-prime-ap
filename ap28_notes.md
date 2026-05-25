# AP-28 Search — Algorithm Changes

## Why the new approach?

The AP-7 brute-force method (testing every number) would need ~10^25 candidates for AP-28.
That's not feasible. Instead:

## New Algorithm

1. **LLL + Riemann zeros** → target region ~10^15 (same as before)
2. **GPU finds ALL primes** in a 1 billion-wide window around the target
3. **CPU scans prime positions** for AP-28 patterns using hash-set lookups

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
