import json
import math
from pathlib import Path

from sympy import primerange

from research.pattern_counting import PATTERNS, PatternCounter, direct_count, measure

SAVED = Path(__file__).resolve().parents[1] / "results" / "pattern-counting.json"


def test_recursion_is_exact_for_every_pattern():
    for name in PATTERNS:
        for x in (100, 1000, 4097):
            row = measure(name, x)
            assert row["count"] == row["direct_count"]


def test_single_form_states_collapse_and_patterns_do_not():
    x = 2**14
    primes = list(primerange(2, math.isqrt(x) + 1))
    single = PatternCounter((0,), primes)
    single.count(x, single.root)
    # Every substitution t = p*s fixes the bad set {0}: one state per prefix.
    assert len(single.state_list) == len(primes) + 1
    twins = PatternCounter((0, 2), list(primerange(2, math.isqrt(x + 2) + 1)))
    twins.count(x, twins.root)
    assert len(twins.state_list) > 20*len(primes)


def test_twin_substitution_remembers_the_residue():
    primes = list(primerange(2, 40))
    counter = PatternCounter((0, 2), primes)
    children = {counter.child(counter.root, r) for r in counter.state_list[counter.root][-1]}
    # The two roots modulo the largest prime give different subproblems.
    assert len(children) == 2


def test_direct_count_matches_brute_force():
    primes = [2, 3, 5, 7]
    brute = sum(all((t + o) % q for o in (0, 2) for q in primes) for t in range(500))
    assert direct_count((0, 2), primes, 500) == brute


def test_saved_report_shows_superlinear_pattern_growth():
    data = json.loads(SAVED.read_text())
    blocks = data["patterns"]
    assert blocks["primes"]["subproblem_growth_exponent"] < 0.9
    for name in ("twins", "ap3_d6", "ap5_d30"):
        assert blocks[name]["subproblem_growth_exponent"] > 1.0
        assert all(r["count"] == r["direct_count"] for r in blocks[name]["rows"])
