from math import gcd

import pytest
from research.projective_lattice import (allowed_directions, belongs_to_cell,
                                          cell_basis, reduced_basis)


@pytest.mark.parametrize('p',[29,31,37,41,43])
def test_projective_local_count(p):
    k,D=28,223092870
    choices=allowed_directions(k,D,p)
    good=[]
    for a in range(p):
        for m in range(p):
            if all((a+j*D*m)%p for j in range(k)):
                good.append((a,m))
                assert (None if m==0 else a*pow(m,-1,p)%p) in choices
    assert len(good)==(p-1)*(p-k+1)
    assert len(choices)==p+1-k


@pytest.mark.parametrize('choices',[{29:None,31:223092870%31},
                                    {29:223092870%29,31:None},
                                    {29:223092870%29,31:223092870%31}])
def test_lattice_basis_exact_and_primitive_point_filter(choices):
    k,D=28,223092870
    basis=cell_basis(k,D,choices)
    reduced=reduced_basis(k,D,choices)
    transform=reduced*basis.inv()
    assert all(v.q==1 for v in transform)
    assert abs(int(transform.det()))==1
    for u in range(-4,5):
        for v in range(-4,5):
            a,m=map(int,(u*basis[0,:]+v*basis[1,:]))
            for p,slope in choices.items():
                assert (m%p==0) if slope is None else ((a-slope*m)%p==0)
            if belongs_to_cell(a,m,k,D,choices):
                assert gcd(a,D*m)==1
                assert all((a+j*D*m)%p for p in choices for j in range(k))


def test_positive_primitive_point_certificate():
    k,D=28,223092870
    choices={29:None,31:D%31,37:2*D%37,41:3*D%41}
    assert belongs_to_cell(2489407,116,k,D,choices)
    assert all((2489407+j*D*116)%p for p in choices for j in range(k))
    assert not belongs_to_cell(2*2489407,2*116,k,D,choices)


def test_two_variable_factor_identity():
    from math import prod
    from prime_ap import singular_series
    from sympy import primerange
    k,D,P=28,223092870,100000
    product=1.0
    for p in primerange(2,P+1):
        if D%p==0:
            product *= (1-1/p)**(1-k)
        else:
            product *= (1-(k-1)/p)/(1-1/p)**(k-1)
    phi=prod(p-1 for p in primerange(2,29))
    assert product == pytest.approx(singular_series(k-1,D)*D/phi)
    assert product/singular_series(k,D) == pytest.approx(3.54943806)
