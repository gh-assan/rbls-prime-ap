"""Actual arithmetic counterfamily to certification from finite local data alone."""
from math import prod

from sympy import primerange
from sympy.ntheory.modular import crt


def certificate():
    k,D,B,q=28,223092870,37,41
    extra=tuple(int(p) for p in primerange(29,B+1))
    Q=prod(extra)
    a0,period=map(int,crt([D,Q,q],[1,D%Q,0]))
    first=a0+max(0,(10**15-a0+period-1)//period)*period
    starts=[first+t*period for t in range(10)]
    small=tuple(int(p) for p in primerange(2,B+1))
    for a in starts:
        terms=[a+j*D for j in range(k)]
        assert terms[-1]<2**64
        assert all(n%p for n in terms for p in small)
        assert a>q and a%q==0
    return dict(k=k,D=D,B=B,hidden_prime=q,Q=Q,residue=a0,period=period,
                first=first,starts=starts,forced_first_term_cofactors=[a//q for a in starts],
                actual_prime_progressions=0,
                claim='All terms pass primes <=37; first term is composite by factor 41.',
                limitation='This deliberately selected subfamily has a fixed tail divisor; '
                           'it does not contradict a full singular-series model that includes it.')
