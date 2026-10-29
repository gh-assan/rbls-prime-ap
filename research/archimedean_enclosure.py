"""Outward enclosures of a defined AP density-model integral.

This integrates a continuous function. It neither counts prime progressions
nor supplies a bound for the model's arithmetic discrepancy.
"""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
import heapq
import json
from operator import index
from pathlib import Path

from research.character_minorant import SUBGROUP_INDICES, spectral_constants
from research.character_optimality import dual_data
from research.euler_tail_bounds import certified_constants
from research.power_exclusion import DIFFERENCE_UNIT, UINT64_MAX


def twice_clipped_area(a0, a1, b0, b1, height):
    """Twice the exact area of a box intersected with a+b<=height."""
    return (max(height-a0-b0, 0)**2 - max(height-a1-b0, 0)**2
            - max(height-a0-b1, 0)**2 + max(height-a1-b1, 0)**2)


class LogKernel:
    def __init__(self, k, precision=28):
        self.k, self.precision = map(index, (k, precision))
        if self.k < 2 or self.precision < 16:
            raise ValueError("require k>=2 and precision>=16")
        self.logs = {}
        self.values = {}

    def log_integer(self, n):
        n = index(n)
        if n < 1:
            raise ValueError("logarithm input must be positive")
        if n not in self.logs:
            if n == 1:
                self.logs[n] = (Decimal(0), Decimal(0))
            else:
                with localcontext() as ctx:
                    ctx.prec = self.precision
                    # ln is correctly rounded to nearest; adjacent numbers
                    # enclose the exact logarithm independently of tie direction.
                    value = Decimal(n).ln()
                    self.logs[n] = (ctx.next_minus(value), ctx.next_plus(value))
        return self.logs[n]

    def log_ratio(self, numerator, denominator):
        lo_n, hi_n = self.log_integer(numerator)
        lo_d, hi_d = self.log_integer(denominator)
        with localcontext() as ctx:
            ctx.prec = self.precision
            ctx.rounding = ROUND_FLOOR
            lo = lo_n-hi_d
            ctx.rounding = ROUND_CEILING
            hi = hi_n-lo_d
        return lo, hi

    def bounds(self, a, b):
        """Enclose product_j 1/log(a+j*b/(k-1)), for a>=2,b>=0."""
        a, b = map(index, (a, b))
        if a < 2 or b < 0:
            raise ValueError("require a>=2 and b>=0")
        key = (a, b)
        if key not in self.values:
            logs = [self.log_ratio((self.k-1)*a+j*b, self.k-1)
                    for j in range(self.k)]
            with localcontext() as ctx:
                ctx.prec = self.precision
                ctx.rounding = ROUND_FLOOR
                denominator_lo = Decimal(1)
                for lo, _ in logs:
                    denominator_lo *= lo
                ctx.rounding = ROUND_CEILING
                denominator_hi = Decimal(1)
                for _, hi in logs:
                    denominator_hi *= hi
                upper = Decimal(1)/denominator_lo
                ctx.rounding = ROUND_FLOOR
                lower = Decimal(1)/denominator_hi
            self.values[key] = (lower, upper)
        return self.values[key]


def doubling_grid(start, end):
    result = [start]
    while result[-1] < end:
        result.append(min(end, 2*result[-1]))
    return result


def integral_enclosure(k, step, height, max_cells=8000, precision=28):
    """Enclose the continuous cone integral using monotone rectangle bounds."""
    k, step, height, max_cells = map(index, (k, step, height, max_cells))
    precision = index(precision)
    if k < 2 or step < 1 or height < 2 or max_cells < 1:
        raise ValueError("invalid cone or cell parameters")
    W = (k-1)*step
    kernel = LogKernel(k, precision)
    if height <= W+2:
        return dict(lower=Decimal(0), upper=Decimal(0), cells=0, area=Fraction(0), kernel=kernel)

    def cell_bounds(box):
        a0, a1, b0, b1 = box
        twice_area = twice_clipped_area(a0, a1, b0, b1, height)
        if twice_area == 0:
            return None
        if twice_area < 0:
            raise ArithmeticError("negative clipped area")
        f_lo, _ = kernel.bounds(a1, b1)
        _, f_hi = kernel.bounds(a0, b0)
        with localcontext() as ctx:
            ctx.prec = precision
            ctx.rounding = ROUND_FLOOR
            lower = Decimal(twice_area)*f_lo/Decimal(2*W)
            ctx.rounding = ROUND_CEILING
            upper = Decimal(twice_area)*f_hi/Decimal(2*W)
        return lower, upper

    heap = []
    serial = 0
    lower = upper = Decimal(0)

    def add(box):
        nonlocal serial, lower, upper
        values = cell_bounds(box)
        if values is None:
            return
        lo, hi = values
        with localcontext() as ctx:
            ctx.prec = precision
            ctx.rounding = ROUND_FLOOR
            lower += lo
            ctx.rounding = ROUND_CEILING
            upper += hi
        heapq.heappush(heap, (-(hi-lo), serial, box, lo, hi))
        serial += 1

    a_grid = doubling_grid(2, height-W)
    b_grid = doubling_grid(W, height-2)
    initial_boxes = [(a0, a1, b0, b1)
                     for a0, a1 in zip(a_grid, a_grid[1:])
                     for b0, b1 in zip(b_grid, b_grid[1:])
                     if twice_clipped_area(a0, a1, b0, b1, height) > 0]
    if len(initial_boxes) > max_cells:
        raise ValueError("max_cells is smaller than the initial dyadic partition")
    for box in initial_boxes:
        add(box)
    while len(heap)+3 <= max_cells:
        _, _, box, lo, hi = heapq.heappop(heap)
        a0, a1, b0, b1 = box
        if a1-a0 <= 1 and b1-b0 <= 1:
            heapq.heappush(heap, (-(hi-lo), serial, box, lo, hi))
            break
        with localcontext() as ctx:
            ctx.prec = precision
            ctx.rounding = ROUND_FLOOR
            lower -= lo
            ctx.rounding = ROUND_CEILING
            upper -= hi
        # Splitting choices affect efficiency only. Every child gets an
        # independently outward-rounded monotone bound.
        a_parts = [a0, (a0+a1)//2, a1] if a1-a0 > 1 else [a0, a1]
        b_parts = [b0, (b0+b1)//2, b1] if b1-b0 > 1 else [b0, b1]
        for x0, x1 in zip(a_parts, a_parts[1:]):
            for y0, y1 in zip(b_parts, b_parts[1:]):
                add((x0, x1, y0, y1))
    return dict(lower=lower, upper=upper, cells=len(heap),
                area=Fraction((height-W-2)**2, 2*W), kernel=kernel)


def one_sided_support_requirement(rank, strict_threshold):
    """Necessary occupied classes if every nonprincipal Walsh mean < threshold."""
    rank = index(rank)
    strict_threshold = Fraction(strict_threshold)
    if rank < 2 or not 0 <= strict_threshold < 1:
        raise ValueError("require rank>=2 and 0<=strict_threshold<1")
    bound = Fraction(2*(rank-1), 1)/(1+strict_threshold)
    return bound.numerator//bound.denominator+1


def model_certificate(max_cells=8000, precision=28):
    M, X = DIFFERENCE_UNIT, UINT64_MAX
    result = integral_enclosure(28, M, X, max_cells, precision)
    alpha = spectral_constants()["selected_unit_fraction"]
    beta_lo, beta_hi = certified_constants()["beta_infinite_interval"]
    # Products of finite Decimal values are exact rationals here, avoiding
    # another rounding layer in the final stored model intervals.
    raw_lo = Fraction(result["lower"])*beta_lo
    raw_hi = Fraction(result["upper"])*beta_hi
    kernel = result["kernel"]
    D = M//7
    strip_upper = Fraction(0)
    grid = doubling_grid(2, X)
    for a0, a1 in zip(grid, grid[1:]):
        strip_upper += 6*(a1-a0)*Fraction(kernel.bounds(a0, 27*D)[1])
    strip_upper *= beta_hi

    def display_interval(lo, hi):
        values = {}
        for key, value, rounding in [("lower", lo, ROUND_FLOOR), ("upper", hi, ROUND_CEILING)]:
            with localcontext() as ctx:
                ctx.prec = 18
                ctx.rounding = rounding
                values[key] = str(Decimal(value.numerator)/Decimal(value.denominator))
        return values

    rho = dual_data(tuple(SUBGROUP_INDICES.values()))["rho"]
    return {
        "status": "Rigorous enclosure of a defined density-model main term; not an actual prime count or success probability.",
        "height": X, "k": 28, "difference_unit": M,
        "precision": precision, "active_cells": result["cells"],
        "unselected_M_model": display_interval(raw_lo, raw_hi),
        "selected_M_model": display_interval(alpha*raw_lo, alpha*raw_hi),
        "unselected_D_model": display_interval(7*raw_lo, 7*raw_hi+strip_upper),
        "selected_to_D_model_ratio_upper": str(alpha/7),
        "strict_one_sided_character_threshold": str(rho),
        "necessary_quadratic_support": one_sided_support_requirement(7, rho),
        "support_refers_to": "Occupied quadratic classes of nonzero von Mangoldt tuples, which may include prime powers outside the selected set.",
        "finite_prime_count_error_bound_available": False,
        "AP28_witness_available": False,
        "beta_source": "research.euler_tail_bounds.certified_constants: P=100000, precision=60",
    }


if __name__ == "__main__":
    certificate = model_certificate()
    destination = Path(__file__).resolve().parents[1]/"results"/"archimedean-enclosure-checks.json"
    destination.write_text(json.dumps(certificate, indent=2)+"\n")
    print(json.dumps(certificate, indent=2))
