"""Exact primal/dual and limited-independence checks for the third paper."""
from fractions import Fraction
from math import comb, gcd, isqrt
from operator import index

from sympy import Matrix, Rational, isprime, primerange

from research.completion_certificates import binomial_coefficients, lower_bound, model_moments, paired_minorant


def zero_mass_binomial(k, p, order):
    """Remove mass at zero while preserving moments through order.

    A sufficient domain is p >= (order+1)/(k+order+1). The returned law is an
    abstract defect model, not a distribution of arithmetic progressions.
    """
    k,order=map(index,(k,order))
    p=Fraction(p)
    n=order+1
    if not 0 <= order < k or not 0 < p < 1 or p/(1-p) < Fraction(n,k):
        raise ValueError('parameters outside the proved nonnegativity domain')
    weights=[comb(k,c)*p**c*(1-p)**(k-c) for c in range(k+1)]
    original_zero=weights[0]
    for c in range(n+1):
        weights[c]-=original_zero*(-1)**c*comb(n,c)
    if weights[0]!=0 or min(weights)<0 or sum(weights)!=1:
        raise AssertionError('invalid zero-mass certificate')
    for r in range(order+1):
        assert sum(w*comb(c,r) for c,w in enumerate(weights) if c>=r)==comb(k,r)*p**r
    return tuple(weights)


def sharp_paired_certificate(k, moments, roots):
    """Prove sharpness by matching a feasible law on the minorant contact set.

    No numerical LP solver is trusted. The independent rational primal/dual
    checks prove sharpness over nonnegative real histogram weights.
    Fixed-size integer histograms can yield additional rounding information.
    """
    k=index(k)
    roots=tuple(map(index,roots))
    support=[0,1]+[c for r in roots for c in (r,r+1)]
    degree=1+2*len(roots)
    if len(set(support))!=len(support) or min(support)<0 or max(support)>k:
        raise ValueError('distinct contact points in 0..k are required')
    if len(moments)<degree+1:
        raise ValueError('insufficient moments')
    matrix=Matrix([[comb(c,r) if c>=r else 0 for c in support] for r in range(degree+1)])
    target=Matrix([Rational(Fraction(m).numerator,Fraction(m).denominator) for m in moments[:degree+1]])
    solution=matrix.inv()*target
    if any(w<0 for w in solution):
        raise ValueError('contact set is not primal feasible for these moments')
    assert matrix*solution==target
    assert all(paired_minorant(c,roots)<=(1 if c==0 else 0) for c in range(k+1))
    value=lower_bound(moments,roots)
    weights=tuple(Fraction(w) for w in solution)
    assert weights[0]==value
    return dict(k=k,roots=list(roots),support=support,weights=[str(w) for w in weights],
                binomial_moments=[str(m) for m in moments[:degree+1]],
                coefficients=[str(b) for b in binomial_coefficients(roots)],
                sharp_lower_bound=str(value))


def arithmetic_seven():
    """Actual rough AP-7 family; defect labels are checked against primality."""
    k,D,B,X=7,210,29,20000
    assert B**3>X and 10<=B
    small=tuple(primerange(2,B+1))
    tail=tuple(primerange(B+1,isqrt(X)+1))
    histogram=[0]*(k+1)
    examples=[]
    for m in range(1,11):
        for a in range(B+1,X-(k-1)*D*m+1):
            terms=[a+j*D*m for j in range(k)]
            if any(n%p==0 for n in terms for p in small):
                continue
            # Roughness and m<=B imply this, without a separate gcd sieve.
            assert gcd(a,D*m)==1
            incidences=[(j,int(q)) for j,n in enumerate(terms) for q in tail
                        if n%q==0 and q*q<=n]
            defects=len(incidences)
            assert defects==sum(not isprime(n) for n in terms)
            assert len({q for j,q in incidences})==defects
            histogram[defects]+=1
            if defects==0 and len(examples)<3:
                examples.append(dict(a=a,d=D*m,terms=terms))
    moments=[sum(count*comb(c,r) for c,count in enumerate(histogram) if c>=r) for r in range(k+1)]
    certificate=sharp_paired_certificate(k,moments,(2,5))
    return dict(k=k,D=D,B=B,X=X,multipliers=list(range(1,11)),
                histogram=histogram,binomial_moments=moments,examples=examples,
                actual_prime_progressions=histogram[0],certificate=certificate)
