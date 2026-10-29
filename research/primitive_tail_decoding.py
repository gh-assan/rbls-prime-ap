"""Exact reconstruction of sparse primitive tail intersections.

This decodes a specified congruence intersection. It neither enumerates all
prime labels nor establishes a positive AP-28 completion score.
"""
from math import gcd,prod
from operator import index

from sympy import isprime,primerange
from sympy.ntheory.modular import crt


def rational_convergents(numerator,denominator):
    numerator,denominator=map(index,(numerator,denominator))
    if numerator<0 or denominator<1:
        raise ValueError('require numerator>=0 and denominator>0')
    p0,p1,q0,q1=0,1,1,0
    while denominator:
        quotient,remainder=divmod(numerator,denominator)
        p0,p1=p1,quotient*p1+p0
        q0,q1=q1,quotient*q1+q0
        yield p1,q1
        numerator,denominator=denominator,remainder


def decode_primitive_box(residue,modulus,a_max,m_max):
    """Return the unique positive primitive (a,m), or None, if N>2*a_max*m_max.

    Completeness is proved by rational reconstruction under the explicit size
    condition. Outside that domain this function raises, rather than reporting
    an unsupported empty intersection.
    """
    residue,modulus,a_max,m_max=map(index,(residue,modulus,a_max,m_max))
    if min(a_max,m_max)<1 or modulus<=2*a_max*m_max:
        raise ValueError('require positive bounds and modulus > 2*a_max*m_max')
    residue%=modulus
    found=[]
    for u,m in rational_convergents(residue,modulus):
        if m>m_max:
            break
        a=residue*m-modulus*u
        if 1<=a<=a_max and gcd(a,m)==1 and gcd(m,modulus)==1:
            found.append((a,m))
    assert len(found)<=1
    return found[0] if found else None


def decode_tail_intersection(k,D,A,X,tags,*,sieve_bound=None,m_cap=None,base_cell=None):
    """Exactly count a specified tail intersection by returning its sole point.

    Return None when its primitive filtered intersection is empty. The size
    condition for complete reconstruction is checked explicitly. Optional
    base_cell is (F,I,K): m=I*v and a=F*u+K*v.
    """
    k,D,A,X=map(index,(k,D,A,X))
    if k<2 or min(D,A)<1:
        raise ValueError('require k>=2,D>0,A>0')
    tags=tuple((index(j),index(q)) for j,q in tags)
    if not tags or len({j for j,q in tags})!=len(tags) or len({q for j,q in tags})!=len(tags):
        raise ValueError('require distinct term indices and distinct tail primes')
    if any(not 0<=j<k or not isprime(q) or D%q==0 for j,q in tags):
        raise ValueError('invalid tail-prime labels')
    if sieve_bound is not None:
        sieve_bound=index(sieve_bound)
        if sieve_bound<2 or A<=sieve_bound or any(q<=sieve_bound for j,q in tags):
            raise ValueError('require A>B>=2 and all tail primes>B')
    if base_cell is not None:
        F,I,K=map(index,base_cell)
        if min(F,I)<1:
            raise ValueError('invalid triangular base cell')
    W=(k-1)*D
    m_max=(X-A)//W
    if m_cap is not None:
        m_max=min(m_max,index(m_cap))
    if m_max<1:
        return None
    modulus=prod(q for j,q in tags)
    residue=int(crt([q for j,q in tags],[-j*D for j,q in tags])[0])
    point=decode_primitive_box(residue,modulus,X-W,m_max)
    if point is None:
        return None
    a,m=point
    if a<A or a+W*m>X or gcd(a,D*m)!=1:
        return None
    if any(q*q>a+j*D*m or (a+j*D*m)%q for j,q in tags):
        return None
    if base_cell is not None and (m%I or (a-K*(m//I))%F):
        return None
    if sieve_bound is not None:
        for p in primerange(2,sieve_bound+1):
            if any((a+j*D*m)%p==0 for j in range(k)):
                return None
    return point
