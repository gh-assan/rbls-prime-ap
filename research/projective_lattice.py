"""Exact certificates for a proposed two-parameter AP search.

This constructs congruence lattices. It is not an AP-28 discovery algorithm
with an established practical success rate.
"""
from math import gcd, prod
from sympy import Matrix, isprime
from sympy.ntheory.modular import crt


def allowed_directions(k, D, p):
    """Slopes a/m in F_p; None represents the direction m=0."""
    if k < 2 or not isprime(p) or D % p == 0 or p <= k:
        raise ValueError('require prime p > k, p not dividing D, and k >= 2')
    return tuple((D*s) % p for s in range(1, p-k+1)) + (None,)


def cell_basis(k, D, choices):
    """Rows span (a,m) satisfying chosen finite/infinite slope conditions.

    Origin exclusions are deliberately separate from the linear lattice.
    """
    if D < 1 or k < 2:
        raise ValueError('require D > 0 and k >= 2')
    finite, infinite = [], []
    for p, slope in sorted(choices.items()):
        if slope not in allowed_directions(k,D,p):
            raise ValueError(f'direction {slope} is forbidden modulo {p}')
        (infinite if slope is None else finite).append((p,slope))
    F=prod(p for p,_ in finite)
    I=prod(p for p,_ in infinite)
    c=int(crt([p for p,_ in finite],[s for _,s in finite])[0]) if finite else 0
    return Matrix([[F,0],[c*I,I]])


def belongs_to_cell(a,m,k,D,choices):
    """Check positivity, primitive coordinates, and every local direction."""
    if a <= k or m <= 0 or gcd(a,D*m) != 1:
        return False
    for p,slope in choices.items():
        if slope is None:
            if m % p != 0 or a % p == 0:
                return False
        elif m % p == 0 or (a-slope*m) % p != 0:
            return False
    return True


def reduced_basis(k,D,choices):
    """Integer weighting: the second coordinate is the total span, (k-1)*D*m."""
    weight=(k-1)*D
    ordinary=cell_basis(k,D,choices)
    weighted=ordinary*Matrix([[1,0],[0,weight]])
    reduced=weighted.lll()
    return Matrix([[int(row[0]),int(row[1])//weight] for row in reduced.tolist()])


def certificate():
    k,D=28,223092870
    counts=[]
    for p in [29,31,37,41,43]:
        count=sum(all((a+j*D*m)%p for j in range(k))
                  for a in range(p) for m in range(p))
        assert count==(p-1)*(p-k+1)
        counts.append(dict(prime=p,good_pairs=count,allowed_directions=p+1-k))
    choices={29:None,31:D%31,37:(2*D)%37,41:(3*D)%41}
    basis=cell_basis(k,D,choices)
    reduced=reduced_basis(k,D,choices)
    assert abs(int(basis.det())) == prod(choices)
    assert abs(int(reduced.det())) == prod(choices)
    # Recover the unimodular transformation; this checks full lattice equality.
    transform=reduced*basis.inv()
    assert all(x.q==1 for x in transform)
    assert abs(int(transform.det()))==1
    return dict(k=k,D=D,counts=counts,choices=choices,basis=basis.tolist(),
                reduced_basis=reduced.tolist(),determinant=abs(int(basis.det())))


if __name__ == '__main__':
    import json
    print(json.dumps(certificate(),default=int,indent=2))
