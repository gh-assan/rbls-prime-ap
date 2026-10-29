"""Rank differences by conjectured hits per second of measured pilot search."""
import argparse
import json
from pathlib import Path
from time import perf_counter

from prime_ap import expected_probability, search, survivor_density


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--k', type=int, default=28)
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--differences', type=int, nargs='+', required=True)
    parser.add_argument('--pilot-count', type=int, default=1_000_000)
    parser.add_argument('--sieve-bound', type=int, default=1000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    rows = []
    for d in dict.fromkeys(args.differences):
        began = perf_counter()
        try:
            pilot = search(args.start, args.start+args.pilot_count, args.k, d,
                           sieve_bound=args.sieve_bound)
            # Include wheel and sieve construction in pilot wall time.
            elapsed = perf_counter() - began
            probability = expected_probability(args.k, d, args.start)
        except (ValueError, TypeError) as error:
            parser.error(str(error))
        density = survivor_density(args.k, d, args.sieve_bound)
        rows.append(dict(d=d, probability_per_raw_start=probability,
                         sieve_survival_fraction=density,
                         probability_per_survivor=probability/density if density else 0.0,
                         pilot_seconds=elapsed, pilot=pilot.to_dict(),
                         estimated_hits_per_second=probability*args.pilot_count/elapsed))
    rows.sort(key=lambda r:r['estimated_hits_per_second'],reverse=True)
    output = dict(k=args.k, start=args.start, sieve_bound=args.sieve_bound,
                  warning='Heuristic ranking from a short pilot; not a discovery guarantee. '
                          'Local density changes over large search ranges. Repeat and scale pilots.',
                  ranked_differences=rows)
    payload=json.dumps(output,indent=2)
    if args.output:
        args.output.write_text(payload+'\n',encoding='utf-8')
    print(payload)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
