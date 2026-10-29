from math import gcd
import random

import pytest

from research.completion_certificates import geometric_count
from research.lattice_floor_counts import augment_cell,count_cell,floor_sum


def test_signed_floor_sum_against_exhaustive_arithmetic():
    rng=random.Random(2841)
    for _ in range(2000):
        n=rng.randrange(60);m=rng.randrange(1,80)
        a=rng.randrange(-200,201);b=rng.randrange(-200,201)
        assert floor_sum(n,m,a,b)==sum((a*i+b)//m for i in range(n))


def test_large_triangle_uses_exact_integer_arithmetic():
    X,A,W=2**64-1,29,27*223092870
    n=(X-A)//W
    expected=n*(X-A+1)-W*n*(n+1)//2
    assert count_cell(1,1,0,A,W,X)==expected
    assert floor_sum(10**30,1,-3,7)==-3*10**30*(10**30-1)//2+7*10**30


def test_halfplane_envelopes_against_independent_point_enumeration():
    rng=random.Random(2842)
    for _ in range(200):
        F,I,c,A,W,X=(rng.randrange(1,15),rng.randrange(1,7),rng.randrange(-25,26),
                     rng.randrange(1,15),rng.randrange(1,11),rng.randrange(30,151))
        constraints=[(rng.randrange(W+1),rng.randrange(-50,200)) for j in range(rng.randrange(6))]
        cap=rng.randrange(1,30)
        brute=sum(1 for m in range(1,cap+1) for a in range(A,X+1)
                  if a+W*m<=X and m%I==0 and (a-c*m)%F==0
                  and all(a+ell*m>=h for ell,h in constraints))
        assert count_cell(F,I,c,A,W,X,constraints,m_cap=cap)==brute
        assert count_cell(F,I,c,A,W,X)==geometric_count(F,I,c,A,W,X)


def test_augmented_cell_preserves_each_actual_congruence():
    F,I,c=augment_cell(11,1,1,210,[(2,31),(5,37)])
    count=count_cell(F,I,c,30,1260,20000,[(420,31**2),(1050,37**2)],m_cap=10)
    brute=sum(1 for m in range(1,11) for a in range(30,20000-1260*m+1)
              if (a-m)%11==0 and (a+420*m)%31==0 and (a+1050*m)%37==0
              and a+420*m>=31**2 and a+1050*m>=37**2)
    assert count==brute==11
    assert F*I==11*31*37


def test_invalid_counting_domains_are_rejected():
    for args in [(-1,2,1,1),(1,0,1,1)]:
        with pytest.raises(ValueError):floor_sum(*args)
    with pytest.raises(ValueError):
        count_cell(1,1,0,1,10,100,[(11,20)])
    with pytest.raises(ValueError):
        augment_cell(11,1,1,210,[(2,11)])
    assert count_cell(1,1,0,10,10,19)==0


def test_floor_reciprocity_above_machine_integer_limits():
    n,modulus=10**30,10**50+7
    assert floor_sum(n,modulus,modulus-1,0)==(n-1)*(n-2)//2
