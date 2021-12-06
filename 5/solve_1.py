import itertools


def parse_point(point):
    x, y = point.split(",")
    return (int(x), int(y))


def parse_points(points):
    start_point = parse_point(points[0])
    end_point = parse_point(points[1])
    return (start_point, end_point)


def parse_line(line):
    points = line.split(" -> ")
    return parse_points(points)


def parse_lines(lines):
    return [parse_line(l) for l in lines]


def load_content(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return [line.rstrip() for line in lines if len(line.rstrip()) > 0]


def not_diagonal(line):
    start, end = line
    return (start[0] == end[0]) or (start[1] == end[1])


def expand_line(line):
    start, end = line
    ret = []
    if start[0] == end[0]:
        x = start[0]
        y_delta = abs(start[1] - end[1])
        for i in range(y_delta + 1):
            ret.append((x, min(start[1], end[1]) + i))
    elif start[1] == end[1]:
        y = start[1]
        x_delta = abs(start[0] - end[0])
        for i in range(x_delta + 1):
            ret.append((min(start[0], end[0]) + i, y))
    else:
        raise NotImplementedError()
    return ret


def expand(filtered):
    expanded = []
    for l in filtered:
        expanded = expanded + expand_line(l)
    return expanded


def crossing_count(sorted_points):
    crossing = 0
    for _, group in itertools.groupby(sorted_points, key=lambda tup: (tup[0], tup[1])):
        if len(list(group)) > 1:
            crossing = crossing + 1
    return crossing


def run(filename):
    content = load_content(filename)
    parsed = parse_lines(content)
    filtered = list(filter(not_diagonal, parsed))
    expanded = expand(filtered)
    sorted_points = sorted(expanded, key=lambda tup: (tup[0], tup[1]))
    print(f"{crossing_count(sorted_points)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
