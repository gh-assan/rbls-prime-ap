import json
from math import lcm
from pathlib import Path

from sympy import isprime

from research.record_extensions import RECORDS, certificate


def test_every_published_record_is_prime_and_every_ap28_window_is_blocked():
    report = certificate()
    assert len(report["records"]) == len(RECORDS) == 8
    for record in report["records"]:
        a, d, length = record["start"], record["difference"], record["length"]
        assert d % 223092870 == 0 and d % 29
        assert all(isprime(a + j*d) for j in range(length))
        # Both adjacent neighbors are blocked, which gives the 14-term bound.
        assert [b["index"] for b in record["neighbor_blocks"]] == [-1, length]
        windows = record["ap28_windows"]
        assert [w["window_first_index"] for w in windows] == list(range(length - 28, 1))
        # Since 29 does not divide d, exactly one window avoids the zero class.
        assert sum(w["survives_modulo_29"] for w in windows) == 1
        for b in record["neighbor_blocks"] + [w["blocking_term"] for w in windows]:
            assert not 0 <= b["index"] < length
            assert b["value"] == a + b["index"]*d
            if b["reason"] == "proper divisor":
                assert 1 < b["divisor"] < b["value"]
                assert b["divisor"]*b["cofactor"] == b["value"]
            else:
                assert b["value"] < 2
    assert report["windows_excluded"] == 20
    assert not report["ap28_witness_supplied"]


def test_overlap_lemma_forces_equal_differences_for_records_of_length_26_and_27():
    # 15 common terms span at least 14*lcm(d,e), at most 25*d or 26*d and 27*e.
    for length in (26, 27):
        assert (length - 1) < 2*14 and 27 < 2*14
        for d in range(1, 7):
            source = {100 + j*d for j in range(length)}
            for e in range(1, 7):
                for start in (97, 100, 103):
                    overlap = sorted(source & {start + j*e for j in range(28)})
                    if len(overlap) > 1:
                        assert overlap[-1] - overlap[0] >= (len(overlap) - 1)*lcm(d, e)
                    if d != e:
                        assert len(overlap) <= 14


def test_saved_record_certificate_is_reproducible():
    path = Path(__file__).resolve().parents[1] / "results" / "record-extension-checks.json"
    assert json.loads(path.read_text()) == certificate()
