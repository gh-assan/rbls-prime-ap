import json
from pathlib import Path

import numpy as np

from research.resonance_bisection import (
    SieveSpectrum, captured_share, lll_frequencies, node_estimates,
    small_support_frequencies)

SAVED = Path(__file__).resolve().parents[1] / "results" / "resonance-bisection.json"


def small_spectrum():
    return SieveSpectrum(13, start=10**9, length=30030)


def test_full_frequency_sum_reproduces_exact_interval_counts():
    spec = small_spectrum()
    mask = spec.survivors()
    offsets = np.arange(0, 29000, 997)
    est = node_estimates(spec, np.arange(spec.M), 997, offsets)[spec.M]
    exact = np.array([mask[o:o + 997].sum() for o in offsets])
    assert np.max(np.abs(est - exact)) < 1e-8


def test_pair_correlation_variance_matches_a_full_period_and_parseval():
    spec = small_spectrum()
    mask = spec.survivors()
    ell = 64
    prefix = np.concatenate([[0], np.cumsum(np.tile(mask, 2))])
    counts = prefix[np.arange(spec.M) + ell] - prefix[np.arange(spec.M)]
    assert abs(counts.var() - spec.fluctuation_variance(ell)) < 1e-9
    share, _ = captured_share(spec, np.arange(spec.M), ell, (spec.M,))
    assert abs(share[str(spec.M)] - 1) < 1e-9


def test_frequency_generators_produce_valid_residues():
    spec = SieveSpectrum(23)
    pool = lll_frequencies(spec, 2**10, coefficient_range=1, depth=4)
    assert 0 in pool and np.all((pool >= 0) & (pool < spec.M))
    small = small_support_frequencies(spec, 1)
    # Any small-prime part times one or zero active big primes.
    assert len(np.unique(small)) == 210*(1 + sum(p - 1 for p in (11, 13, 17, 19, 23)))


def test_saved_report_records_negative_scaling_honestly():
    data = json.loads(SAVED.read_text())
    assert "no AP28" in data["status"]
    for row in data["part_b_scaling"]:
        for pool in ("lll_share", "small_support_share"):
            shares = list(row[pool].values())
            assert all(0 <= s <= 1 + 1e-9 for s in shares)
            assert shares == sorted(shares)
