"""Experiment C2 / idea 7 of the brainstorm: Meissel-Lehmer for patterns.

Phi(x, S) counts t in [0, x) such that, for every sieve prime q, the residue
t mod q avoids the bad set S_q. A pattern t+o_1, ..., t+o_k starts with
S_q = {-o_i mod q}. Peeling the largest sieve prime p gives the exact identity

    Phi(x, S) = Phi(x, S without p) - sum_{r in S_p} Phi(ceil((x-r)/p), S^(p,r)),

where t = p*s + r and S^(p,r)_q = {(b-r)/p mod q : b in S_q}. For a single
form t, S_q = {0} is fixed by every substitution, so subproblems collapse to
(floor(x/n), number of primes): this is Legendre/Meissel memoization. The
experiment measures how many distinct subproblems the same exact recursion
needs for patterns of two or more forms.
"""
import json
import math
import sys
from pathlib import Path

from sympy import primerange


PATTERNS = {
    "primes": (0,),
    "twins": (0, 2),
    "ap3_d6": (0, 6, 12),
    "ap5_d30": (0, 30, 60, 90, 120),
}
LEAF = 16


class PatternCounter:
    def __init__(self, offsets, primes):
        self.primes = tuple(primes)
        self.states = {}
        self.state_list = []
        self.transforms = {}
        self.memo = {}
        self.calls = 0
        self.leaf_cells = 0
        root = tuple(tuple(sorted({(-o) % q for o in offsets})) for q in self.primes)
        self.root = self.intern(root)

    def intern(self, state):
        sid = self.states.get(state)
        if sid is None:
            sid = len(self.state_list)
            self.states[state] = sid
            self.state_list.append(state)
        return sid

    def child(self, sid, r):
        """State after t = p*s + r for the largest prime p of the state."""
        key = (sid, r)
        if key not in self.transforms:
            state = self.state_list[sid]
            p = self.primes[len(state) - 1]
            inv = [pow(p, -1, q) for q in self.primes[:len(state) - 1]]
            new = tuple(tuple(sorted({(b - r)*i % q for b in bad}))
                        for bad, q, i in zip(state[:-1], self.primes, inv))
            self.transforms[key] = self.intern(new)
        return self.transforms[key]

    def drop(self, sid):
        key = (sid, None)
        if key not in self.transforms:
            self.transforms[key] = self.intern(self.state_list[sid][:-1])
        return self.transforms[key]

    def count(self, x, sid):
        self.calls += 1
        if x <= 0:
            return 0
        state = self.state_list[sid]
        if not state:
            return x
        if x <= LEAF:
            self.leaf_cells += x
            return sum(all(t % q not in bad for bad, q in zip(state, self.primes))
                       for t in range(x))
        key = (x, sid)
        if key in self.memo:
            return self.memo[key]
        p = self.primes[len(state) - 1]
        bad = state[-1]
        if len(bad) == p:
            value = 0
        else:
            value = self.count(x, self.drop(sid))
            for r in bad:
                value -= self.count(-((r - x)//p), self.child(sid, r))
        self.memo[key] = value
        return value


def direct_count(offsets, primes, x):
    sieve = bytearray([1])*x
    for q in primes:
        for o in offsets:
            start = (-o) % q
            sieve[start::q] = bytes(len(range(start, x, q)))
    return sum(sieve)


def measure(name, x):
    offsets = PATTERNS[name]
    primes = list(primerange(2, math.isqrt(x + max(offsets)) + 1))
    counter = PatternCounter(offsets, primes)
    value = counter.count(x, counter.root)
    return {
        "pattern": name, "x": x, "sieve_primes": len(primes), "count": value,
        "direct_count": direct_count(offsets, primes, x),
        "calls": counter.calls, "distinct_subproblems": len(counter.memo),
        "distinct_states": len(counter.state_list), "leaf_cells": counter.leaf_cells,
    }


def growth_exponent(rows):
    """Least-squares slope of log(distinct subproblems) against log(x)."""
    xs = [math.log(r["x"]) for r in rows]
    ys = [math.log(max(1, r["distinct_subproblems"])) for r in rows]
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    return sum((a - mx)*(b - my) for a, b in zip(xs, ys))/sum((a - mx)**2 for a in xs)


def run():
    sys.setrecursionlimit(100000)
    sizes = {"primes": range(10, 25), "twins": range(10, 19),
             "ap3_d6": range(10, 18), "ap5_d30": range(10, 17)}
    report = {"status": "Exact recursion measured; no sublinear pattern counter and no AP28 supplied.",
              "leaf_size": LEAF, "patterns": {}}
    for name, exps in sizes.items():
        rows = [measure(name, 2**e) for e in exps]
        if any(r["count"] != r["direct_count"] for r in rows):
            raise AssertionError(f"{name}: recursion disagrees with direct sieve")
        report["patterns"][name] = {"offsets": PATTERNS[name], "rows": rows,
                                    "subproblem_growth_exponent": growth_exponent(rows[-4:])}
    return report


if __name__ == "__main__":
    data = run()
    out = Path(__file__).resolve().parents[1] / "results" / "pattern-counting.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    for name, block in data["patterns"].items():
        last = block["rows"][-1]
        print(name, "x =", last["x"], "subproblems =", last["distinct_subproblems"],
              "states =", last["distinct_states"], "exponent = %.3f" % block["subproblem_growth_exponent"])
