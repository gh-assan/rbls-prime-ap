# RBLS (Riemann-Based Lattice Sieve) — Arithmetic Progression Prime Finder

This project searches for **length-7 arithmetic progressions of primes** (AP-7) using a hybrid approach:

1. **Analytic Phase:** Uses the imaginary parts of the first three Riemann zeta zeros and SymPy's LLL lattice reduction to compute a resonance-aligned starting magnitude (~10¹⁵).
2. **Discrete Sieve:** Tests candidate numbers in batches using a deterministic Miller-Rabin primality test (64-bit, 12-witness, guaranteed correct for all `n < 2⁶⁴`).

Two implementations are provided:

| Script | Platform | Engine |
|--------|----------|--------|
| `rbls_gpu_pipeline.py` | Windows + NVIDIA GPU (Tesla T4, etc.) | CUDA via PyCUDA |
| `rbls_m1_pipeline.py` | macOS Apple Silicon (M1/M2/M3) | Numba JIT + parallel CPU |

---

## Prerequisites

### For `rbls_gpu_pipeline.py` (GPU — Windows)

- Windows 10/11
- Microsoft Visual Studio Build Tools 2022 (or VS 2022) with **VC++ toolset**
- NVIDIA GPU with Compute Capability ≥ 3.0 (e.g., Tesla T4, RTX series)
- NVIDIA CUDA Toolkit (matching your GPU driver)
- Python 3.10+ (64-bit)

### For `rbls_m1_pipeline.py` (Apple Silicon — macOS)

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

### GPU Pipeline (Windows)

The GPU script requires the Visual Studio Build Tools environment to be loaded **before** running. Use a single `cmd.exe` invocation:

```powershell
cmd.exe /c "`"D:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" && .venv\Scripts\python.exe rbls_gpu_pipeline.py 2>&1"
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

---

## How It Works

1. **Phase 1 — LLL Resonance Targeting**
   - Takes imaginary parts of Riemann zeros `t₁, t₂, t₃`
   - Converts to angular frequencies `αᵢ = tᵢ / 2π`
   - Constructs a 4D integer lattice and runs LLL reduction (SymPy)
   - Extracts a resonant multiplier to target numbers near 10¹⁵

2. **Phase 2 — GPU/CPU Sieve**
   - Generates a contiguous block of candidate starting values
   - For each candidate `a`, tests the sequence `a, a+d, a+2d, ..., a+(k-1)d`
   - Step size `d = 210` (primorial P₇ = 2·3·5·7)
   - Uses deterministic Miller-Rabin with 12 witnesses (guaranteed for 64-bit)

---

## Troubleshooting

| Error | Likely Fix |
|-------|------------|
| `ModuleNotFoundError: No module named 'numpy'` | Activate venv and `pip install numpy` |
| `ModuleNotFoundError: No module named 'pycuda'` | Install CUDA Toolkit, then `pip install pycuda` |
| `OSError: nvcc not found` | Add CUDA Toolkit `bin` folder to PATH |
| `fatal error C1083` / `cl.exe` errors | Run via `vcvars64.bat` as shown above |
| `numba` errors (M1 pipeline) | `pip install numba` (requires LLVM) |
