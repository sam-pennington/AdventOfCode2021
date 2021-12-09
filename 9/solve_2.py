from functools import reduce


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


def calculate_basins(sinks, grid):
    stack = []
    basins = []
    basin = []
    for start in sinks:
        stack = [start]
        basin = []
        seen = set()
        while len(stack) > 0:
            current_coord = stack.pop()
            if current_coord not in seen:
                seen.add(current_coord)
                if current_coord in grid:
                    current = grid[current_coord]
                    if current != 9:
                        basin.append(current)
                        x, y = current_coord
                        comps = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                        stack = stack + comps
        basins.append(basin)
    return basins


def run(filename):
    content = load(filename)
    grid = make_grid(content)
    suitable_coords = scan_grid(grid)
    basins = calculate_basins(suitable_coords, grid)
    biggest = sorted([len(b) for b in basins], reverse=True)[:3]
    result = reduce((lambda x, y: x * y), biggest)
    print(f"{result}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
