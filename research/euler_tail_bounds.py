"""Rigorous Euler-product truncation enclosures, not prime-count bounds."""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from operator import index

from sympy import factorint, primerange


def partial_interval(r,D,P,precision=60,ratio=False):
    """Outward rounded partial product; each input factor is an exact rational."""
    r,D,P,precision=map(index,(r,D,P,precision))
    if r<2 or D<1 or P<=r+1 or precision<10:
        raise ValueError('invalid Euler-product parameters')
    if any(D%int(p) for p in primerange(2,r+2)):
        raise ValueError('D must contain every prime <= r+1')
    if max(factorint(D),default=1)>P:
        raise ValueError('P must include every prime divisor of D')
    lo=hi=Decimal(1)
    for p in primerange(2,P+1):
        p=int(p)
        if ratio:
            if D%p==0:
                continue
            denominator=p*(p-r-1)
            numerator=denominator+r
        elif D%p==0:
            numerator,denominator=p**r,(p-1)**r
        else:
            numerator,denominator=(p-r)*p**(r-1),(p-1)**r
        with localcontext() as context:
            context.prec=precision
            context.rounding=ROUND_FLOOR
            lo=lo*Decimal(numerator)/Decimal(denominator)
        with localcontext() as context:
            context.prec=precision
            context.rounding=ROUND_CEILING
            hi=hi*Decimal(numerator)/Decimal(denominator)
    return Fraction(lo),Fraction(hi)


def certified_constants(r=27,D=223092870,P=100000,precision=60):
    r,D,P=map(index,(r,D,P))
    beta_lo,beta_hi=partial_interval(r,D,P,precision)
    ratio_lo,ratio_hi=partial_interval(r,D,P,precision,ratio=True)
    epsilon=Fraction(r*(r-1)*(P+1)**2,2*P**2*(P+1-r))
    ratio_epsilon=Fraction(r*(P+1),P*(P-r))
    if max(epsilon,ratio_epsilon)>=1:
        raise ValueError('P is too small for the stated nontrivial rational enclosure')
    beta_infinite_lo=beta_lo*(1-epsilon)
    ratio_infinite_hi=ratio_hi/(1-ratio_epsilon)
    return dict(r=r,D=D,P=P,precision=precision,
                beta_partial_interval=(beta_lo,beta_hi),
                beta_log_tail_bound=epsilon,
                beta_infinite_interval=(beta_infinite_lo,beta_hi),
                ratio_partial_interval=(ratio_lo,ratio_hi),
                ratio_log_tail_bound=ratio_epsilon,
                ratio_infinite_interval=(ratio_lo,ratio_infinite_hi))


def decimal_enclosure(value,digits,rounding):
    value=Fraction(value)
    with localcontext() as context:
        context.prec=digits
        context.rounding=rounding
        return str(Decimal(value.numerator)/Decimal(value.denominator))


def readable_certificate():
    exact=certified_constants()
    result={key:value for key,value in exact.items() if isinstance(value,int)}
    result['status']='Rigorous constant enclosures only; finite-height AP28 count error remains unbounded.'
    for key in ['beta_partial_interval','beta_infinite_interval','ratio_partial_interval','ratio_infinite_interval']:
        lo,hi=exact[key]
        result[key]=dict(lower=decimal_enclosure(lo,22,ROUND_FLOOR),
                         upper=decimal_enclosure(hi,22,ROUND_CEILING),
                         exact_lower=str(lo),exact_upper=str(hi))
    for key in ['beta_log_tail_bound','ratio_log_tail_bound']:
        result[key]=str(exact[key])
    return result


if __name__=='__main__':
    import json
    print(json.dumps(readable_certificate(),indent=2))
