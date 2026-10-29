from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from research.character_minorant import (
    allowed_character_residue, certificate, character_minorant, is_square_unit,
    necessary_occupied_cosets, spectral_constants, subgroup_memberships,
)
from research.power_exclusion import (
    DIFFERENCE_UNIT, EXCEPTIONAL_RESIDUE, allowed_residue,
)


def test_exception_is_absorbed_by_a_subgroup_and_selected_classes_are_safe():
    assert not is_square_unit(EXCEPTIONAL_RESIDUE)
    assert subgroup_memberships(EXCEPTIONAL_RESIDUE)[2]
    assert not allowed_character_residue(EXCEPTIONAL_RESIDUE)
    residue = DIFFERENCE_UNIT // 2 + 2
    assert allowed_character_residue(residue) and allowed_residue(residue)
    for value in [1, 29, 31, residue, EXCEPTIONAL_RESIDUE]:
        for square in [1, 29**2, 31**2]:
            assert subgroup_memberships(square)[2]
            assert subgroup_memberships(EXCEPTIONAL_RESIDUE * square)[2]
        assert character_minorant(value) <= int(allowed_character_residue(value))
        if allowed_character_residue(value):
            assert allowed_residue(value)
    assert character_minorant(1) == -4
    assert character_minorant(residue) == 1
    assert character_minorant(2) == 0


def test_exact_character_budget_and_retained_count():
    result = spectral_constants()
    assert result["selected_classes"] == 152156160
    assert result["selected_unit_fraction"] == Fraction(1651, 2772)
    assert result["principal_coefficient"] == Fraction(693733, 1330560) > Fraction(1, 2)
    assert result["nonprincipal_coefficient_mass"] == Fraction(6015973, 1330560)
    assert result["relative_error_factor"] == Fraction(6015973, 693733) < 9
    assert result["character_count"] == 174
    assert result["distinct_real_correlations"] == 151
    assert result["full_quotient_order"] == 1330560
    assert certificate()["actual_arithmetic_bounds_supplied"] is False


def test_quadratic_exception_pattern_has_one_dimension_and_index_128():
    # Independent calculation in the small quotient (F_2)^8, not in the
    # 255-million-element unit group or the progression domain.
    primes = [3, 5, 7, 11, 13, 17, 19, 23]
    pattern = tuple(int(pow(EXCEPTIONAL_RESIDUE, (p-1)//2, p) != 1) for p in primes)
    assert pattern == (1, 0, 0, 1, 0, 1, 1, 0)
    annihilator = [bits for bits in product(range(2), repeat=8)
                   if sum(b*v for b, v in zip(bits, pattern)) % 2 == 0]
    assert len(annihilator) == 128


def test_minorant_transform_on_an_independent_small_finite_group():
    # G=C_2 x C_2 x C_3. Remove the subgroup span((1,0)) in the first
    # component and the identity in C_3; the minorant has 2+3-1=4 characters.
    points = list(product(range(2), range(2), range(3)))
    coefficients = []
    for char in points:
        values = []
        for x in points:
            score = 1 - int(x[1] == 0) - int(x[2] == 0)
            phase = char[0]*x[0]/2 + char[1]*x[1]/2 + char[2]*x[2]/3
            values.append(score*np.exp(-2j*np.pi*phase))
        coefficients.append(sum(values)/len(points))
    assert abs(coefficients[0] - Fraction(1, 6)) < 1e-12
    assert sum(abs(c) > 1e-12 for c in coefficients) == 4
    assert abs(sum(abs(c) for c in coefficients[1:]) - Fraction(7, 6)) < 1e-12


def test_uniform_gate_cannot_localize_a_single_occupied_coset():
    ratio = spectral_constants()["relative_error_factor"]
    assert necessary_occupied_cosets(128, ratio) == 48
    # A point mass has every character amplitude T. The uniform-amplitude
    # gate is negative, even though its signed minorant can equal T.
    b = spectral_constants()["principal_coefficient"]
    coefficient_mass = spectral_constants()["nonprincipal_coefficient_mass"]
    assert b - coefficient_mass == -4
    weights = np.zeros(128)
    weights[17] = 3
    transform = np.fft.fft(weights)
    assert np.allclose(np.abs(transform), 3)
    assert np.isclose(sum(abs(transform[1:])**2), (128-1)*9)


def test_signed_aggregate_retains_information_lost_in_absolute_bounds():
    sizes = [128, 27, 5, 7, 11]
    b = spectral_constants()["principal_coefficient"]
    # At a safe quotient point, subgroup orthogonality gives sum of the
    # nonprincipal characters equal to -1 in every family.
    signed_twist = -sum((Fraction(1, size) for size in sizes), Fraction(0))
    assert b - signed_twist == 1


def test_unsupported_group_inputs_are_rejected():
    with pytest.raises(ValueError):
        subgroup_memberships(7)
    with pytest.raises(ValueError):
        necessary_occupied_cosets(1, 9)
    with pytest.raises(ValueError):
        necessary_occupied_cosets(128, Fraction(1, 2))
