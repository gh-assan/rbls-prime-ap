from decimal import Decimal
from fractions import Fraction
from math import comb,gcd
import random

import pytest
from sympy import primerange

from research.completion_certificates import paired_minorant
from research.euler_tail_bounds import certified_constants,partial_interval
from research.lattice_floor_counts import count_triangular_cell
from research.primitive_cells import intersect_divisibility,primitive_count
from research.signed_tail_aggregation import aggregate_events,positive_pruning
from research.witness_localization import certified_child,localize_exact


def test_divisibility_intersections_match_integer_membership():
    rng=random.Random(291)
    for _ in range(80):
        F,I,K,A,t=rng.randrange(1,15),rng.randrange(1,8),rng.randrange(-15,16),rng.randrange(1,15),rng.randrange(1,12)
        f,i,k=intersect_divisibility(F,I,K,A,t)
        for m in range(1,55):
            for a in range(1,70):
                expected=m%I==0 and (a-K*(m//I))%F==0 and a%A==0 and m%t==0
                actual=m%i==0 and (a-k*(m//i))%f==0
                assert actual==expected


def test_general_triangular_basis_does_not_assume_integer_slope():
    f,i,k=intersect_divisibility(2,3,3,5,1)
    assert i==3 and k%i!=0
    expected=sum(1 for m in range(1,51) for a in range(1,101)
                 if m%3==0 and (a-m)%2==0 and a%5==0 and a+2*m<=100)
    assert count_triangular_cell(f,i,k,1,2,100)==expected


def test_primitive_mobius_count_with_extra_halfplanes():
    rng=random.Random(292)
    for _ in range(40):
        F,I,K=rng.randrange(1,8),rng.randrange(1,5),rng.randrange(-10,11)
        A,W,X,D,cap=5,6,rng.randrange(60,150),rng.choice([6,30,210]),12
        constraints=[(2,35),(4,55)]
        expected=sum(1 for m in range(1,cap+1) for a in range(A,X+1)
                     if a+W*m<=X and m%I==0 and (a-K*(m//I))%F==0
                     and gcd(a,D*m)==1 and all(a+ell*m>=h for ell,h in constraints))
        actual=primitive_count(F,I,K,A,W,X,D,(x for x in constraints),cap)
        assert actual==expected


def test_outward_rounding_contains_exact_small_products():
    r,D,P=3,6,31
    beta=ratio=Fraction(1)
    for p in primerange(2,P+1):
        if D%p==0:
            beta*=Fraction(p**r,(p-1)**r)
        else:
            beta*=Fraction((p-r)*p**(r-1),(p-1)**r)
            ratio*=1+Fraction(r,p*(p-r-1))
    for is_ratio,exact in [(False,beta),(True,ratio)]:
        lo,hi=partial_interval(r,D,P,10,ratio=is_ratio)
        assert lo<=exact<=hi


def test_euler_bounds_nest_higher_precision_and_later_partial_products():
    low=certified_constants(3,6,31,20)
    high=certified_constants(3,6,1000,60)
    lo,hi=low['beta_infinite_interval']
    a,b=high['beta_partial_interval']
    assert lo<=a<=b<=hi
    lo,hi=low['ratio_infinite_interval']
    a,b=high['ratio_partial_interval']
    assert lo<=a<=b<=hi
    for ratio in [False,True]:
        a,b=partial_interval(3,6,31,10,ratio)
        x,y=partial_interval(3,6,31,60,ratio)
        assert a<=x<=y<=b


def test_signed_aggregation_matches_all_moments_despite_duplicates():
    rng=random.Random(293)
    k,N,roots=7,50,(2,5)
    matrix=[[rng.randrange(2) for j in range(k)] for i in range(N)]
    events=[(i,j) for i,row in enumerate(matrix) for j,x in enumerate(row) if x]
    repeated=events+events
    rng.shuffle(repeated)
    result=aggregate_events(N,k,repeated,roots)
    defects=list(map(sum,matrix))
    assert result['defects']==defects
    assert result['unique_updates']==sum(defects)
    assert result['moments']==[sum(comb(c,r) for c in defects) for r in range(6)]
    assert result['score']==sum(paired_minorant(c,roots) for c in defects)
    before,after=positive_pruning([paired_minorant(c,roots) for c in defects],
                                 [i for i,c in enumerate(defects) if c])
    assert before==result['score']
    assert after==defects.count(0)


def test_localization_preserves_positive_score_with_negative_siblings():
    scores=[Fraction(-3),0,Fraction(1),-1,0,1,0,-2,1]
    # Choose a family with positive total and genuine negative subregions.
    scores[0]=Fraction(-1,2)
    scores[-2]=Fraction(-1,4)
    assert sum(scores)>0
    result=localize_exact(len(scores),lambda lo,hi:sum(scores[lo:hi]))
    assert scores[result['index']]>0
    assert result['calls']<=1+(len(scores)-1).bit_length()


def test_interval_child_selection_needs_no_independent_child_lower_bounds():
    assert certified_child(Fraction(1,3),Fraction(-1,7),Fraction(1,8))==('right',Fraction(5,24))
    assert certified_child(1,-1,2) is None
    assert certified_child(1,Fraction(1,10),2)==('left',Fraction(1,10))


def test_invalid_contract_inputs_are_rejected():
    with pytest.raises(ValueError):intersect_divisibility(0,1,0,1,1)
    with pytest.raises(ValueError):primitive_count(1,1,0,1,1,100,0)
    with pytest.raises(ValueError):aggregate_events(1,3,[(1,0)],(2,))
    with pytest.raises(ValueError):aggregate_events(0,3,[],(0,))
    with pytest.raises(ValueError):localize_exact(0,lambda a,b:0)
    with pytest.raises(ValueError):localize_exact(1,lambda a,b:0)
    with pytest.raises(ValueError):certified_child(1,2,1)


def test_boolean_coverage_handles_nonsemiprime_terms():
    from sympy import isprime
    family=[[97,103,109],[105,111,117]]
    events=[(i,j) for i,row in enumerate(family) for j,n in enumerate(row)
            for q in primerange(3,11) if n%q==0 and q*q<=n]
    assert events.count((1,0))==3
    report=aggregate_events(2,3,events,(2,))
    assert report['defects']==[0,3]
    assert report['union_size']==1
    assert report['score']==1
    assert sum(all(isprime(n) for n in row) for row in family)==1


def test_actual_hidden_tail_family_stays_within_uint64():
    from research.hidden_tail_family import certificate
    report=certificate()
    for a,cofactor in zip(report['starts'],report['forced_first_term_cofactors']):
        assert a==41*cofactor and cofactor>1
        assert a+27*report['D']<2**64
        assert all((a+j*report['D'])%p for p in primerange(2,38) for j in range(28))
