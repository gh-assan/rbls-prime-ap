"""Calibrate the distance to an AP28 against PrimeGrid's actual record counts.

Model quantities here are numerical quadratures of the prime-tuple density,
not enclosures and not arithmetic bounds. Local sieve fractions are exact
products evaluated in floating point. No starts or differences are searched.
"""
import json
import math
from pathlib import Path

import numpy as np
from sympy import primerange


PRIMORIAL_23 = 223092870
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)
HEIGHT = 2**64 - 1

PRIMEGRID_STATS = "https://www.primegrid.com/stats_ap26.php"
PRIMEGRID_ACCESSED = "2026-10-29"
# Lengths found by PrimeGrid's AP26/AP27 program (stats page totals).
PRIMEGRID_FOUND = {20: 1723364, 21: 413368, 22: 93527, 23: 20660,
                   24: 4144, 25: 663, 26: 71, 27: 4, 28: 0}
AP27_DATES = ("2019-09-23", "2023-05-26", "2023-12-10", "2026-08-02")


def singular_series(k, limit=10**7):
    """Local constant for a+j*23#*m, 0<=j<k, truncated at `limit`."""
    total = 0.0
    for p in primerange(2, limit):
        if PRIMORIAL_23 % p == 0:
            total -= (k - 1)*math.log1p(-1/p)
        else:
            total += math.log1p(-(k - 1)/p) - (k - 1)*math.log1p(-1/p)
    return math.exp(total)


def cone_integral(k, height=HEIGHT, a_nodes=4000, m_nodes=400):
    """Midpoint quadrature of prod_j 1/log(a+j*23#*m) over the cone, log scale."""
    D = PRIMORIAL_23
    W = (k - 1)*D
    us = np.linspace(math.log(2), math.log(height - W), a_nodes)
    total = 0.0
    for u0, u1 in zip(us, us[1:]):
        a = math.exp((u0 + u1)/2)
        m_max = (height - a)/W
        if m_max <= 1:
            continue
        vs = np.linspace(0, math.log(m_max), m_nodes)
        m = np.exp((vs[1:] + vs[:-1])/2)
        f = np.ones_like(m)
        for j in range(k):
            f /= np.log(a + j*D*m)
        total += a*(u1 - u0)*float(np.sum(f*m))*(vs[1] - vs[0])
    return total


def model_count(k, **kwargs):
    return singular_series(k)*cone_integral(k, **kwargs)


def neighbor_probability(height, limit=10**7):
    """Heuristic chance that the one neighbor of an AP27 surviving 29 is prime.

    Primes up to 23 cannot divide it; it is nonzero modulo 29 by selection;
    for p>=31 the 27 prime terms leave p-27 equally likely zero indices.
    """
    factor = math.prod(p/(p - 1) for p in SMALL_PRIMES)*29/28
    for p in primerange(31, limit):
        factor *= (p/(p - 1))*(p - 27)/(p - 26)
    return factor/math.log(height)


def window_ratios(q):
    """Maximal-length ratios in the program's fixed 28-term window.

    With the 24-term core prime and the four outer terms independently prime
    with chance q: P26/P27 = (3-q)/(2q) and P27/P28 = 2(1-q)/q.
    """
    return (3 - q)/(2*q), 2*(1 - q)/q


def q_from_counts(n26, n27):
    """Invert (3-q)/(2q) = n26/n27."""
    return 3*n27/(2*n26 + n27)


def poisson_interval(n):
    """Exact central 95% interval for a Poisson mean given n events (n=4)."""
    table = {4: (1.0899, 10.2416)}
    return table[n]


def local_information(limits=(23, 59, 541, 10**4, 10**6, 10**7)):
    """Fraction of cone cells surviving every local condition at primes <= y."""
    log_fraction = sum(math.log1p(-1/p) for p in SMALL_PRIMES)
    rows = []
    primes = iter(primerange(29, max(limits) + 1))
    pending = next(primes)
    for y in limits:
        while pending is not None and pending <= y:
            p = pending
            log_fraction += math.log((p - 1)*(p - 27)/p**2)
            pending = next(primes, None)
        rows.append({"y": y, "bits": -log_fraction/math.log(2)})
    return rows


def report(a_nodes=4000, m_nodes=400):
    W = 27*PRIMORIAL_23
    cells = (HEIGHT - 2 - W)**2/(2*W)
    counts = {k: model_count(k, a_nodes=a_nodes, m_nodes=m_nodes) for k in (26, 27, 28)}
    q_data = q_from_counts(PRIMEGRID_FOUND[26], PRIMEGRID_FOUND[27])
    q_model = {f"{h:.0e}": neighbor_probability(h) for h in (2e17, 1e18, 2e18)}
    lo, hi = poisson_interval(PRIMEGRID_FOUND[27])
    info = local_information()
    for row in info:
        row["cells_per_expected_ap28"] = cells*2**-row["bits"]/counts[28]
    return {
        "status": "Calibration of a heuristic model against actual record counts; no AP28 and no arithmetic bound supplied.",
        "primegrid_stats": PRIMEGRID_STATS,
        "primegrid_accessed": PRIMEGRID_ACCESSED,
        "primegrid_found": PRIMEGRID_FOUND,
        "ap27_discovery_dates": AP27_DATES,
        "cone_cells_below_2_64": cells,
        "model_counts_below_2_64": counts,
        "model_ratio_26_27": counts[26]/counts[27],
        "model_ratio_27_28": counts[27]/counts[28],
        "bits_to_isolate_one_ap28": math.log2(cells/counts[28]),
        "q_from_primegrid_26_27": q_data,
        "maximal_ap27_per_ap28_from_data": window_ratios(q_data)[1],
        "ap27_poisson_95": [lo, hi],
        "maximal_ap27_per_ap28_data_range": sorted(
            window_ratios(q_from_counts(PRIMEGRID_FOUND[26], n27))[1] for n27 in (lo, hi)),
        "q_model_by_height": q_model,
        "maximal_ap27_per_ap28_model": {h: window_ratios(q)[1] for h, q in q_model.items()},
        "predicted_ap26_per_ap27_model_1e18": window_ratios(q_model["1e+18"])[0],
        "observed_ap26_per_ap27": PRIMEGRID_FOUND[26]/PRIMEGRID_FOUND[27],
        "local_information": info,
        "ap28_witness_supplied": False,
    }


if __name__ == "__main__":
    data = report()
    destination = Path(__file__).resolve().parents[1] / "results" / "ap28-distance.json"
    destination.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))
