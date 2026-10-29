from fractions import Fraction
from itertools import product

import pytest

from research.transference_audit import (
    ap28_free_digit_count,
    certificate,
    interval_cube_count,
    interval_sup_lower_factor,
)


def direct_cube_sum(values, order):
    """Independent defining sum on small integer intervals, with signed h."""
    length = len(values)
    total = 0
    for steps in product(range(1 - length, length), repeat=order):
        offsets = [(sum(step for step, bit in zip(steps, mask) if bit), sum(mask) % 2)
                   for mask in product((0, 1), repeat=order)]
        for base in range(length):
            if all(0 <= base + offset < length for offset, _ in offsets):
                term = 1
                for offset, conjugate in offsets:
                    value = values[base + offset]
                    term *= value.conjugate() if conjugate else value
                total += term
    return total


@pytest.mark.parametrize("length,order", [(1, 3), (3, 1), (3, 2), (4, 3)])
def test_exact_interval_cube_count_against_defining_cubes(length, order):
    assert interval_cube_count(length, order) == direct_cube_sum((1,) * length, order)


@pytest.mark.parametrize("order", [2, 3])
def test_interval_pointwise_comparison_and_sharp_point_mass(order):
    for values in [(0, 3, 0), (1, -2, 3), (-2, 1, -1)]:
        unnormalized = direct_cube_sum(values, order)
        assert unnormalized >= max(map(abs, values)) ** (2**order)
        if values == (0, 3, 0):
            assert unnormalized == 3 ** (2**order)
        cubes = interval_cube_count(len(values), order)
        factor = interval_sup_lower_factor(len(values), order)
        assert factor ** (2**order) <= Fraction(1, cubes)


@pytest.mark.parametrize("order", [2, 3])
def test_interval_comparison_includes_complex_phases(order):
    for values in [(1+1j, 2-1j, -1j), (0, 3j, 0)]:
        total = direct_cube_sum(values, order)
        assert total.imag == 0
        maximum_square = max(z.real**2 + z.imag**2 for z in values)
        assert total.real >= maximum_square ** (2**(order-1))
        if values == (0, 3j, 0):
            assert total.real == 3 ** (2**order)


def digit_allowed(value):
    while value:
        value, digit = divmod(value, 29)
        if digit >= 27:
            return False
    return True


def test_digit_count_boundary_prefixes_against_independent_membership():
    count = 0
    for limit in range(2500):
        if limit and digit_allowed(limit):
            count += 1
        assert ap28_free_digit_count(limit) == count
    for exponent in (1, 2, 3, 8):
        assert ap28_free_digit_count(29**exponent - 1) == 27**exponent - 1
        assert ap28_free_digit_count(29**exponent) == 27**exponent


def test_finite_field_step_in_ap_free_digit_proof():
    # All nonzero steps give 28 distinct residues mod 29, too many to fit
    # into the 27 allowed digits. This checks the induction's base step.
    for start in range(29):
        for step in range(1, 29):
            residues = {(start + j*step) % 29 for j in range(28)}
            assert len(residues) == 28
            assert not residues <= set(range(27))


def test_finite_certificate_separates_obstruction_from_arithmetic_solution():
    report = certificate()
    desired = report["desired_primorial_interval"]
    assert desired["common_interval_length"] == 82686390082
    assert desired["integer_cube_count_bits"] == 1869
    assert desired["ap28_free_digit_set_count"] == 50756571120
    assert Fraction(desired["ap28_free_digit_set_density"]) > Fraction(3, 5)
    assert Fraction(desired["half_dense_model_mean_upper"]) < Fraction(1, 2)
    published = report["published_W1_interval"]
    assert published["integer_cube_count_bits"] == 3450
    assert published["ap28_free_digit_set_count"] == 7526968007116178141
    assert Fraction(published["half_dense_model_mean_upper"]) < Fraction(51, 1000)
    assert Fraction(published["ap28_free_digit_set_density"]) > Fraction(2, 5)
    for family in (desired, published):
        assert not family["stated_prime_weight_peak_compatible_with_majorant"]
    assert not report["actual_ap28_arithmetic_lower_bound_supplied"]
    assert not report["ap28_witness_supplied"]


def test_invalid_norm_and_digit_domains_are_rejected():
    for args in [(0, 2), (3, 0)]:
        with pytest.raises(ValueError):
            interval_cube_count(*args)
    with pytest.raises(ValueError):
        interval_sup_lower_factor(4, 1)
    with pytest.raises(ValueError):
        ap28_free_digit_count(-1)
