import json
from pathlib import Path

from sympy import primerange

from research.garner_tree import (
    explicit_tree, good_residues, orders, prefix_survivors, tree_work)

SAVED = Path(__file__).resolve().parents[1] / "results" / "garner-tree.json"


def test_level_accounting_matches_an_explicit_tree_for_every_order():
    primes = [2, 3, 5, 7] + list(primerange(11, 30))
    length = 2**16
    for name, order in orders(primes).items():
        surv = prefix_survivors(order, length=length)
        rows = tree_work(order, surv, length=length)
        for switch in (1, 4, 7, len(order)):
            generated, found = explicit_tree(order, switch, length=length)
            assert found == surv[-1]
            assert generated == rows[switch]["generated"]


def test_extra_level_beyond_the_window_costs_exactly_s_times_g_minus_2_plus_next():
    primes = [2, 3, 5, 7] + list(primerange(11, 60))
    length = 2**14
    order = orders(primes)["ascending"]
    surv = prefix_survivors(order, length=length)
    rows = tree_work(order, surv, length=length)
    for i in range(1, len(order)):
        if rows[i]["modulus"] > length:
            g = len(good_residues(order[i]))
            assert rows[i + 1]["work"] - rows[i]["work"] == surv[i]*(g - 2) + surv[i + 1]


def test_saved_report_best_tree_is_within_a_constant_of_the_wheel():
    data = json.loads(SAVED.read_text())
    for row in data["rows"]:
        ratios = {k: v["best_over_wheel"] for k, v in row["orders"].items()}
        assert 0.7 < min(ratios.values()) < 1.0
        assert all(v["beyond_window_identity_holds"] for v in row["orders"].values())
    assert "no AP28" in data["status"]
