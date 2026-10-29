"""Finite residue-class certificates excluding perfect powers.

This is an algebraic proof checker, not a progression search or a primality
test. A positive certificate excludes perfect powers only.
"""
from fractions import Fraction
import json
from math import gcd, prod
from operator import index
from pathlib import Path


UINT64_MAX = 2**64 - 1
DIFFERENCE_UNIT = 7 * 223092870
UNIT_GROUPS = ((3, 2, 2), (5, 4, 2), (49, 42, 3), (11, 10, 2),
               (13, 12, 2), (17, 16, 3), (19, 18, 2), (23, 22, 5))
POWER_TESTS = {
    2: ((3, 1), (5, 2), (7, 3), (11, 5), (13, 6), (17, 8), (19, 9), (23, 11)),
    3: ((7, 2), (13, 4), (19, 6)),
    5: ((11, 2),),
    7: ((49, 6),),
    11: ((23, 2),),
}
EXCEPTIONAL_POWER = 29**13
EXCEPTIONAL_RESIDUE = EXCEPTIONAL_POWER % DIFFERENCE_UNIT


def passes_power_character_tests(value):
    """Membership in S0: not an ell-th power in U(M), ell=2,3,5,7,11."""
    value = index(value) % DIFFERENCE_UNIT
    return gcd(value, DIFFERENCE_UNIT) == 1 and all(
        any(pow(value, exponent, modulus) != 1 for modulus, exponent in tests)
        for tests in POWER_TESTS.values())


def allowed_residue(value):
    """Membership in S, including exclusion of the class containing 29^13."""
    value = index(value) % DIFFERENCE_UNIT
    return value != EXCEPTIONAL_RESIDUE and passes_power_character_tests(value)


def certifies_non_power(value):
    """True proves n is not b^e, b,e>=2; False is inconclusive.

    The finite height is part of the theorem. Unsupported heights raise.
    """
    value = index(value)
    if not 2 <= value <= UINT64_MAX:
        raise ValueError("require 2 <= value < 2^64 for this certificate")
    return allowed_residue(value)


def residue_counts():
    """Exact group counts using independent primary components, no class scan."""
    orders = [order for modulus, order, generator in UNIT_GROUPS]
    unit_count = prod(orders)
    indices = {ell: prod(gcd(ell, order) for order in orders) for ell in POWER_TESTS}
    retained = prod(Fraction(i - 1, i) for i in indices.values())
    before_exception = unit_count * retained
    if before_exception.denominator != 1 or not passes_power_character_tests(EXCEPTIONAL_RESIDUE):
        raise ArithmeticError("invalid finite group certificate")
    return unit_count, indices, int(before_exception), int(before_exception) - 1


def certificate():
    unit_count, indices, before, after = residue_counts()
    example_residue = DIFFERENCE_UNIT // 2 + 2
    cofactor = example_residue * pow(31, -1, DIFFERENCE_UNIT) % DIFFERENCE_UNIT
    composite = 31 * cofactor
    assert cofactor > 1 and composite < UINT64_MAX and certifies_non_power(composite)
    return {
        "status": "Perfect-power exclusion only; no primality or AP28 certificate.",
        "domain": [2, UINT64_MAX],
        "difference_unit": DIFFERENCE_UNIT,
        "unit_residues": unit_count,
        "power_subgroup_indices": indices,
        "classes_before_exception": before,
        "classes_after_exception": after,
        "retained_unit_fraction": str(Fraction(after, unit_count)),
        "excluded_power": EXCEPTIONAL_POWER,
        "excluded_residue": EXCEPTIONAL_RESIDUE,
        "next_base_to_exponent_13": 31**13,
        "explicit_allowed_residue": example_residue,
        "composite_counterexample": {"value": composite, "factors": [31, cofactor]},
        "composite_progression_height_bound_for_every_unit_class": 58 * DIFFERENCE_UNIT + 31,
        "coverage": "Group-theoretic proof; no AP candidate enumeration.",
    }


if __name__ == "__main__":
    result = certificate()
    destination = Path(__file__).resolve().parents[1] / "results" / "power-exclusion-checks.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
