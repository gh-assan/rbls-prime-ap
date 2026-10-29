"""Exact finite checks for the 2026 transference route assessment.

These checks count cubes and a digit-defined AP-free set. They neither scan
prime progression candidates nor supply an AP-28 arithmetic lower bound.
"""
from fractions import Fraction
import json
from math import comb, factorial, prod
from operator import index
from pathlib import Path


def interval_cube_count(length, order):
    """Number of integer order-cubes wholly contained in [1, length]."""
    length, order = map(index, (length, order))
    if length < 1 or order < 1:
        raise ValueError("require length >= 1 and order >= 1")
    return sum(2**j * comb(order, j) * comb(length, j + 1)
               for j in range(min(order, length - 1) + 1))


def interval_sup_lower_factor(length, order):
    """Rational lower bound in ||h||_U^order[length] >= c ||h||_inf.

    Only orders >=2 admit this comparison for arbitrary complex h. The
    exact factor is cube_count**(-1/2**order). This routine weakens it with
    exp(-t) >= 1-t and log(cube_count) < cube_count.bit_length().
    """
    length, order = map(index, (length, order))
    if length < 1 or order < 2:
        raise ValueError("require length >= 1 and order >= 2")
    cubes = interval_cube_count(length, order)
    return max(Fraction(0), 1 - Fraction(cubes.bit_length(), 2**order))


def ap28_free_digit_count(limit):
    """Count positive n<=limit with base-29 digits in {0,...,26}.

    There are at most log_29(limit)+1 iterations. The count is a digit-prefix
    calculation, without generating the set or enumerating progressions.
    """
    limit = index(limit)
    if limit < 0:
        raise ValueError("require a nonnegative limit")
    digits = []
    value = limit
    while value:
        digits.append(value % 29)
        value //= 29
    count = 0
    for pos in range(len(digits) - 1, -1, -1):
        digit = digits[pos]
        count += min(digit, 27) * 27**pos
        if digit >= 27:
            break
    else:
        count += 1
    return count - 1  # remove zero, including when limit == 0


def _family_report(height, difference_unit, phi, log_lower, prime_weight_lower):
    length = height // difference_unit - 1
    order = 56
    cubes = interval_cube_count(length, order)
    factor = interval_sup_lower_factor(length, order)
    # By Brun--Titchmarsh, for every unit class b modulo D this bounds the
    # fraction of n in [1,length] for which D*n+b is prime.
    prime_fraction_upper = Fraction(2 * height, log_lower * phi * length)

    # ||nu-1||_U56 < 1 implies ||nu-1||_inf < 101/100, so nu<201/100.
    assert factor > Fraction(100, 101)
    majorant_cap = Fraction(201, 100)
    assert prime_weight_lower > majorant_cap

    # If 0<=f<=nu is prime-supported and |mean(g-f)|<=1/100, then
    # h=g/2 has mean at most this bound. It is below the density of an
    # explicit AP-28-free set, so density alone cannot guarantee an AP.
    mean_error = Fraction(1, 100)
    dense_mean_upper = (majorant_cap * prime_fraction_upper + mean_error) / 2
    free_count = ap28_free_digit_count(length)
    free_density = Fraction(free_count, length)
    assert dense_mean_upper < free_density

    return {
        "difference_unit": difference_unit,
        "phi_difference_unit": phi,
        "common_interval_length": length,
        "gowers_order": order,
        "integer_cube_count_bits": cubes.bit_length(),
        "interval_norm_to_sup_lower_factor": str(factor),
        "majorant_norm_hypothesis": "||nu-1||_U56[N] < 1",
        "majorant_strict_pointwise_upper_bound": str(majorant_cap),
        "normalized_unscaled_prime_weight_peak_strict_lower_bound": str(prime_weight_lower),
        "stated_prime_weight_peak_compatible_with_majorant": False,
        "brun_titchmarsh_prime_fraction_upper": str(prime_fraction_upper),
        "assumed_dense_model_absolute_mean_error": str(mean_error),
        "half_dense_model_mean_upper": str(dense_mean_upper),
        "ap28_free_digit_set_count": free_count,
        "ap28_free_digit_set_density": str(free_density),
    }


def certificate():
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    difference_unit = prod(primes)
    phi = prod(p - 1 for p in primes)
    height = 2**64 - 1

    # e < sum_{j=0}^5 1/j! + (1/6!)/(1-1/7). Subsequent factorial
    # ratios are <=1/7, and some are strictly smaller.
    e_upper = sum((Fraction(1, factorial(j)) for j in range(6)), Fraction(0))
    e_upper += Fraction(7, 6 * factorial(6))
    assert e_upper == Fraction(11743, 4320)
    assert e_upper**25 < Fraction(height, difference_unit)
    assert e_upper**44 < height
    assert e_upper**16 < difference_unit
    assert e_upper**9 < 11**4  # log(11) > 9/4

    desired = _family_report(height, difference_unit, phi, 25,
                             Fraction(16 * phi, difference_unit))
    desired["unscaled_weight_obstruction_scope"] = (
        "Every nonzero prime weight on [1,N] exceeds 16*phi(D)/D.")
    assert Fraction(desired["brun_titchmarsh_prime_fraction_upper"]) < Fraction(49, 100)
    assert Fraction(desired["half_dense_model_mean_upper"]) < Fraction(1, 2)
    assert Fraction(desired["ap28_free_digit_set_density"]) > Fraction(3, 5)

    published = _family_report(height, 1, 1, 44, Fraction(9, 4))
    published["unscaled_weight_obstruction_scope"] = (
        "The full prime weight at n=10 is log(11)>9/4.")
    assert Fraction(published["half_dense_model_mean_upper"]) < Fraction(51, 1000)
    assert Fraction(published["ap28_free_digit_set_density"]) > Fraction(2, 5)

    return {
        "status": "Finite route obstruction checked; AP-28 construction remains open.",
        "height": height,
        "desired_primorial_interval": desired,
        "published_theorem_6_2_W_at_this_height": 1,
        "published_W1_interval": published,
        "scope": "The direct small-U56 majorant and density-only route on the two stated common intervals; not all transference arguments or heights.",
        "actual_ap28_arithmetic_lower_bound_supplied": False,
        "ap28_witness_supplied": False,
    }


if __name__ == "__main__":
    report = certificate()
    target = Path(__file__).resolve().parents[1] / "results" / "transference-audit-checks.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
