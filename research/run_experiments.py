"""Reproduce matched direct/sieved experiments; preserve every repeat and miss."""
import json
import platform
from pathlib import Path
import statistics
import sys
from time import perf_counter

# Permit `python research/run_experiments.py` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import sympy

from prime_ap import (WITNESSES, expected_probability, get_required_primorial,
                      is_prime, search, singular_series)


def direct_search(start, stop, k, d):
    began = perf_counter()
    matches, calls = [], 0
    for a in range(start, stop):
        for j in range(k):
            calls += 1
            if not is_prime(a + j*d):
                break
        else:
            matches.append(a)
    return dict(matches=matches, primality_tests=calls, seconds=perf_counter()-began)


def main():
    cases = [(7, 210, 999721467550000), (8, 210, 999721631450000),
             (9, 210, 10**15), (9, 223092870, 10**9), (28, 223092870, 10**15)]
    output = dict(python=sys.version, platform=platform.platform(), numpy=np.__version__,
                  sympy=sympy.__version__, repeats=3, raw_starts_per_case=100000,
                  witnesses=list(WITNESSES), cases=[])
    for k, d, a in cases:
        rows = []
        for repeat in range(3):
            # Alternate order to limit systematic cache/thermal bias.
            if repeat % 2:
                direct = direct_search(a, a+100000, k, d)
                sieved = search(a, a+100000, k, d).to_dict()
            else:
                sieved = search(a, a+100000, k, d).to_dict()
                direct = direct_search(a, a+100000, k, d)
            assert sieved['matches'] == direct['matches']
            for value in sieved['matches']:
                assert all(sympy.isprime(value+j*d) for j in range(k))
            rows.append(dict(direct=direct, sieved=sieved))
        ratio = statistics.median(r['direct']['seconds'] for r in rows) / statistics.median(
            r['sieved']['seconds'] for r in rows)
        output['cases'].append(dict(k=k, d=d, start=a, runs=rows, median_time_ratio=ratio))
    output['estimates'] = []
    for k, d, a in [(7,210,10**15),(8,210,10**15),(9,210,10**15),
                    (28,223092870,10**15),(28,223092870,10**9),
                    (28,get_required_primorial(31),10**9)]:
        probability = expected_probability(k,d,a)
        output['estimates'].append(dict(k=k,d=d,start=a,prime_bound=100000,
                                       singular_series=singular_series(k,d),
                                       probability=probability,expected_raw_starts=1/probability))
    target = Path(__file__).resolve().parents[1] / 'results' / 'comparison.json'
    target.write_text(json.dumps(output,indent=2)+'\n')
    for row in output['cases']:
        r=row['runs'][0]
        print(row['k'],row['d'],f"{row['median_time_ratio']:.1f}x",
              r['direct']['primality_tests'],r['sieved']['primality_tests'],r['sieved']['matches'])
    print(json.dumps(output['estimates'],indent=2))


if __name__ == '__main__':
    main()
