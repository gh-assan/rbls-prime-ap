"""Reproduce exact certificates and labeled sparsity proxies in paper three."""
import json
from fractions import Fraction
from math import comb,exp,log
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.completion_certificates import model_moments
from research.coupled_moments import arithmetic_seven,sharp_paired_certificate,zero_mass_binomial
from research.lattice_floor_counts import augment_cell,count_cell


def analysis():
    p=Fraction(2,5)
    weights=zero_mass_binomial(28,p,5)
    counterexample=dict(label='abstract exchangeable defect law; not arithmetic AP28 data',
                       k=28,p=str(p),matched_order=5,zero_mass=str(weights[0]),
                       weights=[str(w) for w in weights],
                       normalized_moments=[str(m) for m in model_moments(28,p)[:6]],
                       subset_all_one_probabilities=[str(sum(w*comb(c,r) for c,w in enumerate(weights) if c>=r)/comb(28,r))
                                                     for r in range(1,6)])
    sharp=sharp_paired_certificate(28,model_moments(28,Fraction(1,10)),(3,6))
    sharp['label']='sharp bound for supplied binomial moments, not AP28 arithmetic'
    actual=arithmetic_seven()
    F,I,c=augment_cell(11,1,1,210,[(2,31),(5,37)])
    count=count_cell(F,I,c,30,1260,20000,[(420,31**2),(1050,37**2)],m_cap=10)
    brute=[(a,m) for m in range(1,11) for a in range(30,20000-1260*m+1)
           if (a-m)%11==0 and (a+420*m)%31==0 and (a+1050*m)%37==0
           and a+420*m>=31**2 and a+1050*m>=37**2]
    assert len(brute)==count
    X=2**64-1;W=27*223092870
    volume=Fraction((X-29-W)**2,2*W)
    sparse=[]
    for theta,order in [(1/3,5),(1/(1+exp(1/9)),5),(1/(1+exp(1/19)),3)]:
        bound=X**theta
        sparse.append(dict(theta=theta,order=order,sieve_bound_scale=bound,
                           area_over_minimum_tail_index_Q1=float(volume)/bound**order))
    B=2396179891
    H=X-(B+1)-W
    cap_ratio=Fraction(W*(B-1),H)
    cap_fraction=2*cap_ratio-cap_ratio**2
    assert 2642246**3>X and B**3>X
    return dict(status='Exact moment/counter certificates plus explicitly labeled geometric proxies; no AP28 witness.',
                sharp_model_certificate=sharp,zero_mass_counterexample=counterexample,
                arithmetic_AP7=actual,
                geometric_example=dict(base=[11,1,1],tags=[[2,31],[5,37]],augmented_cell=[F,I,c],
                                       A=30,W=1260,X=20000,m_cap=10,count=count,pairs=brute,
                                       note='geometric count before remaining roughness exclusions'),
                uint64_sparsity_proxies=sparse,
                exact_fifth_intersection_proxy_upper_bound_Q1=str(Fraction(2642246,2*W)),
                multiplier_cap_example=dict(X=X,B=B,A=B+1,area_fraction=str(cap_fraction),
                                            area_fraction_float=float(cap_fraction),
                                            note='geometric area retained; not a retained-prime-count guarantee'),
                cubic_model=dict(defect_probability='1/20',normalized_lower_bound='731/4000',
                                 theta=1/(1+exp(1/19)),
                                 normalized_moments=[str(m) for m in model_moments(28,Fraction(1,20))[:4]]))


if __name__=='__main__':
    result=analysis()
    path=Path(__file__).resolve().parents[1]/'results'/'coupled-analysis.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
