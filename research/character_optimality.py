"""Exact abstract dual certificates for the character minorant.

The dual measure is on residue classes. It is not an arithmetic distribution
of prime progressions and provides no missing prime-correlation estimate.
"""
from fractions import Fraction
from itertools import combinations
import json
from math import prod
from operator import index
from pathlib import Path

from research.character_minorant import SUBGROUP_INDICES, spectral_constants


def dual_data(indices):
    """Return a certified sharpness witness when this candidate dual is valid.

    Uniformly lift a mixture of configurations with exactly one zero quotient
    coordinate. All nontrivial Fourier profiles must pass the exact bound.
    This construction is not valid for every choice of quotient sizes.
    """
    indices = tuple(map(index, indices))
    if len(indices) < 2 or min(indices) < 2:
        raise ValueError("require at least two quotient sizes, each >=2")
    mean = 1 - sum((Fraction(1, n) for n in indices), Fraction(0))
    if mean <= 0:
        raise ValueError("the Bonferroni mean must be positive")
    mass = len(indices) - 1 + mean
    rho = mean / mass
    weights = tuple(Fraction(1, n) + rho * Fraction(n - 1, n) for n in indices)
    profiles = []
    for size in range(1, len(indices) + 1):
        for active in combinations(range(len(indices)), size):
            value = Fraction((-1)**size, prod(indices[j] - 1 for j in active)) * (
                1 - sum(weights[j] * indices[j] for j in active))
            profiles.append((active, value))
    if sum(weights) != 1 or min(weights) <= 0 or any(abs(v) > rho for _, v in profiles):
        raise ValueError("this dual does not certify the claimed optimum for these sizes")
    return dict(indices=indices, mean=mean, coefficient_mass=mass, rho=rho,
                weights=weights, profiles=tuple(profiles))


def certificate():
    indices = tuple(SUBGROUP_INDICES.values())
    data = dual_data(indices)
    primal = spectral_constants()
    assert 1 / data["rho"] == primal["relative_error_factor"]
    multi = [(abs(value), active, value) for active, value in data["profiles"] if len(active) > 1]
    maximum, active, signed_value = max(multi)
    return {
        "status": "Optimal modular error ratio proved; no finite arithmetic bound or AP28 witness.",
        "quotient_sizes": indices,
        "uniform_character_threshold": str(data["rho"]),
        "optimal_nonprincipal_to_principal_ratio": str(1 / data["rho"]),
        "dual_mixture_weights": [str(w) for w in data["weights"]],
        "nonprincipal_profile_types": len(data["profiles"]),
        "dual_mass_on_safe_residues": 0,
        "dual_is_actual_prime_progression_distribution": False,
        "largest_multicomponent_profile": {
            "active_coordinates": active,
            "value": str(signed_value),
            "absolute_value": str(maximum),
        },
        "all_profile_bounds_verified": True,
        "scope": "All pointwise minorants for the fixed five bad subgroups, with uniform absolute Fourier errors.",
        "actual_arithmetic_bounds_supplied": False,
        "direct_published_parameter_audit": {
            "N_range": "1<N<2^64",
            "Q_definition": "exp((log N)^(1/10))",
            "strict_Q_upper_bound": "121/16 < 8",
            "cutoff_needed_to_include_prime_23": "w>23",
            "w_above_23_inside_stated_2_to_Q_range": False,
            "scope": "This direct use of Theorem 1.4's parameter range only; not an impossibility result for other analytic methods.",
        },
    }


if __name__ == "__main__":
    result = certificate()
    destination = Path(__file__).resolve().parents[1] / "results" / "character-optimality-checks.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
