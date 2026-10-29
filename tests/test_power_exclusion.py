from fractions import Fraction
from math import gcd, prod

import pytest
from sympy import factorint

from research.power_exclusion import (
    DIFFERENCE_UNIT, EXCEPTIONAL_POWER, EXCEPTIONAL_RESIDUE, POWER_TESTS,
    UINT64_MAX, UNIT_GROUPS, allowed_residue, certificate,
    certifies_non_power, passes_power_character_tests, residue_counts,
)


def test_exhibited_generators_prove_all_local_unit_groups_are_cyclic():
    assert 2 * prod(modulus for modulus, order, generator in UNIT_GROUPS) == DIFFERENCE_UNIT
    for modulus, order, generator in UNIT_GROUPS:
        assert gcd(generator, modulus) == 1
        assert pow(generator, order, modulus) == 1
        assert all(pow(generator, order // int(q), modulus) != 1 for q in factorint(order))


def test_local_power_images_agree_with_the_character_tests():
    # Small finite-group identity checks, not a progression discovery search.
    for ell, tests in POWER_TESTS.items():
        for modulus, exponent in tests:
            units = {r for r in range(modulus) if gcd(r, modulus) == 1}
            image = {pow(r, ell, modulus) for r in units}
            assert image == {r for r in units if pow(r, exponent, modulus) == 1}


def test_exact_retained_count_uses_primary_components_without_scanning_classes():
    total, indices, before, after = residue_counts()
    assert total == 255467520
    assert indices == {2: 256, 3: 27, 5: 5, 7: 7, 11: 11}
    assert Fraction(before, total) == Fraction(1105, 1848)
    assert before == 152755200 and after == 152755199
    assert Fraction(after, total) > Fraction(5979, 10000)


def test_lone_uncovered_prime_exponent_has_exactly_one_possible_base():
    assert 29**13 <= UINT64_MAX < 31**13
    assert [b for b in range(2, 31) if gcd(b, DIFFERENCE_UNIT) == 1] == [29]
    assert EXCEPTIONAL_POWER == 10260628712958602189
    assert EXCEPTIONAL_RESIDUE == 839436809
    assert passes_power_character_tests(EXCEPTIONAL_POWER)
    assert not allowed_residue(EXCEPTIONAL_POWER)


def test_covered_powers_fail_a_local_test_and_the_exception_is_removed():
    for ell in POWER_TESTS:
        for base in [29, 31, 37, 101, 1009]:
            value = base**ell
            if value <= UINT64_MAX:
                assert not certifies_non_power(value)
    assert not certifies_non_power(EXCEPTIONAL_POWER)


def test_prime_power_exclusion_cannot_be_mistaken_for_primality():
    report = certificate()
    composite = report["composite_counterexample"]["value"]
    left, right = report["composite_counterexample"]["factors"]
    assert composite == 19520626127 == left * right
    assert min(left, right) > 1 and certifies_non_power(composite)


def test_progression_preserves_the_class_but_no_primality_is_asserted():
    residue = DIFFERENCE_UNIT // 2 + 2
    assert residue == 780825047 and allowed_residue(residue)
    for j in [0, 1, 13, 27]:
        assert certifies_non_power(residue + j * DIFFERENCE_UNIT * 17)


def test_crt_counterfamily_works_even_when_the_first_cofactor_would_be_one():
    bound = 58 * DIFFERENCE_UNIT + 31
    assert bound == 90575705251 < UINT64_MAX
    for residue in [1, 31, DIFFERENCE_UNIT // 2 + 2, DIFFERENCE_UNIT - 1]:
        cofactor = residue * pow(31, -1, DIFFERENCE_UNIT) % DIFFERENCE_UNIT
        if cofactor == 1:
            cofactor += DIFFERENCE_UNIT
        start = 31 * cofactor
        assert 2 <= cofactor <= DIFFERENCE_UNIT + 1
        assert start % DIFFERENCE_UNIT == residue
        assert start + 27 * DIFFERENCE_UNIT <= bound


def test_certificate_refuses_unsupported_heights_and_fixed_classes_are_not_global():
    for value in [1, 0, -1, 2**64, 2**128]:
        with pytest.raises(ValueError):
            certifies_non_power(value)
    total, _, _, _ = residue_counts()
    residue = DIFFERENCE_UNIT // 2 + 2
    # Euler's theorem constructs a perfect power in the same class at a much
    # larger height; modular exponentiation avoids constructing that huge value.
    assert pow(residue, total + 1, DIFFERENCE_UNIT) == residue
    assert total + 1 > 64
