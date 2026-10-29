"""Check all nonempty fifth-order intersections in the existing AP-7 family."""
from itertools import combinations
import json
from math import comb,isqrt,prod
from pathlib import Path
import sys

from sympy import primerange
from sympy.ntheory.modular import crt

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.primitive_tail_decoding import decode_tail_intersection
from research.primitive_cells import primitive_count


def certificate():
    k,D,B,X,cap=7,210,29,20000,10
    small=tuple(primerange(2,B+1));tail=tuple(primerange(B+1,isqrt(X)+1))
    catalog=[];histogram=[0]*(k+1)
    for m in range(1,cap+1):
        for a in range(B+1,X-(k-1)*D*m+1):
            terms=[a+j*D*m for j in range(k)]
            if any(n%p==0 for n in terms for p in small):
                continue
            tags=[(j,int(q)) for j,n in enumerate(terms) for q in tail if n%q==0 and q*q<=n]
            histogram[len(tags)]+=1
            for group in combinations(tags,5):
                decoded=decode_tail_intersection(k,D,B+1,X,group,sieve_bound=B,m_cap=cap)
                assert decoded==(a,m)
                catalog.append((a,m,group))
    assert len(catalog)==sum(count*comb(c,5) for c,count in enumerate(histogram) if c>=5)==66
    examples=[]
    # Independently compare the existing Möbius/floor-sum counter on three cells.
    for a,m,tags in catalog[:3]:
        modulus=prod(q for j,q in tags)
        residue=int(crt([q for j,q in tags],[-j*D for j,q in tags])[0])
        number=primitive_count(modulus,1,residue,B+1,(k-1)*D,X,D,
                               [(j*D,q*q) for j,q in tags],m_cap=cap)
        assert number==1
        examples.append(dict(a=a,m=m,tags=tags,modulus=modulus,residue=residue,
                             independent_primitive_count=number))
    chosen=[(0,41),(1,73),(2,67),(3,101),(4,79)]
    assert decode_tail_intersection(k,D,B+1,X,chosen,sieve_bound=B,m_cap=cap)==(9143,2)
    return dict(status='Exact local decoding, not an AP28 positive score or a prime-label enumeration method.',
                family=dict(k=k,D=D,B=B,X=X,m_cap=cap),defect_histogram=histogram,
                fifth_order_intersections=len(catalog),distinct_points=len({(a,m) for a,m,tags in catalog}),
                coverage='catalog obtained from complete direct enumeration of this small rough family',
                examples=examples,
                nontrivial_denominator_example=dict(a=9143,m=2,tags=chosen,
                    modulus=1600036849,residue=800022996,continued_fraction_numerator=1),
                uint64_proof=dict(X_max=2**64-1,cube_root_integer_upper=2642246,
                    W=27*223092870,W_exceeds_twice_cube_upper=27*223092870>2*2642246))


if __name__=='__main__':
    result=certificate()
    (Path(__file__).resolve().parents[1]/'results'/'tail-decoding-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
