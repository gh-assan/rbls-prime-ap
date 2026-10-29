"""Reproduce the numerical tables in the completion paper, including model labels."""
import json
from math import exp, log, prod
from pathlib import Path
import sys

import numpy as np
from sympy import primerange

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prime_ap import singular_series
from research.completion_certificates import finite_certificate, model_certificate


def height_model(X,order,beta,k=28,D=223092870):
    """Gauss-Legendre calculation of an open-triangle heuristic integral.

    The integration triangle is a>=29, m>=1, a+(k-1)*D*m<=X.
    A convergence comparison is not a certified quadrature error bound.
    """
    nodes,weights=np.polynomial.legendre.leggauss(order)
    x=(nodes+1)/2
    w=weights/2
    t=x[:,None]
    z=x[None,:]
    A,W=29,(k-1)*D
    H=X-A-W
    if H<=0:
        return 0.0
    denominator=np.ones((order,order))
    for j in range(k):
        denominator *= np.log(A+j*D+float(H)*t*(z+j/(k-1)*(1-z)))
    integral=float(np.sum(w[:,None]*w[None,:]*t/denominator))
    return beta*H**2/W*integral


def analysis():
    D,k=223092870,28
    phi=prod(p-1 for p in primerange(2,29))
    beta=singular_series(k-1,D)*D/phi
    height=[]
    for X in [10**15,10**17,10**18,2*10**18,5*10**18,2**64-1]:
        height.append(dict(X=X,integer_pair_volume=(X-29-(k-1)*D)**2/(2*(k-1)*D),
                           equal_log_model=beta*(X-29-(k-1)*D)**2/(2*(k-1)*D)/log(X)**k,
                           integral_model_by_quadrature={n:height_model(X,n,beta) for n in [32,64,128,256]}))
    roughness=[]
    for theta in [1/3,.4,.45,.48,.49,.495]:
        u=1/theta
        q=1/(1+log(u-1))
        roughness.append(dict(theta=theta,single_integer_asymptotic_prime_fraction=q,
                              independent_model_expected_defects=k*(1-q),
                              independent_model_zero_defects=q**k))
    return dict(status='Certificates are exact; roughness/height tables are calibration models, not AP28 counts.',
                prime_product_bound=100000,beta_partial=beta,
                arithmetic_AP5=finite_certificate(),model_AP28=model_certificate(),
                single_integer_roughness_calibration=roughness,
                first_moment_threshold_in_independent_model=1/(1+exp(1/27)),
                fifth_degree_example_theta=1/(1+exp(1/9)),height_models=height)


if __name__ == '__main__':
    target=Path(__file__).resolve().parents[1]/'results'/'completion-analysis.json'
    result=analysis()
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
