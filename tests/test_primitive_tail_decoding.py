from math import gcd
import random

import pytest
from sympy import nextprime,primerange

from research.primitive_tail_decoding import decode_primitive_box,decode_tail_intersection,rational_convergents


def test_box_decoder_against_all_small_primitive_fractions():
    for A in range(1,7):
        for M in range(1,7):
            modulus=int(nextprime(2*A*M))
            expected={}
            for a in range(1,A+1):
                for m in range(1,M+1):
                    if gcd(a,m)==1:
                        residue=a*pow(m,-1,modulus)%modulus
                        assert residue not in expected
                        expected[residue]=(a,m)
            for residue in range(modulus):
                assert decode_primitive_box(residue,modulus,A,M)==expected.get(residue)


def test_box_decoder_handles_nonprime_moduli_and_asymmetric_large_bounds():
    rng=random.Random(2911)
    for _ in range(200):
        A,M=10**18,rng.randrange(1,10**8)
        modulus=2*A*M+rng.randrange(1,10**10)
        while True:
            a=rng.randrange(1,A+1);m=rng.randrange(1,M+1)
            if gcd(a,m)==1 and gcd(m,modulus)==1:
                break
        residue=a*pow(m,-1,modulus)%modulus
        assert decode_primitive_box(residue,modulus,A,M)==(a,m)


def test_actual_rough_ap7_intersection_decodes_and_filters_exactly():
    tags=[(0,41),(1,73),(2,67),(3,101),(4,79)]
    point=decode_tail_intersection(7,210,30,20000,tags,sieve_bound=29,m_cap=10)
    assert point==(9143,2)
    a,m=point
    assert all((a+j*210*m)%q==0 and q*q<=a+j*210*m for j,q in tags)
    assert all((a+j*210*m)%p for p in primerange(2,30) for j in range(7))
    assert decode_tail_intersection(7,210,30,20000,tags,sieve_bound=29,m_cap=1) is None
    assert decode_tail_intersection(7,210,30,20000,tags,sieve_bound=29,base_cell=(2,1,0)) is None


def test_invalid_or_incomplete_size_regimes_are_not_reported_as_empty():
    with pytest.raises(ValueError,match='modulus'):
        decode_primitive_box(7,100,10,10)
    with pytest.raises(ValueError):
        decode_tail_intersection(7,210,30,20000,[(0,41),(0,73)])
    with pytest.raises(ValueError):
        decode_tail_intersection(7,210,30,20000,[(0,41),(1,41)])
    with pytest.raises(ValueError):
        decode_tail_intersection(7,210,30,20000,[(0,7)])
    with pytest.raises(ValueError):
        decode_tail_intersection(7,210,30,20000,[(0,41)],sieve_bound=37)


def test_universal_ap28_five_label_reconstruction_threshold_is_exact():
    X=2**64-1;W=27*223092870;cube_upper=2642246
    assert cube_upper**3>X
    assert W>2*cube_upper
    # Thus W>2*X^(1/3), so B^5>X^(5/3)>2*X^2/W
    # whenever B^3>X. The implementation checks the exact integer instance.
    B=cube_upper
    qs=[];q=B
    for _ in range(5):
        q=int(nextprime(q));qs.append(q)
    from math import prod
    m_max=(X-B-1)//W
    assert prod(qs)>2*(X-W)*m_max
    result=decode_tail_intersection(28,223092870,B+1,X,list(enumerate(qs)),sieve_bound=None)
    assert result is None or (result[0]>=B+1 and result[0]+W*result[1]<=X)


def test_all_nonempty_fifth_intersections_in_real_small_family():
    from research.run_tail_decoding_checks import certificate
    report=certificate()
    assert report['fifth_order_intersections']==66
    assert report['distinct_points']==26
    assert report['defect_histogram']==[78,230,320,225,81,21,4,1]


def test_primitivity_is_essential_to_the_uniqueness_statement():
    modulus=211
    points=[(5*i,i) for i in range(1,5)]
    assert all((a-5*m)%modulus==0 for a,m in points)
    assert decode_primitive_box(5,modulus,20,4)==(5,1)
    assert len(points)==4  # geometric points need not be unique
