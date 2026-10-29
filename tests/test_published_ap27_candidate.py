import json
from math import lcm
from pathlib import Path

import pytest
from sympy import isprime

import research.check_published_ap27 as checker
from research.check_published_ap27 import DIFFERENCE, START, certificate


def test_published_ap27_has_independently_verified_prime_terms():
    report = certificate()
    assert report["published_ap27_start"] == 4361612620*223092870 + 184607939
    assert report["published_ap27_terms"][-1] == 1985251042229959019
    assert all(isprime(n) for n in report["published_ap27_terms"])


def test_derived_candidate_is_rejected_by_exact_proper_divisors():
    report = certificate()
    assert (-START * pow(DIFFERENCE, -1, 29)) % 29 == 27
    assert all((START + j*DIFFERENCE) % 29 for j in range(-1, 27))
    assert report["new_term"] == START - DIFFERENCE
    for value, divisor, cofactor in (
        (report["new_term"], report["new_term_proper_divisor"], report["new_term_cofactor"]),
        (report["opposite_extension_term"], 29, report["opposite_extension_cofactor"]),
    ):
        assert 1 < divisor < value
        assert 1 < cofactor < value
        assert value == divisor * cofactor
        assert not isprime(value)
    assert not report["ap28_witness_supplied"]
    assert not report["positive_ap28_arithmetic_bound_supplied"]


def test_progression_overlap_bound_from_lcm_and_sharp_example():
    # Small integer progressions validate the lemma's span argument; these
    # are arbitrary integers, not discovery searches for prime candidates.
    for d in range(1, 7):
        source = {100 + j*d for j in range(27)}
        for e in range(1, 7):
            for start in (97, 100, 102):
                overlap = sorted(source & {start + j*e for j in range(28)})
                if len(overlap) > 1:
                    assert overlap[-1] - overlap[0] >= (len(overlap)-1)*lcm(d, e)
                if d != e:
                    assert len(overlap) <= 14
    assert len(set(range(0, 53, 2)) & set(range(28))) == 14


def test_saved_candidate_check_matches_its_reproducible_certificate():
    path = Path(__file__).resolve().parents[1] / "results" / "published-ap27-extension-check.json"
    assert json.loads(path.read_text()) == certificate()


def test_checker_refuses_to_issue_a_certificate_when_verification_fails(monkeypatch):
    monkeypatch.setattr(checker, "is_prime", lambda n: False)
    with pytest.raises(ValueError, match="failed primality verification"):
        checker.certificate()
