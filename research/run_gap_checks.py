"""Reproducible checks for the four gap papers; no AP-28 discovery claim."""
import json
from fractions import Fraction
from math import gcd,isqrt
from pathlib import Path
import sys

from sympy import isprime,primerange

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.completion_certificates import paired_minorant
from research.euler_tail_bounds import readable_certificate
from research.hidden_tail_family import certificate as hidden_tail_certificate
from research.primitive_cells import intersect_divisibility,primitive_count
from research.signed_tail_aggregation import aggregate_events,positive_pruning
from research.witness_localization import localize_exact


def checks():
    k,D,B,X,cap=7,210,29,20000,10
    small=tuple(primerange(2,B+1))
    tail=tuple(primerange(B+1,isqrt(X)+1))
    family=[]
    events=[]
    for m in range(1,cap+1):
        for a in range(B+1,X-(k-1)*D*m+1):
            terms=[a+j*D*m for j in range(k)]
            if any(n%p==0 for n in terms for p in small):
                continue
            row=len(family)
            family.append((a,m))
            for j,n in enumerate(terms):
                for q in tail:
                    if n%q==0 and q*q<=n:
                        events.append((row,j))
    result=aggregate_events(len(family),k,events,(2,5))
    scores=[paired_minorant(c,(2,5)) for c in result['defects']]
    before,after=positive_pruning(scores,[i for i,c in enumerate(result['defects']) if c])
    assert before==result['score'] and after==78
    prefix=[Fraction(0)]
    for score in scores:
        prefix.append(prefix[-1]+score)
    localization=localize_exact(len(family),lambda lo,hi:prefix[hi]-prefix[lo])
    a,m=family[localization['index']]
    terms=[a+j*D*m for j in range(k)]
    assert all(isprime(n) for n in terms)
    basis=intersect_divisibility(2,3,3,5,1)
    primitive=primitive_count(*basis,1,2,100,6)
    brute=sum(1 for m0 in range(1,50) for a0 in range(1,101)
              if m0%3==0 and (a0-m0)%2==0 and a0%5==0 and a0+2*m0<=100
              and gcd(a0,6*m0)==1)
    assert primitive==brute
    return dict(status='Exact small-family checks and rigorous constants. G2/G3 finite-height AP28 arithmetic remains open.',
                G1=dict(input_basis=[2,3,3],a_divisor=5,m_divisor=1,
                        intersection_basis=list(basis),primitive_D=6,A=1,W=2,X=100,
                        exact_primitive_count=primitive,independent_brute_count=brute),
                G2=dict(k=k,D=D,B=B,X=X,m_cap=cap,rough_candidates=len(family),
                        distinct_composite_incidences=result['unique_updates'],
                        binomial_moments=result['moments'],signed_score=str(result['score']),
                        covered_candidates=result['union_size'],zero_defect_count=len(family)-result['union_size'],
                        score_after_pruning=str(after),
                        coverage='all starts and m in the stated finite range, all tail primes B<q<=sqrt(X)'),
                G3=readable_certificate(),
                G5=hidden_tail_certificate(),
                G4=dict(index=localization['index'],oracle_calls=localization['calls'],
                        trace=localization['trace'],a=a,m=m,d=D*m,terms=terms,
                        singleton_score=str(localization['singleton_score']),
                        independent_primality_checks='all seven passed SymPy isprime',
                        note='localization uses a precomputed score on an explicit AP7 family, not an AP28 oracle'))


if __name__=='__main__':
    result=checks()
    path=Path(__file__).resolve().parents[1]/'results'/'gap-checks.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
