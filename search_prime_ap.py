"""Portable CLI: exact AP search, with JSON output for successes and misses."""
import argparse
import json
from pathlib import Path

from prime_ap import search


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--count', type=int, required=True, help='number of raw starts')
    parser.add_argument('--k', type=int, default=9)
    parser.add_argument('--difference', type=int, help='default: product of primes <= k')
    parser.add_argument('--sieve-bound', type=int, default=1000)
    parser.add_argument('--segment-size', type=int, default=1_000_000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        result = search(args.start, args.start + args.count, args.k, args.difference,
                        sieve_bound=args.sieve_bound, segment_size=args.segment_size)
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    payload = json.dumps(result.to_dict(), indent=2)
    if args.output:
        args.output.write_text(payload + '\n', encoding='utf-8')
    print(payload)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
