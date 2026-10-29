from fractions import Fraction
from math import factorial, isqrt

import pytest
from sympy import GF, Matrix, primerange
from sympy.polys.matrices import DomainMatrix

from research.analytic_ap28_certificates import (
    analytic_geometry,
    finite_difference_coefficients,
    gowers_sup_lower_factor,
)


def test_ap28_polynomial_phase_relation_and_exact_rank_transition():
    coefficients = finite_difference_coefficients(27)
    assert all(sum(c * j ** r for j, c in enumerate(coefficients)) == 0
               for r in range(27))
    assert sum(c * j ** 27 for j, c in enumerate(coefficients)) == -factorial(27)
    # Independent exact linear algebra over a field of valid characteristic
    # checks the nullity transition without expensive rational elimination.
    degree_26 = Matrix([[j ** r for j in range(28)] for r in range(27)])
    degree_27 = Matrix([[j ** r for j in range(28)] for r in range(28)])
    field_26 = DomainMatrix.from_Matrix(degree_26).convert_to(GF(101))
    field_27 = DomainMatrix.from_Matrix(degree_27).convert_to(GF(101))
    assert field_26.rank() == 27
    assert field_27.rank() == 28
    assert int(field_27.det()) % 101 == prod_factorials(27) % 101


def prod_factorials(last):
    value = 1
    for j in range(1, last + 1):
        value *= factorial(j)
    return value


def test_finite_group_obstruction_precludes_a_crude_sparse_model_certificate():
    factor = gowers_sup_lower_factor(27, 66)
    assert factor == Fraction(16776985, 16777216)
    assert factor > Fraction(49999, 50000)
    # Success of L-28*epsilon>0, with L<=1, forces this pointwise accuracy.
    assert 1 / (28 * factor) < Fraction(9, 250) < Fraction(1, 2)
    # For a nonconstant indicator of density at most 1/2, even the improved
    # constant-model telescoping bound cannot certify positivity.
    assert factor / 2 > Fraction(1, 2) ** 28


def exact_real_gowers_power(values, order):
    """Independent small-group evaluation of the defining recursive identity."""
    if order == 1:
        return (sum(values) / len(values)) ** 2
    size = len(values)
    return sum(exact_real_gowers_power(
        tuple(values[x] * values[(x+h) % size] for x in range(size)), order-1)
        for h in range(size)) / size


@pytest.mark.parametrize("order", [2, 3, 4])
def test_norm_sup_comparison_from_exact_norm_values_and_its_sharp_case(order):
    for entries in [(1, 0, 0, 0, 0), (1, -2, 3, 0, 1), (-1, 1, -1)]:
        values = tuple(map(Fraction, entries))
        power = exact_real_gowers_power(values, order)
        lower = Fraction(max(map(abs, values)) ** (2**order), len(values)**(order+1))
        assert power >= lower
        if entries == (1, 0, 0, 0, 0):
            assert power == lower


@pytest.mark.parametrize("k,D,X", [(3, 2, 80), (5, 30, 5000), (28, 223092870, 2**64-1)])
def test_prime_power_overcount_uses_all_exponents_with_exact_bounds(k, D, X):
    report = analytic_geometry(k, D, X)
    W = (k - 1) * D
    assert report["continuous_cone_area"] == Fraction(max(0, X - 2 - W)**2, 2*W)
    assert report["multiplier_cap"] == (X - 2) // W
    assert report["proper_prime_power_value_bound"] == (X.bit_length()-2)*isqrt(X)
    if X < 10000:
        powers = set()
        for p in primerange(2, isqrt(X) + 1):
            n = int(p)**2
            while n <= X:
                powers.add(n)
                n *= int(p)
        assert len(powers) <= report["proper_prime_power_value_bound"]


def test_empty_cone_and_invalid_mathematical_inputs():
    report = analytic_geometry(28, 223092870, 100)
    assert report["continuous_cone_area"] == 0
    assert report["proper_power_tuple_bound"] == 0
    for args in [(1, 1), (2, 0), (0, 66)]:
        with pytest.raises(ValueError):
            gowers_sup_lower_factor(*args)
    with pytest.raises(ValueError):
        finite_difference_coefficients(0)
    with pytest.raises(ValueError):
        analytic_geometry(1, 1, 100)
