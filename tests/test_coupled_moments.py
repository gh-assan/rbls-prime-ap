from fractions import Fraction
from math import comb

import pytest

from research.completion_certificates import model_moments
from research.coupled_moments import arithmetic_seven,sharp_paired_certificate,zero_mass_binomial


def test_zero_mass_law_matches_all_mixed_joint_probabilities_through_five():
    k,p,order=28,Fraction(2,5),5
    weights=zero_mass_binomial(k,p,order)
    assert min(weights)>=0 and weights[0]==0 and sum(weights)==1
    # Conditional on C=c, choose the c defect positions uniformly. For a fixed
    # pattern with s ones and r-s zeros, this is its exact probability.
    for r in range(1,order+1):
        for s in range(r+1):
            actual=sum(w*Fraction(comb(k-r,c-s),comb(k,c))
                       for c,w in enumerate(weights) if 0<=c-s<=k-r)
            assert actual==p**s*(1-p)**(r-s)


@pytest.mark.parametrize('k,order',[(6,2),(10,3),(28,5)])
def test_zero_mass_nonnegativity_at_proved_threshold(k,order):
    n=order+1
    weights=zero_mass_binomial(k,Fraction(n,k+n),order)
    assert weights[0]==0 and min(weights)>=0


def test_primal_dual_pair_proves_model_bound_is_sharp():
    moments=model_moments(28,Fraction(1,10))
    report=sharp_paired_certificate(28,moments,(3,6))
    assert report['sharp_lower_bound']=='9/400'
    support=report['support'];weights=list(map(Fraction,report['weights']))
    for r in range(6):
        assert sum(w*comb(c,r) for c,w in zip(support,weights) if c>=r)==moments[r]
    assert min(weights)>=0
    assert Fraction(report['sharp_lower_bound'])>Fraction(153,8000)


def test_arithmetic_seven_is_a_nontrivial_signed_certificate():
    report=arithmetic_seven()
    assert report['histogram']==[78,230,320,225,81,21,4,1]
    assert report['binomial_moments']==[960,2005,1772,874,281,66,11,1]
    assert report['certificate']['sharp_lower_bound']=='1069/15'
    assert report['actual_prime_progressions']==78
    assert report['binomial_moments'][0]-report['binomial_moments'][1]<0


def test_invalid_or_unproved_certificates_are_rejected():
    with pytest.raises(ValueError):
        zero_mass_binomial(28,Fraction(1,10),5)
    with pytest.raises(ValueError):
        sharp_paired_certificate(28,model_moments(28,Fraction(2,5)),(3,6))
    with pytest.raises(ValueError):
        sharp_paired_certificate(28,[1,2],(3,6))


def test_multiplier_cap_is_needed_for_automatic_primitivity():
    from math import gcd
    from sympy import primerange
    # Without m<=B, all three terms can be B-rough yet share a large factor.
    B,a,D,m=7,121,6,11
    terms=[a+j*D*m for j in range(3)]
    assert all(n%p for n in terms for p in primerange(2,B+1))
    assert gcd(a,D*m)==11
    # With the cap, rough a and a B-smooth D force the asserted gcd condition.
    for a in range(B+1,200):
        if all(a%p for p in primerange(2,B+1)):
            assert all(gcd(a,D*m)==1 for m in range(1,B+1))


def test_integer_sparse_bound_covers_the_uint64_domain():
    from fractions import Fraction
    W=27*223092870
    assert 2642246**3>2**64-1
    assert Fraction(2642246,2*W)<Fraction(11,50000)
