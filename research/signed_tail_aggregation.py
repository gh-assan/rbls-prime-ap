"""Exact incidence aggregation on an explicitly covered finite candidate set."""
from fractions import Fraction
from math import comb
from operator import index

from research.completion_certificates import paired_minorant


def aggregate_events(candidate_count,k,events,roots):
    """Each event is a verified (candidate_index, composite_term_index).

    Completeness and validity of the external event generator are assumptions
    to check separately. Duplicate events do not change the result.
    """
    candidate_count,k=map(index,(candidate_count,k))
    if candidate_count<0 or k<1:
        raise ValueError('invalid finite family size or progression length')
    roots=tuple(roots)
    paired_minorant(0,roots)  # validate even when the input family is empty
    degree=1+2*len(roots)
    masks=[0]*candidate_count
    counts=[0]*candidate_count
    moments=[candidate_count]+[0]*degree
    score=Fraction(candidate_count)
    updates=0
    for candidate,term in events:
        candidate,term=map(index,(candidate,term))
        if not 0<=candidate<candidate_count or not 0<=term<k:
            raise ValueError('event outside the declared family')
        flag=1<<term
        if masks[candidate]&flag:
            continue
        old=counts[candidate]
        counts[candidate]+=1
        masks[candidate]|=flag
        for r in range(1,degree+1):
            if old>=r-1:
                moments[r]+=comb(old,r-1)
        score+=paired_minorant(old+1,roots)-paired_minorant(old,roots)
        updates+=1
    defects=counts
    assert score==sum(paired_minorant(c,roots) for c in defects)
    return dict(defects=defects,moments=moments,score=score,
                union_size=sum(mask!=0 for mask in masks),unique_updates=updates)


def positive_pruning(scores,known_composites):
    """Remove certified composite points; an admissible minorant cannot decrease."""
    scores=list(map(Fraction,scores))
    removed=set(map(index,known_composites))
    if any(not 0<=i<len(scores) or scores[i]>0 for i in removed):
        raise ValueError('removed points must have nonpositive minorant scores')
    before=sum(scores)
    after=sum(score for i,score in enumerate(scores) if i not in removed)
    assert after>=before
    return before,after
