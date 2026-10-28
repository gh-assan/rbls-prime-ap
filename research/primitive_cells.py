"""Exact finite primitive-point corrections; no large-domain runtime claim."""
from math import gcd
from operator import index

from sympy import factorint, mobius

from research.lattice_floor_counts import count_triangular_cell


def intersect_divisibility(F,I,K,a_divisor,m_divisor):
    """Intersect a=F*u+K*v,m=I*v with a_divisor|a, m_divisor|m."""
    F,I,K,A,t=map(index,(F,I,K,a_divisor,m_divisor))
    if min(F,I,A,t)<1:
        raise ValueError('lattice diagonals and divisors must be positive')
    v0=t//gcd(I,t)
    M,K0=I*v0,K*v0
    g=gcd(F,A)
    h=g//gcd(g,K0)
    modulus=A//g
    U=0 if modulus==1 else (-K0*h//g*pow(F//g,-1,modulus))%modulus
    newF=F*modulus
    return newF,M*h,(F*U+K0*h)%newF


def squarefree_divisors_with_mobius(D):
    terms=[(1,1)]
    for p in factorint(D):
        terms += [(s*int(p),-mu) for s,mu in terms.copy()]
    return terms


def primitive_count(F,I,K,A,W,X,D,lower_constraints=(),m_cap=None):
    """Count points with gcd(a,D*m)=1 by two exact finite Möbius sums.

    Cost includes up to 2**omega(D)*floor((X-A)/W) intersection counts;
    the formula does not assert that this is affordable for AP-28 heights.
    """
    F,I,K,A,W,X,D=map(index,(F,I,K,A,W,X,D))
    if min(F,I,A,W,D)<1:
        raise ValueError('require positive F,I,A,W,D')
    cap=(X-A)//W
    if m_cap is not None:
        cap=min(cap,index(m_cap))
    total=0
    constraints=tuple(lower_constraints)
    divisor_terms=squarefree_divisors_with_mobius(D)
    for t in range(1,cap+1):
        mu_t=int(mobius(t))
        if not mu_t:
            continue
        for s,mu_s in divisor_terms:
            divisor=s*t//gcd(s,t)
            newF,newI,newK=intersect_divisibility(F,I,K,divisor,t)
            total+=mu_s*mu_t*count_triangular_cell(newF,newI,newK,A,W,X,constraints,cap)
    assert total>=0
    return total
