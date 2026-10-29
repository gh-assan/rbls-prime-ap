"""Verify one published AP27 and reject its algebraically selected extension.

This is a fixed candidate check. It generates no search ranges or variants.
"""
import json
from pathlib import Path

from prime_ap import is_prime


SOURCE = "https://www.primegrid.com/forum_thread.php?id=7012&nowrap=true"
START = 973044677408627339
DIFFERENCE = 174505864 * 223092870


def certificate():
    terms = [START + j * DIFFERENCE for j in range(27)]
    if not all(is_prime(n) for n in terms):
        raise ValueError("a published AP27 term failed primality verification")
    root = (-START * pow(DIFFERENCE, -1, 29)) % 29
    if root != 27:
        raise ValueError("the source progression has an unexpected residue modulo 29")
    left = START - DIFFERENCE
    right = START + 27 * DIFFERENCE
    if left != 2971 * 314410522846529 or right != 29 * 69799381250398231:
        raise ValueError("an exact proper-divisor certificate failed")
    return {
        "status": "Fixed AP28 candidate rejected by a proper divisor; construction goal remains open.",
        "source": SOURCE,
        "source_message_id": 189807,
        "source_discoverer": "Kai Presler, PrimeGrid",
        "source_discovery_date": "2026-08-02",
        "published_ap27_start": START,
        "published_ap27_difference": DIFFERENCE,
        "published_ap27_terms": terms,
        "reference_uint64_verifier_confirms_all_27": True,
        "zero_term_index_modulo_29": root,
        "algebraically_selected_extension_index": -1,
        "derived_ap28_start": left,
        "derived_ap28_difference": DIFFERENCE,
        "new_term": left,
        "new_term_proper_divisor": 2971,
        "new_term_cofactor": 314410522846529,
        "opposite_extension_term": right,
        "opposite_extension_proper_divisor": 29,
        "opposite_extension_cofactor": 69799381250398231,
        "max_shared_terms_with_any_positive_difference_prime_ap28": 14,
        "overlap_bound_scope": "This fixed published AP27, using the integer progression overlap lemma and both composite neighbors.",
        "ap28_witness_supplied": False,
        "positive_ap28_arithmetic_bound_supplied": False,
    }


if __name__ == "__main__":
    report = certificate()
    destination = Path(__file__).resolve().parents[1] / "results" / "published-ap27-extension-check.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
