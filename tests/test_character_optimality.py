from fractions import Fraction
from itertools import combinations
from math import factorial, prod

import numpy as np
import pytest

from research.character_minorant import SUBGROUP_INDICES, spectral_constants
from research.character_optimality import certificate, dual_data


def test_fixed_primal_and_dual_certificates_match_exactly():
    data = dual_data(tuple(SUBGROUP_INDICES.values()))
    assert data["rho"] == Fraction(693733, 6015973)
    assert data["weights"] == tuple(Fraction(n, 6015973) for n in
                                    [735313, 890853, 1758181, 1454053, 1177573])
    assert min(data["weights"]) > 0 and sum(data["weights"]) == 1
    assert 1/data["rho"] == spectral_constants()["relative_error_factor"]
    assert data["mean"] - data["rho"]*data["coefficient_mass"] == 0


def test_all_fourier_profiles_and_analytic_sufficient_inequality():
    data = dual_data(tuple(SUBGROUP_INDICES.values()))
    assert len(data["profiles"]) == 31
    assert data["rho"] > Fraction(1, 14)
    for active, value in data["profiles"]:
        assert abs(value) <= data["rho"]
        if len(active) == 1:
            assert value == data["rho"]
    values = [n-1 for n in data["indices"]]
    for size in range(2, len(values)+1):
        for subset in combinations(values, size):
            assert prod(subset) - sum(subset) >= 14*(size-1)


def test_independent_direct_fourier_transform_of_a_small_dual_measure():
    data = dual_data((5, 7))
    measure = np.zeros((5, 7))
    measure[0, 1:] = float(data["weights"][0])/6
    measure[1:, 0] = float(data["weights"][1])/4
    assert np.isclose(measure.sum(), 1)
    assert np.all(measure[1:, 1:] == 0) and measure[0, 0] == 0
    transform = np.fft.fftn(measure)
    profiles = dict(data["profiles"])
    for i in range(5):
        for j in range(7):
            if i == j == 0:
                expected = 1
            else:
                active = tuple(k for k, nonzero in enumerate((i != 0, j != 0)) if nonzero)
                expected = float(profiles[active])
            assert abs(transform[i, j] - expected) < 1e-12
    assert np.max(np.abs(transform.ravel()[1:])) <= float(data["rho"]) + 1e-12


def test_the_candidate_dual_is_not_silently_generalized_to_invalid_sizes():
    # For these smaller sizes, a mixed Fourier coefficient exceeds rho.
    # They must not receive the fixed-family optimality claim.
    with pytest.raises(ValueError):
        dual_data((4, 3))
    for sizes in [(), (5,), (1, 5), (2, 2)]:
        with pytest.raises(ValueError):
            dual_data(sizes)


def test_exact_elementary_parameter_bound_for_the_published_Q_range():
    # e's tail after 1/5! is bounded by a geometric series starting at 1/6!.
    e_upper = sum((Fraction(1, factorial(j)) for j in range(6)), Fraction(0)) + Fraction(7, 4320)
    assert e_upper == Fraction(11743, 4320) < Fraction(11, 4)
    assert Fraction(121, 16) < 8 < 23
    assert 64 < 2**10
    report = certificate()
    assert report["actual_arithmetic_bounds_supplied"] is False
    assert report["dual_is_actual_prime_progression_distribution"] is False
    assert report["direct_published_parameter_audit"]["w_above_23_inside_stated_2_to_Q_range"] is False
