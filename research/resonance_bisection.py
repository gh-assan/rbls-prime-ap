"""Experiment C1 of the domain-ladder brainstorm: resonance bisection.

Sieve survivors are periodic modulo M, the product of the sieve primes. The
number of survivors in an interval is exactly a sum over frequencies h mod M
of a product of local Dirichlet kernels times an interval kernel. This module
keeps only the most resonant frequencies and measures whether the truncated
counts can steer a bisection to survivors more cheaply than wheel enumeration.

Small analog: AP-10 with difference 210, starts near 10**9. Exact survivor
counts come from direct sieving. Fluctuation variances come from an exact
pair-correlation formula, so the captured share needs no sampling.
"""
import json
import math
from pathlib import Path

import numpy as np
from sympy import ZZ, primerange
from sympy.polys.matrices import DomainMatrix


K = 10
D = 210
START = 10**9
LENGTH = 2**20
CHECKPOINTS = (1, 16, 256, 4096, 65536)


def sieve_primes(y):
    return [2, 3, 5, 7] + list(primerange(11, y + 1))


class SieveSpectrum:
    """Survivors of a+j*D, 0<=j<K, coprime to every sieve prime."""

    def __init__(self, y, start=START, length=LENGTH):
        self.y, self.start, self.length = y, start, length
        self.primes = sieve_primes(y)
        self.M = math.prod(self.primes)
        self.good, self.ghat = {}, {}
        for p in self.primes:
            bad = {(-D*j) % p for j in range(K)}
            good = np.array([x for x in range(p) if x not in bad])
            self.good[p] = good
            t = np.arange(p)
            # ghat_p(t) = sum over good x of e(-t*x/p)
            self.ghat[p] = np.exp(-2j*np.pi*np.outer(t, good)/p).sum(axis=1)
        self.crt = {p: pow(self.M // p, -1, p) for p in self.primes}
        self.density = math.prod(len(self.good[p])/p for p in self.primes)

    def survivors(self):
        a = self.start + np.arange(self.length, dtype=np.int64)
        mask = np.ones(self.length, bool)
        for p in self.primes:
            allowed = np.zeros(p, bool)
            allowed[self.good[p]] = True
            mask &= allowed[a % p]
        return mask

    def coefficients(self, h):
        """Exact c_h = prod_p ghat_p(h*(M/p)^-1 mod p)/p for h in [0,M)."""
        h = np.asarray(h, dtype=np.int64)
        c = np.ones(h.shape, complex)
        for p in self.primes:
            c *= self.ghat[p][(h % p)*self.crt[p] % p]/p
        return c

    def magnitudes(self, h):
        h = np.asarray(h, dtype=np.int64)
        m = np.ones(h.shape)
        for p in self.primes:
            m *= np.abs(self.ghat[p])[(h % p)*self.crt[p] % p]/p
        return m

    def frequencies_from_local(self, local):
        """h with prescribed local components h_p, via h = sum h_p*(M/p) mod M."""
        h = np.zeros(len(next(iter(local.values()))), dtype=np.int64)
        for p, hp in local.items():
            h = (h + (np.asarray(hp, dtype=np.int64) % p)*(self.M // p)) % self.M
        return h

    def fluctuation_variance(self, ell):
        """Exact variance over all positions s mod M of the count in [s,s+ell)."""
        t = np.arange(-(ell - 1), ell)
        pair = np.ones(t.shape)
        for p in self.primes:
            allowed = np.zeros(p, bool)
            allowed[self.good[p]] = True
            both = np.array([np.count_nonzero(allowed & np.roll(allowed, -s))
                             for s in range(p)])
            pair *= both[t % p]/p
        second = float(np.sum((ell - np.abs(t))*pair))
        return second - (ell*self.density)**2


def interval_kernel(theta, ell):
    """|sum_{u<ell} e(u*theta)| for theta in [0,1)."""
    s = np.sin(np.pi*theta)
    out = np.full(theta.shape, float(ell))
    nz = np.abs(s) > 1e-15
    out[nz] = np.abs(np.sin(np.pi*ell*theta[nz])/s[nz])
    return out


def scores(spec, h, ell):
    return spec.magnitudes(h)*interval_kernel((h % spec.M)/spec.M, ell)


def optimal_frequencies(spec, levels, rmax, chunk=2**24):
    """Top-rmax frequencies of the full spectrum by |c_h|*|G_ell(h/M)|."""
    best = {ell: (np.empty(0), np.empty(0, dtype=np.int64)) for ell in levels}
    for lo in range(0, spec.M, chunk):
        h = np.arange(lo, min(spec.M, lo + chunk), dtype=np.int64)
        mag = spec.magnitudes(h)
        for ell in levels:
            sc = mag*interval_kernel(h/spec.M, ell)
            keep = np.argpartition(sc, -rmax)[-rmax:] if len(sc) > rmax else np.arange(len(sc))
            s0, h0 = best[ell]
            s1 = np.concatenate([s0, sc[keep]])
            h1 = np.concatenate([h0, h[keep]])
            top = np.argsort(-s1)[:rmax]
            best[ell] = (s1[top], h1[top])
    return {ell: hs for ell, (_, hs) in best.items()}


def lll_frequencies(spec, ell, coefficient_range=2, depth=8):
    """Resonant frequencies from short vectors of a phase lattice.

    A vector (v_p) gives local components h_p = v_p*sigma_p, with
    sigma_p = D^-1 mod p for p>=11, so the local kernel peaks when v_p is small.
    The last coordinate measures ell*theta, the interval phase.
    """
    scale = 2**12
    n = len(spec.primes)
    sigma = [1 if D % p == 0 else pow(D, -1, p) for p in spec.primes]
    rows = []
    for i, p in enumerate(spec.primes):
        row = [0]*(n + 1)
        row[i] = scale
        row[n] = round(scale*ell*sigma[i]/p)
        rows.append(row)
    rows.append([0]*n + [scale*ell])
    basis = DomainMatrix([[ZZ(x) for x in r] for r in rows], (n + 1, n + 1), ZZ).lll()
    basis = np.array(basis.to_Matrix().tolist(), dtype=np.int64)[:, :n] // scale
    order = np.argsort(np.abs(basis).sum(axis=1))
    vecs = basis[order[:depth]]
    grid = np.array(np.meshgrid(*[np.arange(-coefficient_range, coefficient_range + 1)]*len(vecs),
                                indexing="ij")).reshape(len(vecs), -1).T
    v = grid @ vecs
    local = {p: v[:, i]*sigma[i] for i, p in enumerate(spec.primes)}
    return np.unique(spec.frequencies_from_local(local))


def small_support_frequencies(spec, support=2):
    """All frequencies with any small-prime part and at most `support` big primes active."""
    small = [p for p in spec.primes if D % p == 0]
    big = [p for p in spec.primes if D % p]
    parts = [np.zeros(1, dtype=np.int64)]
    for p in small:
        parts = [(x[:, None] + (np.arange(p)*(spec.M//p) % spec.M)[None, :]).ravel() % spec.M
                 for x in parts]
    base = parts[0]
    pieces = [np.zeros(1, dtype=np.int64)]
    singles = {p: (np.arange(1, p)*(spec.M//p)) % spec.M for p in big}
    pieces += list(singles.values())
    if support >= 2:
        for i, p in enumerate(big):
            for q in big[i + 1:]:
                pieces.append(((singles[p][:, None] + singles[q][None, :]) % spec.M).ravel())
    big_part = np.concatenate(pieces)
    return ((base[:, None] + big_part[None, :]) % spec.M).ravel()


def captured_share(spec, h, ell, checkpoints=CHECKPOINTS):
    """Share of the exact fluctuation variance carried by the top-R frequencies."""
    h = np.unique(h[h != 0])
    c = spec.coefficients(h)
    g = interval_kernel(h/spec.M, ell)
    mass = np.sort(np.abs(c*g)**2)[::-1]
    total = spec.fluctuation_variance(ell)
    cum = np.cumsum(mass)
    return {str(r): float(cum[min(r, len(cum)) - 1]/total) for r in checkpoints}, total


def node_estimates(spec, h, ell, offsets, checkpoints=None):
    """Re sum_h c_h e(h*s/M) G_ell(h/M) for nodes starting at start+offsets.

    Returns {R: estimates using the first R frequencies of h} at each checkpoint.
    """
    h = np.asarray(h, dtype=np.int64)
    checkpoints = sorted({min(r, len(h)) for r in (checkpoints or [len(h)])})
    c = spec.coefficients(h)
    base = np.array([((spec.start % spec.M)*int(x) % spec.M)/spec.M for x in h])
    theta = h/spec.M
    nonzero = np.abs(np.sin(np.pi*theta)) > 1e-15
    g = np.full(h.shape, complex(ell))
    g[nonzero] = (np.exp(2j*np.pi*ell*theta[nonzero]) - 1)/(np.exp(2j*np.pi*theta[nonzero]) - 1)
    weight = c*g
    offsets = np.asarray(offsets, dtype=np.float64)
    running = np.zeros(len(offsets))
    out, done = {}, 0
    for r in checkpoints:
        for lo in range(done, r, 1024):
            sl = slice(lo, min(r, lo + 1024))
            phase = np.exp(2j*np.pi*(base[sl][None, :] + np.outer(offsets, theta[sl])))
            running += np.real(phase*weight[sl][None, :]).sum(axis=1)
        done = r
        out[r] = running.copy()
    return out


def accuracy(spec, mask, h_ranked, ell, checkpoints=CHECKPOINTS):
    offsets = np.arange(0, spec.length, ell)
    exact = mask.reshape(-1, ell).sum(axis=1)
    est_at = node_estimates(spec, h_ranked, ell, offsets, checkpoints)
    out = {}
    for r in checkpoints:
        est = est_at[min(r, len(h_ranked))]
        out[str(r)] = {
            "occupancy_accuracy": float(np.mean((est >= 0.5) == (exact >= 1))),
            "mean_abs_error": float(np.mean(np.abs(est - exact))),
        }
    return out, float(np.mean(exact >= 1))


def bisection(spec, mask, ranked, r, leaf):
    """4-ary descent keeping children with truncated count >= 1/2."""
    levels = sorted(ranked, reverse=True)
    kept = [0]
    evaluated = 0
    for ell in levels[1:]:
        children = np.array([o + i*ell for o in kept for i in range(4)])
        if len(children) == 0:
            break
        est = node_estimates(spec, ranked[ell][:r], ell, children)[min(r, len(ranked[ell]))]
        evaluated += len(children)
        kept = list(children[est >= 0.5])
        if ell == leaf:
            break
    found = sum(int(mask[o:o + leaf].sum()) for o in kept)
    return {"frequencies": r, "nodes_evaluated": evaluated,
            "fourier_terms": evaluated*r + r*len(spec.primes)*(len(levels) - 1),
            "leaves_kept": len(kept), "survivors_found": found,
            "survivors_total": int(mask.sum())}


def wheel_cost(spec):
    """Cells a wheel over primes with product <= LENGTH visits, and survivors."""
    wheel, prod = [], 1
    for p in spec.primes:
        if prod*p > spec.length:
            break
        wheel.append(p)
        prod *= p
    dens = math.prod(len(spec.good[p])/p for p in wheel)
    return {"wheel_primes": wheel, "wheel_cells": spec.length*dens}


def run():
    report = {"k": K, "difference": D, "start": START, "length": LENGTH,
              "status": "Experiment on a small analog; no AP28 and no proof supplied."}

    # Part A: full spectrum available (y=23, M=223092870 > LENGTH).
    spec = SieveSpectrum(23)
    mask = spec.survivors()
    levels = [2**e for e in (20, 18, 16, 14, 12, 10, 8)]
    ranked = optimal_frequencies(spec, levels, max(CHECKPOINTS))
    part_a = {"y": 23, "M": spec.M, "density": spec.density,
              "survivors": int(mask.sum()), "levels": {}}
    for ell in levels[1:]:
        acc, occupied = accuracy(spec, mask, ranked[ell], ell)
        share, var = captured_share(spec, ranked[ell], ell)
        part_a["levels"][str(ell)] = {"occupied_fraction": occupied, "variance": var,
                                      "captured_share": share, "accuracy": acc}
    part_a["bisection"] = [bisection(spec, mask, ranked, r, 2**8) for r in (256, 4096, 65536)]
    part_a["baseline"] = wheel_cost(spec)
    report["part_a_optimal"] = part_a

    # Part B: one-survivor level as y grows, LLL and small-support pools.
    part_b = []
    for y in (23, 29, 31, 37, 41, 43, 47):
        spec = SieveSpectrum(y)
        ell = 2**round(math.log2(1/spec.density))
        row = {"y": y, "M": spec.M, "density": spec.density, "level": ell}
        lll = lll_frequencies(spec, ell)
        small = small_support_frequencies(spec, 2)
        row["lll_pool"] = int(len(lll))
        row["lll_share"], row["variance"] = captured_share(spec, lll, ell)
        row["small_support_pool"] = int(len(small))
        row["small_support_share"], _ = captured_share(spec, small, ell)
        row["baseline"] = wheel_cost(spec)
        part_b.append(row)
    report["part_b_scaling"] = part_b

    # Part C: larger LLL pools at the same one-survivor level.
    part_c = []
    for y, rng, depth in ((31, 1, 11), (31, 2, 11), (37, 1, 13), (37, 2, 11), (47, 1, 14), (47, 1, 16)):
        spec = SieveSpectrum(y)
        ell = 2**round(math.log2(1/spec.density))
        pool = lll_frequencies(spec, ell, coefficient_range=rng, depth=depth)
        share, _ = captured_share(spec, pool, ell, (4096, 65536, 10**7))
        part_c.append({"y": y, "coefficient_range": rng, "depth": depth,
                       "lattice_dimension": len(spec.primes) + 1, "pool": int(len(pool)),
                       "captured_share": share})
    report["part_c_pool_depth"] = part_c
    return report


if __name__ == "__main__":
    data = run()
    out = Path(__file__).resolve().parents[1] / "results" / "resonance-bisection.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))
