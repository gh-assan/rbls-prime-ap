"""Exact constants for the analytic AP-28 note.

These routines verify algebra and finite inequalities. They do not enumerate
candidate progressions, evaluate prime correlations, or find an AP-28.
"""
from fractions import Fraction
from math import comb, isqrt
from operator import index


def finite_difference_coefficients(order):
    """Coefficients annihilating polynomials of degree below ``order``."""
    order = index(order)
    if order < 1:
        raise ValueError("require order >= 1")
    return tuple((-1) ** j * comb(order, j) for j in range(order + 1))


def gowers_sup_lower_factor(order, group_bits):
    """Rational c with ||f||_U^order >= c ||f||_inf when |G|<=2^bits.

    This weakens |G|^(-(order+1)/2^order) using exp(-t)>=1-t
    and log(2)<1. It is a lower bound, not a norm computation.
    """
    order, group_bits = map(index, (order, group_bits))
    if order < 2 or group_bits < 1:
        raise ValueError("require order >= 2 and group_bits >= 1")
    return max(Fraction(0), 1 - Fraction(group_bits * (order + 1), 2 ** order))


def analytic_geometry(k, difference_unit, height):
    """Cone area and a rigorous proper-prime-power tuple overcount.

    For a>=2, m>=1, a+(k-1)*D*m<=X, every tuple with a proper
    prime power in at least one position lies in this overcount. Multiplying
    it by log(X)^k bounds its von Mangoldt weight. No primality calls enter.
    """
    k, difference_unit, height = map(index, (k, difference_unit, height))
    if k < 2 or difference_unit < 1 or height < 2:
        raise ValueError("require k>=2, D>=1 and X>=2")
    span_unit = (k - 1) * difference_unit
    m_max = (height - 2) // span_unit
    slack = max(0, height - 2 - span_unit)
    volume = Fraction(slack * slack, 2 * span_unit)
    exponent_count = max(0, height.bit_length() - 2)
    proper_power_bound = exponent_count * isqrt(height)
    return {
        "span_unit": span_unit,
        "multiplier_cap": m_max,
        "continuous_cone_area": volume,
        "proper_prime_power_value_bound": proper_power_bound,
        "proper_power_tuple_bound": k * m_max * proper_power_bound,
    }
