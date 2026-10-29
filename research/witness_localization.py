"""Constructive localization contract for an additive, exactly evaluated score."""
from fractions import Fraction
from operator import index


def localize_exact(size,score_oracle):
    """Find a positive singleton using at most 1+ceil(log2(size)) score calls.

    Oracle(lo,hi) must return the exact additive score on the half-open range.
    The cost of that oracle and the arithmetic meaning of positivity are not
    established by this generic localization routine.
    """
    size=index(size)
    if size<1:
        raise ValueError('a nonempty finite domain is required')
    lo,hi=0,size
    score=Fraction(score_oracle(lo,hi))
    if score<=0:
        raise ValueError('a positive initial score is required')
    trace=[]
    while hi-lo>1:
        mid=(lo+hi)//2
        left=Fraction(score_oracle(lo,mid))
        trace.append(dict(lo=lo,hi=hi,mid=mid,parent=str(score),left=str(left)))
        if left>0:
            hi=mid
            score=left
        else:
            lo=mid
            score-=left
        assert score>0
    return dict(index=lo,singleton_score=score,trace=trace,calls=1+len(trace))


def certified_child(parent_lower,left_lower,left_upper):
    """Choose a positive child from valid bounds; None means refine precision."""
    parent_lower,left_lower,left_upper=map(Fraction,(parent_lower,left_lower,left_upper))
    if parent_lower<=0 or left_lower>left_upper:
        raise ValueError('invalid certificate bounds')
    if left_lower>0:
        return 'left',left_lower
    right_lower=parent_lower-left_upper
    if right_lower>0:
        return 'right',right_lower
    return None
