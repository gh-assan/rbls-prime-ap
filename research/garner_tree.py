"""Experiment for idea 25 of the brainstorm: Garner tree search with box pruning.

In mixed radix a = v1 + v2*q1 + v3*q1*q2 + ..., the condition at the i-th prime
involves only the first i digits (Garner's algorithm). The tree fixes one digit
per prime, keeps only residues allowed at that prime, and prunes a class once
it has no representative in the search window. At a switch depth the classes
are expanded into window representatives, which are filtered by the remaining
primes with early exit. The wheel is the natural order switched at the largest
modulus not exceeding the window.

Work counts every generated child, every representative and every filter
check. Kept classes and window survivors per level are exact: below the window
size every admissible class is kept; above it a kept class holds exactly one
window cell, so kept classes equal surviving cells. `explicit_tree` runs the
tree itself for cross-checking. Small analog: AP-10 with difference 210.
"""
import json
import math
import random
from pathlib import Path

import numpy as np
from sympy import primerange


K = 10
D = 210
START = 10**9
LENGTH = 2**22


def good_residues(p):
    bad = {(-D*j) % p for j in range(K)}
    return np.array([x for x in range(p) if x not in bad], dtype=np.int64)


def prefix_survivors(order, start=START, length=LENGTH):
    """S_i: window cells passing the first i primes of the order, i = 0..n."""
    cells = start + np.arange(length, dtype=np.int64)
    counts = [length]
    for p in order:
        allowed = np.zeros(p, bool)
        allowed[good_residues(p)] = True
        cells = cells[allowed[cells % p]]
        counts.append(len(cells))
    return counts


def tree_work(order, survivors, length=LENGTH):
    """Work for every switch depth, from exact level counts.

    generated_i = kept_{i-1} * |G_i|, kept_i = prod|G| while the modulus is at
    most the window, else S_i. Switching at depth i costs the generated
    children so far, S_i representatives, and sum_{j>=i} S_j filter checks.
    """
    n = len(order)
    modulus, kept, generated = 1, 1, 0
    filter_tail = [0]*(n + 1)
    for i in range(n - 1, -1, -1):
        filter_tail[i] = filter_tail[i + 1] + survivors[i]
    rows = [{"switch": 0, "modulus": 1, "generated": 0,
             "work": survivors[0] + filter_tail[0]}]
    for i, p in enumerate(order, start=1):
        g = len(good_residues(p))
        generated += kept*g
        modulus *= p
        kept = kept*g if modulus <= length else survivors[i]
        rows.append({"switch": i, "modulus": modulus, "generated": generated,
                     "kept": kept, "work": generated + survivors[i] + filter_tail[i]})
    return rows


def explicit_tree(order, switch, start=START, length=LENGTH):
    """Run the tree directly; returns (generated children, survivors)."""
    classes, modulus, generated = [0], 1, 0
    for p in order[:switch]:
        good = good_residues(p)
        inv = pow(modulus, -1, p)
        nxt = []
        for c in classes:
            for g in good:
                generated += 1
                child = c + modulus*((int(g) - c)*inv % p)
                if modulus*p > length:
                    first = child + modulus*p*((start - child + modulus*p - 1)//(modulus*p))
                    if first >= start + length:
                        continue
                nxt.append(child)
        classes, modulus = nxt, modulus*p
    cells = []
    for c in classes:
        first = c + modulus*((start - c + modulus - 1)//modulus)
        cells.extend(range(first, start + length, modulus))
    cells = np.array(cells, dtype=np.int64)
    for p in order[switch:]:
        allowed = np.zeros(p, bool)
        allowed[good_residues(p)] = True
        cells = cells[allowed[cells % p]]
    return generated, len(cells)


def orders(primes, seed=0):
    small = [p for p in primes if D % p == 0]
    big = [p for p in primes if D % p]
    shuffled = primes[:]
    random.Random(seed).shuffle(shuffled)
    survival = sorted(primes, key=lambda p: (len(good_residues(p))/p, p))
    return {"ascending": primes[:], "by_survival": survival, "big_first": big + small,
            "descending": big[::-1] + small[::-1], "random": shuffled}


def wheel_depth(order, length=LENGTH):
    prod, depth = 1, 0
    for p in order:
        if prod*p > length:
            break
        prod *= p
        depth += 1
    return depth


def run():
    report = {"k": K, "difference": D, "start": START, "length": LENGTH,
              "status": "Exact work counts on a small analog; no AP28 and no proof supplied.",
              "rows": []}
    for y in (23, 47, 97, 199, 541):
        primes = [2, 3, 5, 7] + list(primerange(11, y + 1))
        base_rows = tree_work(primes, prefix_survivors(primes))
        wheel = base_rows[wheel_depth(primes)]
        row = {"y": y, "survivors": prefix_survivors(primes)[-1], "wheel": wheel, "orders": {}}
        for name, order in orders(primes).items():
            surv = prefix_survivors(order)
            rows = tree_work(order, surv)
            best = min(rows, key=lambda r: r["work"])
            # Once the modulus exceeds the window, one more level changes the
            # work by exactly S_i*(|G_p| - 2) + S_{i+1}.
            identity = all(
                rows[i + 1]["work"] - rows[i]["work"]
                == surv[i]*(len(good_residues(order[i])) - 2) + surv[i + 1]
                for i in range(1, len(order)) if rows[i]["modulus"] > LENGTH)
            row["orders"][name] = {
                "best": best, "best_over_wheel": best["work"]/wheel["work"],
                "beyond_window_identity_holds": identity,
            }
        row["wheel_work_per_survivor"] = wheel["work"]/max(1, row["survivors"])
        report["rows"].append(row)
    return report


if __name__ == "__main__":
    data = run()
    out = Path(__file__).resolve().parents[1] / "results" / "garner-tree.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    for row in data["rows"]:
        print(row["y"], "survivors", row["survivors"], "wheel work", row["wheel"]["work"],
              {k: (v["best"]["switch"], v["best"]["work"], round(v["best_over_wheel"], 3))
               for k, v in row["orders"].items()})
