
def make_grid(content):
    grid = {}
    for row_idx, row in enumerate(content):
        for col_idx, col in enumerate(row):
            grid[(row_idx, col_idx)] = int(col)
    return grid


def load(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [x.rstrip() for x in lines]
        return lines


def scan_grid(grid):
    suitable = []
    for cell in grid.keys():
        x, y = cell
        comps = ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
        comparison_results = []
        for comp in comps:
            if comp in grid:
                comparison_results.append(grid[cell] < grid[comp])
        if all(comparison_results):
            suitable.append(cell)
    return suitable


def run(filename):
    content = load(filename)
    grid = make_grid(content)
    suitable_coords = scan_grid(grid)
    risk_levels = [grid[x] + 1 for x in suitable_coords]
    print(f"risk levels: {risk_levels}")
    print(f"sum: {sum(risk_levels)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
