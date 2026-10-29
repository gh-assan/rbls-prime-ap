"""Exact two-dimensional counts using Euclidean floor-sum reciprocity.

Counts geometric congruence cells. Roughness and origin/gcd exclusions not
encoded by the supplied cell are not silently added.
"""
from fractions import Fraction
from itertools import combinations
from math import gcd
from operator import index

from sympy import isprime
from sympy.ntheory.modular import crt


def floor_sum(n, modulus, a, b):
    """Sum floor((a*i+b)/modulus), 0<=i<n, with exact signed integers."""
    n,modulus,a,b=map(index,(n,modulus,a,b))
    if n<0 or modulus<1:
        raise ValueError('require n>=0 and modulus>0')
    total=0
    while True:
        qa,a=divmod(a,modulus)
        qb,b=divmod(b,modulus)
        total+=qa*n*(n-1)//2+qb*n
        height=a*n+b
        if height<modulus:
            return total
        n,b=divmod(height,modulus)
        modulus,a=a,modulus


def augment_cell(F,I,c,D,tags):
    """Add a+j*D*m=0 mod q for distinct primes coprime with F*I."""
    F,I,c,D=map(index,(F,I,c,D))
    if min(F,I,D)<1:
        raise ValueError('F,I,D must be positive')
    used=set()
    for j,q in tags:
        j,q=map(index,(j,q))
        if j<0 or not isprime(q) or gcd(q,F*I)!=1 or q in used:
            raise ValueError('require distinct new primes coprime with cell determinant')
        c=int(crt([F,q],[c,-j*D])[0])
        F*=q
        used.add(q)
    return int(F),int(I),int(c)


def count_triangular_cell(F,I,K,A,W,X,lower_constraints=(),m_cap=None):
    """Count a=F*u+K*v, m=I*v in a>=A,m>=1,a+W*m<=X.

    Each lower constraint (ell,h) means a+ell*m>=h, with 0<=ell<=W.
    The count is exact before any additional primitive-point/roughness filters.
    """
    F,I,K,A,W,X=map(index,(F,I,K,A,W,X))
    if min(F,I,A,W)<1:
        raise ValueError('F,I,A,W must be positive')
    lines=[(0,A)]
    for ell,h in lower_constraints:
        ell,h=map(index,(ell,h))
        if not 0<=ell<=W:
            raise ValueError('require 0<=ell<=W')
        lines.append((ell,h))
    V=(X-A)//(W*I)
    if m_cap is not None:
        V=min(V,index(m_cap)//I)
    for ell,h in lines:
        if h>X:
            return 0
        if ell<W:
            V=min(V,(X-h)//((W-ell)*I))
    if V<1:
        return 0
    cuts={1,V+1}
    for (ell1,h1),(ell2,h2) in combinations(lines,2):
        if ell1!=ell2:
            crossing=Fraction(h1-h2,(ell1-ell2)*I)
            cut=crossing.numerator//crossing.denominator+1
            if 1<cut<V+1:
                cuts.add(cut)
    cuts=sorted(cuts)
    answer=0
    for lo,hi in zip(cuts,cuts[1:]):
        ell,h=max(lines,key=lambda line:line[1]-line[0]*I*lo)
        length=hi-lo
        upper=-W*I-K
        lower=ell*I+K
        answer+=floor_sum(length,F,upper,X+upper*lo)
        answer+=floor_sum(length,F,lower,-h+lower*lo)
        answer+=length
    assert answer>=0
    return answer


def count_cell(F,I,c,A,W,X,lower_constraints=(),m_cap=None):
    """Compatibility wrapper for cells with K=c*I."""
    I,c=map(index,(I,c))
    return count_triangular_cell(F,I,c*I,A,W,X,lower_constraints,m_cap)
