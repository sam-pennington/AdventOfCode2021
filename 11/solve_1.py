import copy
import time

OKGREEN = '\033[92m'
ENDC = '\033[0m'


def print_cave_emojis(cave, clear=True):
    def octopus(c):
        if c != 0:
            return '🐙'
        return '✨'

    if clear:
        print("\033[H\033[J", end="")
    for i in range(10):
        col_out = "".join([octopus(cave[(i, x)]) for x in range(10)])
        print(f"{col_out}")

    time.sleep(3)


def print_cave(cave, clear=False):
    if clear:
        print("\033[H\033[J", end="")
    for i in range(10):
        cols = [str(cave[(i, x)]) for x in range(10)]
        col_out = "".join(cols).replace("0", OKGREEN + '0' + ENDC)
        print(f"{col_out}")


def load(filename):
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
        return lines


def step_cave(cave):
    ret = copy.copy(cave)
    for r in range(10):
        for c in range(10):
            ret[(r, c)] = ret[(r, c)] + 1
    flashed = False
    first = True
    flashed_octopuses = set()
    propagations = []
    while flashed or first:
        flashed = False
        first = False
        for prop in propagations:
            if prop not in flashed_octopuses:
                ret[prop] = ret[prop] + 1
        propagations = []
        for r in range(10):
            for c in range(10):
                if (r, c) not in flashed_octopuses:
                    if ret[(r, c)] > 9:
                        flashed = True
                        ret[(r, c)] = 0
                        flashed_octopuses.add((r, c))
                        propagation = [(r-1, c), (r+1, c), (r, c-1), (r, c+1),
                                       (r-1, c+1), (r-1, c-1), (r+1, c-1), (r+1, c+1)]
                        propagation = [
                            x for x in propagation if x[0] >= 0 and x[1] >= 0 and x[0] < 10 and x[1] < 10
                        ]
                        propagations = propagations + propagation
    return ret


def simulate_n_step(base_cave, n):
    start = copy.copy(base_cave)
    for _ in range(n):
        start = step_cave(start)
    return start


def parse_cave(content):
    cave = dict()
    for ridx, row in enumerate(content):
        for cidx, col in enumerate(row):
            cave[(ridx, cidx)] = int(col)
    return cave


def count_flashes(cave):
    zeros = [x for x in cave.values() if x == 0]
    return len(zeros)


def run(filename):
    content = load(filename)
    cave = parse_cave(content)
    flashes = 0
    for i in range(101):
        local = simulate_n_step(cave, i)
        flashes = flashes + count_flashes(local)
    print(f"{flashes}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
