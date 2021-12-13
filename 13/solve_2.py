import copy


def load(filename):
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    points = []
    folds = []
    for l in lines:
        if len(l) == 0:
            continue
        if l.startswith('fold'):
            _, _, value = l.split(" ")
            axis, amount = value.split("=")
            if ('y' == axis):
                folds.append((None, int(amount)))
            else:
                folds.append((int(amount), None))
        else:
            x, y = l.split(',')
            points.append((int(x), int(y)))

    return folds, points


def fold_horizontal(grid, y):
    ret = copy.copy(grid)
    top = ret[:y]
    bottom = reversed(ret[y+1:])
    for rdx, r in enumerate(bottom):
        for cdx, c in enumerate(r):
            top[rdx][cdx] = c if c else top[rdx][cdx]
    return top


def fold_vertical(grid, x):
    ret = copy.copy(grid)
    left = [r[:x] for r in ret]
    right = [reversed(r[x+1:]) for r in grid]
    for rdx, r in enumerate(right):
        for cdx, c in enumerate(r):
            left[rdx][cdx] = c if c else left[rdx][cdx]
    return left


def max_column(points):
    xs = [x[0] for x in points]
    return max(xs)


def max_rows(points):
    ys = [x[1] for x in points]
    return max(ys)


def parse_points(points):
    mr = max_rows(points)
    mc = max_column(points)
    grid = [[False for x in range(mc+1)] for y in range(mr+1)]

    for p in points:
        col, row = p
        grid[row][col] = True

    return grid


def print_grid(grid):
    for l in grid:
        row = "".join([' ' if not x else '#' for x in l])
        print(f"{row}")


def count_dots(grid):
    dots = 0
    for r in grid:
        for c in r:
            dots = dots + (1 if c else 0)
    return dots


def do_fold(grid, fold):
    if fold[0] is not None:
        return fold_vertical(grid, fold[0])
    else:
        assert(fold[1] is not None)
        return fold_horizontal(grid, fold[1])


def run(filename):
    folds, points = load(filename)
    grid = parse_points(points)
    for fold in folds:
        grid = do_fold(grid, fold)
    print_grid(grid)


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
