"""Exact checks for the follow-up paper. These are not an AP-28 search claim."""
from fractions import Fraction
from math import comb, gcd, isqrt, prod
from operator import index

from sympy import isprime, primerange


def paired_minorant(c, roots):
    """P(0)=1 and P(c)<=0 at every positive integer c."""
    c = int(index(c))
    roots = tuple(int(index(r)) for r in roots)
    if any(r < 1 for r in roots):
        raise ValueError('pair roots must be positive integers')
    return Fraction((1-c)*prod((c-r)*(c-r-1) for r in roots),
                    prod(r*(r+1) for r in roots))


def binomial_coefficients(roots):
    """Newton expansion P(c)=sum b_r*binom(c,r), by exact differences."""
    roots = tuple(roots)
    degree = 1 + 2*len(roots)
    values = [paired_minorant(c,roots) for c in range(degree+1)]
    result = []
    while values:
        result.append(values[0])
        values = [b-a for a,b in zip(values,values[1:])]
    return tuple(result)


def lower_bound(moments, roots):
    coefficients = binomial_coefficients(roots)
    if len(moments) < len(coefficients):
        raise ValueError('insufficient moments for this polynomial')
    return sum(b*Fraction(m) for b,m in zip(coefficients,moments))


def interval_lower_bound(estimates, errors, roots):
    coefficients = binomial_coefficients(roots)
    if len(estimates) < len(coefficients) or len(errors) < len(coefficients):
        raise ValueError('insufficient moment intervals')
    if any(Fraction(e) < 0 for e in errors):
        raise ValueError('errors must be nonnegative')
    return sum(b*Fraction(m)-abs(b)*Fraction(e)
               for b,m,e in zip(coefficients,estimates,errors))


def model_moments(k, defect_probability):
    p = Fraction(defect_probability)
    if k < 1 or not 0 <= p <= 1:
        raise ValueError('invalid model parameters')
    return tuple(comb(k,r)*p**r for r in range(k+1))


def geometric_count(F,I,c,A,W,X):
    """Count a=F*u+c*I*v, m=I*v with a>=A,m>=1,a+W*m<=X.

    This counts a lattice before primitive-point/origin exclusions.
    """
    if min(F,I,A,W) < 1:
        raise ValueError('F,I,A,W must be positive')
    total = 0
    for v in range(1,(X-A)//(W*I)+1):
        lower = -((c*I*v-A)//F)  # ceil((A-c*I*v)/F)
        upper = (X-W*I*v-c*I*v)//F
        total += max(0,upper-lower+1)
    return total


def finite_certificate():
    """A small AP-5 arithmetic check with prime/semiprime terms, not a model."""
    k,D,B,X = 5,30,20,5000
    assert B**3 > X
    small = tuple(primerange(2,B+1))
    tail = tuple(primerange(B+1,isqrt(X)+1))
    defects, tail_defects, examples = [], [], []
    total_semiprime_incidence = 0
    for a in range(B+1,2000):
        for m in range(1,5):
            terms = [a+j*D*m for j in range(k)]
            if terms[-1] > X or gcd(a,D*m) != 1:
                continue
            if any(n % p == 0 for n in terms for p in small):
                continue
            assert all(gcd(x,y)==1 for j,x in enumerate(terms) for y in terms[j+1:])
            c = sum(not isprime(n) for n in terms)
            # A semiprime has exactly one least prime factor q<=sqrt(n).
            found = [(j,int(q)) for j,n in enumerate(terms) for q in tail
                     if n % q == 0 and q*q <= n]
            assert len(found)==c
            assert len({q for j,q in found})==len(found)
            defects.append(c)
            tail_defects.append(len(found))
            total_semiprime_incidence += len(found)
            if c==0 and len(examples)<3:
                examples.append(dict(a=a,d=D*m,terms=terms))
    moments = [sum(comb(c,r) for c in defects) for r in range(k+1)]
    tail_moments = [sum(comb(c,r) for c in tail_defects) for r in range(k+1)]
    assert moments == tail_moments
    roots = (2,)
    bound = lower_bound(moments,roots)
    actual = defects.count(0)
    assert 0 < bound <= actual
    return dict(k=k,D=D,B=B,X=X,start_interval=[B+1,2000],multipliers=[1,2,3,4],
                rough_candidates=len(defects),defect_histogram=[defects.count(c) for c in range(k+1)],
                binomial_moments=moments,tail_incidence=total_semiprime_incidence,
                polynomial_roots=list(roots),certified_lower_bound=str(bound),
                actual_prime_progressions=actual,examples=examples)


def model_certificate():
    k=28
    roots=(3,7)
    moments=model_moments(k,Fraction(1,10))
    coefficients=binomial_coefficients(roots)
    bound=lower_bound(moments,roots)
    actual=Fraction(9,10)**28
    classical=sum((-1)**r*moments[r] for r in range(6))
    assert all(paired_minorant(c,roots) <= (1 if c==0 else 0) for c in range(k+1))
    assert classical < 0 < bound < actual
    return dict(label='independent binomial calibration, not arithmetic AP28 evidence',k=k,
                defect_probability='1/10',roots=list(roots),
                coefficients=[str(x) for x in coefficients],
                normalized_moments=[str(x) for x in moments[:6]],
                degree_five_bonferroni=str(classical),paired_lower_bound=str(bound),
                paired_lower_bound_float=float(bound),actual_zero_probability=str(actual),
                actual_zero_probability_float=float(actual),
                uniform_moment_error_budget_float=float(bound/sum(map(abs,coefficients))))


if __name__ == '__main__':
    import json
    print(json.dumps(dict(arithmetic_AP5=finite_certificate(),model_AP28=model_certificate()),indent=2))
