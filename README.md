# RBLS (Resonance-Biased Lattice Sieving) — Arithmetic Progression Prime Finder

This project searches for **long arithmetic progressions of primes** (AP-k) using an exploratory hybrid approach:

1. **Analytic Phase:** Uses the imaginary parts of the first three Riemann zeta zeros and SymPy's LLL lattice reduction to compute reproducible target regions near ~10¹⁵.
2. **Discrete Sieve:** Tests candidate numbers in batches using a deterministic Miller-Rabin primality test (64-bit, 12-witness, guaranteed correct for all `n < 2⁶⁴`).
3. **Dynamic Primorial Step Size:** The common difference `d` is computed as the **primorial of all primes less than or equal to `k`**, ensuring admissibility against the required small-prime obstructions.

RBLS is a heuristic target generator, not a proof of elevated prime density. The current AP-7/AP-8 results verify that the implementation finds genuine progressions; controlled baseline searches are still needed before claiming a statistical speedup.

Available implementations:

| Script | k | Platform | Engine |
|--------|---|----------|--------|
| `rbls_gpu_pipeline.py` | 7 | Windows + NVIDIA GPU (Tesla T4, etc.) | CUDA via PyCUDA |
| `rbls_m1_pipeline.py` | 7 | macOS Apple Silicon (M1/M2/M3) | Numba JIT + parallel CPU |
| `rbls_gpu_pipeline_ap8.py` | 8 | Windows + NVIDIA GPU (Tesla T4, etc.) | CUDA via PyCUDA |
| `rbls_m1_pipeline_ap8.py` | 8 | macOS Apple Silicon (M1/M2/M3) | Numba JIT + parallel CPU |
| `rbls_gpu_pipeline_ap9.py` | 9 | Windows + NVIDIA GPU (Tesla T4, etc.) | CUDA via PyCUDA |
| `rbls_m1_pipeline_ap9.py` | 9 | macOS Apple Silicon (M1/M2/M3) | Numba JIT + parallel CPU |
| `rbls_gpu_pipeline_ap28.py` | 28 | Windows + NVIDIA GPU (Tesla T4, etc.) | CUDA via PyCUDA (prime-find then scan) |

---

## Prerequisites

### For GPU Pipelines (Windows)

- Windows 10/11
- Microsoft Visual Studio Build Tools 2022 (or VS 2022) with **VC++ toolset**
- NVIDIA GPU with Compute Capability ≥ 3.0 (e.g., Tesla T4, RTX series)
- NVIDIA CUDA Toolkit (matching your GPU driver)
- Python 3.10+ (64-bit)

### For Apple Silicon Pipeline (macOS)

- macOS with Apple Silicon (M1, M2, M3, etc.)
- Python 3.10+ (arm64)
- LLVM (installed automatically via Numba)

---

## Setup

Create and activate the virtual environment, then install dependencies:

```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate
```

### Install Dependencies

```powershell
pip install numpy pycuda sympy
```

> **Note:** `pycuda` requires a CUDA-capable GPU and the NVIDIA CUDA Toolkit.
>
> For Apple Silicon (`rbls_m1_pipeline.py`), install instead:
> ```bash
> pip install numpy numba sympy
> ```

---

## How to Run

### GPU Pipelines (Windows)

The GPU scripts require the Visual Studio Build Tools environment to be loaded **before** running. Use a single `cmd.exe` invocation:

**AP-7 (k=7, d=210):**
```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe rbls_gpu_pipeline.py 2>&1"
```

**AP-9 (k=9, d=210):**
```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe rbls_gpu_pipeline_ap9.py 2>&1"
```

**AP-28 (k=28, d=223,092,870):** (GPU prime-find then CPU scan)
```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe rbls_gpu_pipeline_ap28.py 2>&1"
```

**Explanation:**
- `vcvars64.bat` — loads the VC++ environment variables (compiler, linker, etc.) needed by PyCUDA to compile the CUDA kernel at runtime.
- `&&` — runs the Python script only after the environment is loaded.
- `2>&1` — merges stderr into stdout so you see any compiler warnings.
- The whole command is wrapped in `cmd.exe /c "..."` so it runs as a single cmd session, preserving environment variables.

> **Note:** Adjust the path to `vcvars64.bat` if your Visual Studio or Build Tools installation is in a different location.

### CPU Pipeline (Apple Silicon / macOS)

```bash
python rbls_m1_pipeline.py
```

Numba will JIT-compile the hot loops on first run (adds ~1–2 seconds initially).

---

## Test Scripts

### `test_prime_kernel.py`
Verifies the CUDA Miller-Rabin kernel against known primes and composites:
```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe test_prime_kernel.py 2>&1"
```

### `test_ap_finder.py`
Validates the AP-finding kernel with known small progressions (AP-3, AP-5) and a small sample near the target range (~10¹⁵):
```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe test_ap_finder.py 2>&1"
```

### `estimate_ap28.py`
Feasibility estimation for AP-28 search:
```powershell
.venv\Scripts\python.exe estimate_ap28.py
```

---

## How It Works

### Phase 1 — LLL Resonance Targeting
- Takes imaginary parts of Riemann zeros `t₁, t₂, t₃`
- Converts to angular frequencies `αᵢ = tᵢ / 2π`
- Constructs a 4D integer lattice and runs LLL reduction (SymPy)
- Extracts a resonant multiplier to target numbers near 10¹⁵

### Phase 2 — GPU/CPU Sieve
- Generates a contiguous block of candidate starting values
- For each candidate `a`, tests the sequence `a, a+d, a+2d, ..., a+(k-1)d`
- Step size `d` is the **primorial of all primes less than or equal to `k`**, computed dynamically by `get_required_primorial(k)`:

  | k | Primes <= k | Primorial d |
  |---|---:|---:|
  | 7 | 2, 3, 5, 7 | 210 |
  | 8 | 2, 3, 5, 7 | 210 |
  | 9 | 2, 3, 5, 7 | 210 |
  | 28 | 2, 3, 5, 7, 11, 13, 17, 19, 23 | 223,092,870 |

- Uses deterministic Miller-Rabin with 12 witnesses (guaranteed for 64-bit)

### Algorithm Variants

| Script | Strategy | Description |
|--------|----------|-------------|
| `rbls_gpu_pipeline.py` | Direct AP test | Each candidate `a` tests if `a, a+d, ..., a+(k-1)d` are all prime. Early exit on first composite. |
| `rbls_m1_pipeline.py` | Direct AP test | Same as GPU but uses Numba parallel CPU on Apple Silicon. |
| `rbls_gpu_pipeline_ap8.py` | Direct AP test | CUDA AP-8 variant with a Hardy-Littlewood-style startup estimate. |
| `rbls_m1_pipeline_ap8.py` | Direct AP test | Apple Silicon AP-8 variant that found the reported AP-8 progression. |
| `rbls_gpu_pipeline_ap9.py` | Direct AP test | CUDA AP-9 variant with progress reporting during each batch. |
| `rbls_m1_pipeline_ap9.py` | Direct AP test | Apple Silicon AP-9 variant used for the reported negative search. |
| `rbls_gpu_pipeline_ap28.py` | Prime-find then scan | Experimental AP-28 prototype. It now exits early if the configured range is too narrow for the required AP-28 span. |

---

## Known Results

The AP-7 pipeline discovered:
```
a_n = 999,721,467,601,817 + n × 210,   for n = 0, 1, ..., 6
```
All 7 terms verified prime via independent CPU-side Miller-Rabin and trial division.

The AP-8 M1 pipeline discovered:
```
a_n = 999,721,631,514,707 + n × 210,   for n = 0, 1, ..., 7
```
All 8 terms verified prime via deterministic Miller-Rabin and SymPy `isprime()`.

AP-9 searches over roughly 7 billion raw candidate starts did not find a 9-term progression. Under a Hardy-Littlewood-style baseline for `d=210`, this is a plausible miss rather than a contradiction of the AP-7/AP-8 results.

---

## Troubleshooting

| Error | Likely Fix |
|-------|------------|
| `ModuleNotFoundError: No module named 'numpy'` | Activate venv and `pip install numpy` |
| `ModuleNotFoundError: No module named 'pycuda'` | Install CUDA Toolkit, then `pip install pycuda` |
| `OSError: nvcc not found` | Add CUDA Toolkit `bin` folder to PATH |
| `fatal error C1083` / `cl.exe` errors | Run via `vcvars64.bat` as shown above |
| `numba` errors (M1 pipeline) | `pip install numba` (requires LLVM) |
| GPU at 100% but no output | First batch can take 20-60s depending on k; check `nvidia-smi` for GPU activity |
