"""Certify that no published AP26/AP27 record extends to a prime AP28.

Every candidate is forced by the overlap lemma: an AP28 sharing at least 15
terms with a record keeps its difference and covers one of a few fixed index
windows. No starts, differences, or CRT classes are searched.
"""
import json
from pathlib import Path

from sympy import factorint, isprime as sympy_isprime

from prime_ap import is_prime


PRIMORIAL_23 = 223092870
RECORD_TABLE = "https://www.pzktupel.de/PAP/aprecords.php"
RECORD_TABLE_UPDATED = "2026-10-12"

# (label, discoverer, date, length, start, multiplier of 23#, source)
RECORDS = (
    ("Gahan 2019", "Rob Gahan, PrimeGrid", "2019-09-23", 27,
     224584605939537911, 81292139, "https://oeis.org/A327760"),
    ("Greer 2023", "Tom Greer, PrimeGrid", "2023-05-26", 27,
     277699295941594831, 170826477, "https://oeis.org/A363980"),
    ("Kwok 2023", "Michael Kwok, PrimeGrid", "2023-12-10", 27,
     605185576317848261, 155368778, "https://oeis.org/A374949"),
    ("Presler 2026", "Kai Presler, PrimeGrid", "2026-08-02", 27,
     973044677408627339, 174505864,
     "https://www.primegrid.com/forum_thread.php?id=7012&nowrap=true"),
    ("Perichon 2010", "Benoit Perichon, PrimeGrid", "2010-04-12", 26,
     193384694*PRIMORIAL_23 + 197182411, 23681770, RECORD_TABLE),
    ("Fry 2012", "James Fry", "2012-03-26", 26,
     15626261*PRIMORIAL_23 + 59138353, 1666981, RECORD_TABLE),
    ("Jayaputera 2025", "James Jayaputera, PrimeGrid", "2025", 26,
     1688330176*PRIMORIAL_23 + 138131087, 397344516, RECORD_TABLE),
    ("Carquillat 2026", "Christian Carquillat, PrimeGrid", "2026-09-12", 26,
     216517777*PRIMORIAL_23 + 148739693, 531515022, RECORD_TABLE),
)


def proper_divisor(n):
    """Smallest prime factor below 10**8 of a composite n, or None."""
    if n < 4 or sympy_isprime(n):
        return None
    p = min(factorint(n, limit=10**8))
    return p if 1 < p < n and n % p == 0 else None


def block(start, difference, index):
    """Exact reason that term `index` cannot belong to a prime progression."""
    n = start + index*difference
    if n < 2:
        return {"index": index, "value": n, "reason": "not an integer at least 2"}
    p = proper_divisor(n)
    if p is None:
        return None
    return {"index": index, "value": n, "reason": "proper divisor",
            "divisor": p, "cofactor": n // p}


def record_certificate(label, discoverer, date, length, start, multiplier, source):
    difference = multiplier*PRIMORIAL_23
    terms = [start + j*difference for j in range(length)]
    if not all(is_prime(n) for n in terms):
        raise ValueError(f"{label}: a published term failed primality verification")
    zero = (-start*pow(difference, -1, 29)) % 29
    neighbors = [block(start, difference, i) for i in (-1, length)]
    if not all(neighbors):
        raise ValueError(f"{label}: an adjacent neighbor is not excluded")
    windows = []
    for s in range(length - 28, 1):
        outside = [i for i in range(s, s + 28) if not 0 <= i < length]
        blocks = [b for b in (block(start, difference, i) for i in outside) if b]
        if not blocks:
            raise ValueError(f"{label}: window starting at {s} is not excluded")
        best = min(blocks, key=lambda b: b.get("divisor", 0))
        windows.append({
            "window_first_index": s,
            "survives_modulo_29": all((i - zero) % 29 for i in range(s, s + 28)),
            "blocking_term": best,
        })
    return {
        "label": label,
        "discoverer": discoverer,
        "date": date,
        "source": source,
        "length": length,
        "start": start,
        "difference": difference,
        "multiplier_of_23_primorial": multiplier,
        "last_term": terms[-1],
        "all_terms_verified_prime": True,
        "zero_index_modulo_29": zero,
        "neighbor_blocks": neighbors,
        "ap28_windows": windows,
    }


def certificate():
    records = [record_certificate(*r) for r in RECORDS]
    return {
        "status": "Every published AP26/AP27 record listed here is maximal toward AP28; no AP28 is supplied.",
        "record_table": RECORD_TABLE,
        "record_table_last_updated": RECORD_TABLE_UPDATED,
        "longest_known_on_record_table": 27,
        "records": records,
        "windows_excluded": sum(len(r["ap28_windows"]) for r in records),
        "max_shared_terms_with_any_prime_ap28": 14,
        "overlap_bound_scope": "Each listed record, by the overlap lemma of G12 and the exact blocking terms.",
        "ap28_witness_supplied": False,
    }


if __name__ == "__main__":
    report = certificate()
    destination = Path(__file__).resolve().parents[1] / "results" / "record-extension-checks.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))
