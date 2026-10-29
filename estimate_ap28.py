"""Conjectural prime-tuple density using the actual logarithm of every term."""
import argparse

from prime_ap import expected_probability, get_required_primorial, singular_series


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--k',type=int,default=28)
    parser.add_argument('--start',type=int,default=10**15)
    parser.add_argument('--difference',type=int)
    parser.add_argument('--starts-per-second',type=float,
                        help='measured raw-start rate for this exact algorithm and tuple')
    args=parser.parse_args(argv)
    try:
        d=get_required_primorial(args.k) if args.difference is None else args.difference
        probability=expected_probability(args.k,d,args.start)
    except ValueError as error:
        parser.error(str(error))
    print(f'Step d: {d:,}; span: {(args.k-1)*d:,}')
    print(f'Partial singular series (primes <= 100000): {singular_series(args.k,d):.6e}')
    print(f'Conjectured probability per raw start near the specified start: {probability:.6e}')
    if probability == 0:
        print('Local prime obstruction: no all-large prime progression for this difference.')
        return 0
    print(f'Local reciprocal intensity (not a guarantee): {1/probability:.6e} raw starts')
    if args.starts_per_second is not None:
        if args.starts_per_second <= 0:
            parser.error('--starts-per-second must be positive')
        print(f'Local reciprocal rate: {1/probability/args.starts_per_second:.6e} seconds')
    print('This local estimate cannot be extrapolated unchanged over enormous intervals.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
