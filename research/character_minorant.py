"""Finite-group minorant constants; no prime-correlation estimates or AP search."""
from fractions import Fraction
import json
from math import gcd, prod
from operator import index
from pathlib import Path

from research.power_exclusion import (
    DIFFERENCE_UNIT, EXCEPTIONAL_RESIDUE, POWER_TESTS, residue_counts,
)


SUBGROUP_INDICES = {2: 128, 3: 27, 5: 5, 7: 7, 11: 11}
EXCEPTIONAL_INVERSE = pow(EXCEPTIONAL_RESIDUE, -1, DIFFERENCE_UNIT)


def is_square_unit(value):
    value = index(value) % DIFFERENCE_UNIT
    return gcd(value, DIFFERENCE_UNIT) == 1 and all(
        pow(value, exponent, modulus) == 1
        for modulus, exponent in POWER_TESTS[2])


def subgroup_memberships(value):
    """Five bad subgroups; the first is <G^2, r_*> of index 128."""
    value = index(value) % DIFFERENCE_UNIT
    if gcd(value, DIFFERENCE_UNIT) != 1:
        raise ValueError("subgroup membership requires a unit modulo M")
    memberships = {
        ell: all(pow(value, exponent, modulus) == 1 for modulus, exponent in tests)
        for ell, tests in POWER_TESTS.items()
    }
    memberships[2] = memberships[2] or is_square_unit(value * EXCEPTIONAL_INVERSE)
    return memberships


def allowed_character_residue(value):
    value = index(value) % DIFFERENCE_UNIT
    return gcd(value, DIFFERENCE_UNIT) == 1 and not any(subgroup_memberships(value).values())


def character_minorant(value):
    """A lower bound for the allowed-class indicator, extended by zero off G."""
    value = index(value) % DIFFERENCE_UNIT
    if gcd(value, DIFFERENCE_UNIT) != 1:
        return 0
    return 1 - sum(subgroup_memberships(value).values())


def spectral_constants():
    unit_count, _, _, _ = residue_counts()
    indices = tuple(SUBGROUP_INDICES.values())
    mean = 1 - sum((Fraction(1, size) for size in indices), Fraction(0))
    nonprincipal_mass = sum((Fraction(size - 1, size) for size in indices), Fraction(0))
    density = prod(Fraction(size - 1, size) for size in indices)
    selected_classes = unit_count * density
    if selected_classes.denominator != 1:
        raise ArithmeticError("nonintegral group count")
    return {
        "unit_residues": unit_count,
        "selected_classes": int(selected_classes),
        "selected_unit_fraction": density,
        "principal_coefficient": mean,
        "nonprincipal_coefficient_mass": nonprincipal_mass,
        "relative_error_factor": nonprincipal_mass / mean,
        "character_count": 1 + sum(size - 1 for size in indices),
        "distinct_real_correlations": 1 + (SUBGROUP_INDICES[2] - 1) + sum(
            (size - 1) // 2 for ell, size in SUBGROUP_INDICES.items() if ell != 2),
        "full_quotient_order": prod(indices),
    }


def necessary_occupied_cosets(quotient_order, amplification):
    """Necessary support for this uniform-amplitude gate; not a prime count.

    If e/T < 1/R is required, Parseval for a quotient of size N forces
    J > R^2*N/(N-1+R^2) occupied quotient classes. Success is not implied.
    """
    quotient_order = index(quotient_order)
    amplification = Fraction(amplification)
    if quotient_order < 2 or amplification < 1:
        raise ValueError("require quotient_order>=2 and amplification>=1")
    threshold = amplification**2 * quotient_order / (quotient_order - 1 + amplification**2)
    return threshold.numerator // threshold.denominator + 1


def certificate():
    constants = spectral_constants()
    result = {key: str(value) if isinstance(value, Fraction) else value
              for key, value in constants.items()}
    result.update({
        "status": "Error transfer proved; actual prime-correlation bounds and AP28 remain open.",
        "subgroup_indices": SUBGROUP_INDICES,
        "sufficient_numeric_condition": "E0 + 9*epsilon < V_M(X)*beta_L, for 27*M+2<=X<2^64",
        "actual_arithmetic_bounds_supplied": False,
        "absolute_amplitude_gate_necessary_quadratic_cosets": necessary_occupied_cosets(
            128, constants["relative_error_factor"]),
        "coverage": "Group identities only; no AP candidates or full character table enumerated.",
    })
    return result


if __name__ == "__main__":
    result = certificate()
    destination = Path(__file__).resolve().parents[1] / "results" / "character-minorant-checks.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
