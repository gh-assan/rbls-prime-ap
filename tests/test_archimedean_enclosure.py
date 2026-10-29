from decimal import Decimal
from fractions import Fraction
from math import prod

import pytest

from research.archimedean_enclosure import (
    LogKernel, integral_enclosure, one_sided_support_requirement, twice_clipped_area,
)
from research.character_optimality import dual_data
from research.character_minorant import SUBGROUP_INDICES


def rational_log_interval(n, terms=64):
    """Independent atanh-series bounds, using exact rational arithmetic."""
    def series(z):
        lower = 2*sum((z**(2*j+1)/Fraction(2*j+1) for j in range(terms)), Fraction(0))
        tail = 2*z**(2*terms+1)/(Fraction(2*terms+1)*(1-z*z))
        return lower, lower+tail
    power = n.bit_length()-1
    z = Fraction(n-2**power, n+2**power)
    a, b = series(z)
    l2, u2 = series(Fraction(1, 3))
    return power*l2+a, power*u2+b


@pytest.mark.parametrize("n", [2, 27, 31, 2**64-1, 54*(2**64-1)])
def test_decimal_log_enclosures_against_independent_exact_series(n):
    lower, upper = LogKernel(28, 24).log_integer(n)
    exact_lower, exact_upper = rational_log_interval(n)
    assert Fraction(lower) <= exact_lower <= exact_upper <= Fraction(upper)


def test_integrand_outward_products_and_endpoint_monotonicity():
    kernel = LogKernel(3, 24)
    lo, hi = kernel.bounds(2, 54)
    logs = [kernel.log_ratio(4+j*54, 2) for j in range(3)]
    exact_lower = 1/prod(Fraction(right) for _, right in logs)
    exact_upper = 1/prod(Fraction(left) for left, _ in logs)
    assert Fraction(lo) <= exact_lower <= exact_upper <= Fraction(hi)
    larger_lo, larger_hi = kernel.bounds(4, 108)
    assert larger_hi < lo
    assert kernel.log_integer(1) == (Decimal(0), Decimal(0))


def test_clipped_area_and_partition_additivity_are_exact():
    assert [twice_clipped_area(0, 2, 0, 2, h) for h in range(1, 5)] == [1, 4, 7, 8]
    whole = twice_clipped_area(2, 100, 4, 100, 100)
    children = sum(twice_clipped_area(a0, a1, b0, b1, 100)
                   for a0, a1 in [(2, 40), (40, 100)]
                   for b0, b1 in [(4, 70), (70, 100)])
    assert whole == children == 94**2


def test_refinement_preserves_a_valid_nested_interval_and_cone_area():
    coarse = integral_enclosure(3, 2, 1000, max_cells=200, precision=24)
    fine = integral_enclosure(3, 2, 1000, max_cells=500, precision=24)
    assert coarse["lower"] <= fine["lower"] <= fine["upper"] <= coarse["upper"]
    assert fine["area"] == Fraction((1000-2-4)**2, 8)
    assert 0 < fine["cells"] <= 500
    empty = integral_enclosure(28, 1561650090, 100)
    assert empty["lower"] == empty["upper"] == empty["area"] == 0


def test_one_sided_support_bound_for_weighted_quadratic_quotients():
    rho = dual_data(tuple(SUBGROUP_INDICES.values()))["rho"]
    assert one_sided_support_requirement(7, rho) == 11
    points = [1, 2, 4, 8, 16, 32, 64, 3, 5, 9]
    for size in range(1, 11):
        weights = [Fraction(j+1, size*(size+1)//2) for j in range(size)]
        maximum = max(sum(w*(1 if bin(char & p).count('1') % 2 == 0 else -1)
                          for p, w in zip(points, weights)) for char in range(1, 128))
        assert maximum >= (1 if size < 6 else Fraction(12, size)-1)
        assert maximum >= rho
    assert one_sided_support_requirement(2, 0) == 3


def test_invalid_numeric_domains_are_rejected():
    with pytest.raises(ValueError):
        integral_enclosure(28, 1561650090, 2**64-1, max_cells=1)
    with pytest.raises(ValueError):
        LogKernel(1)
    with pytest.raises(ValueError):
        LogKernel(3).bounds(1, 2)
    with pytest.raises(ValueError):
        one_sided_support_requirement(1, Fraction(1, 10))
