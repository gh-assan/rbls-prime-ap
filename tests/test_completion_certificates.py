from fractions import Fraction
from math import comb
import random

import pytest

from research.completion_certificates import (binomial_coefficients,finite_certificate,
    geometric_count,interval_lower_bound,lower_bound,model_certificate,paired_minorant)


@pytest.mark.parametrize('roots',[(),(2,),(3,7),(3,5,7),(1,1,4)])
def test_minorant_and_newton_expansion_on_integer_support(roots):
    coefficients=binomial_coefficients(roots)
    for c in range(101):
        expected=paired_minorant(c,roots)
        assert expected <= (1 if c==0 else 0)
        assert sum(b*comb(c,r) for r,b in enumerate(coefficients) if r<=c)==expected


def test_bounds_for_arbitrary_dependent_defect_distributions():
    rng=random.Random(281)
    for _ in range(30):
        histogram=[rng.randrange(100) for c in range(29)]
        moments=[sum(n*comb(c,r) for c,n in enumerate(histogram) if c>=r) for r in range(29)]
        roots=(3,7)
        assert lower_bound(moments,roots)<=histogram[0]
        errors=[Fraction(rng.randrange(10),3) for r in range(6)]
        estimates=[Fraction(m)+e/2 for m,e in zip(moments,errors)]
        assert interval_lower_bound(estimates,errors,roots)<=lower_bound(moments,roots)


def test_exact_model_certificate_and_nonarithmetic_label():
    report=model_certificate()
    assert report['paired_lower_bound']=='153/8000'
    assert report['degree_five_bonferroni']=='-2313/10000'
    assert 'not arithmetic' in report['label']


def test_semiprime_tail_matches_independent_arithmetic_oracle():
    report=finite_certificate()
    assert report['rough_candidates']==105
    assert report['binomial_moments']==[105,76,22,4,0,0]
    assert report['actual_prime_progressions']==47
    assert report['certified_lower_bound']=='47'


def test_geometric_floor_count_including_negative_basis_coefficients():
    rng=random.Random(284)
    for _ in range(100):
        F,I,c,A,W,X=(rng.randrange(1,15),rng.randrange(1,8),rng.randrange(-20,21),
                     rng.randrange(1,20),rng.randrange(1,10),rng.randrange(30,150))
        brute=sum(1 for a in range(A,X+1) for m in range(1,X+1)
                  if a+W*m<=X and m%I==0 and (a-c*m)%F==0)
        assert geometric_count(F,I,c,A,W,X)==brute


def test_invalid_certificate_inputs():
    with pytest.raises(ValueError):
        paired_minorant(1,[0])
    with pytest.raises(ValueError):
        lower_bound([1,2],(3,7))
    with pytest.raises(ValueError):
        interval_lower_bound([1]*6,[-1]*6,(3,7))
