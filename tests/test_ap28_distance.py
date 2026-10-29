import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

from research.ap28_distance import (
    PRIMEGRID_FOUND, local_information, model_count, poisson_interval,
    q_from_counts, window_ratios)

SAVED = Path(__file__).resolve().parents[1] / "results" / "ap28-distance.json"


def test_window_ratios_match_exact_enumeration_of_the_four_outer_terms():
    q = Fraction(1, 11)
    counts = {26: 0, 27: 0, 28: 0}
    # Outer indices -2,-1 (left) and 24,25 (right) around a prime 24-term core.
    for left2, left1, right1, right2 in product((0, 1), repeat=4):
        weight = math.prod(q if bit else 1 - q for bit in (left2, left1, right1, right2))
        length = 24 + (left1 + left1*left2) + (right1 + right1*right2)
        if length >= 26:
            counts[length] += weight
    r26, r27 = window_ratios(q)
    assert counts[26]/counts[27] == r26 and counts[27]/counts[28] == r27
    assert q_from_counts(71, 4) == 12/146


def test_poisson_interval_has_the_stated_tail_probabilities():
    lo, hi = poisson_interval(4)
    upper_tail = 1 - sum(math.exp(-lo)*lo**i/math.factorial(i) for i in range(4))
    lower_tail = sum(math.exp(-hi)*hi**i/math.factorial(i) for i in range(5))
    assert abs(upper_tail - 0.025) < 1e-4 and abs(lower_tail - 0.025) < 1e-4


def test_coarse_quadrature_agrees_with_saved_values_and_the_g11_enclosure():
    saved = json.loads(SAVED.read_text())
    assert 13.270 <= saved["model_counts_below_2_64"]["28"] <= 13.876
    coarse = model_count(28, a_nodes=400, m_nodes=80)
    assert abs(coarse/saved["model_counts_below_2_64"]["28"] - 1) < 0.03


def test_local_information_is_monotone_and_saved_report_is_consistent():
    saved = json.loads(SAVED.read_text())
    rows = local_information((23, 59, 541))
    assert [round(r["bits"], 9) for r in rows] == [
        round(r["bits"], 9) for r in saved["local_information"][:3]]
    bits = [r["bits"] for r in saved["local_information"]]
    assert bits == sorted(bits)
    assert saved["primegrid_found"] == {str(k): v for k, v in PRIMEGRID_FOUND.items()}
    assert saved["maximal_ap27_per_ap28_data_range"][0] < 22.4 < saved["maximal_ap27_per_ap28_data_range"][1]
    assert not saved["ap28_witness_supplied"]
