import copy

START = 'start'
END = 'end'


def load(filename):
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
        return lines


def parse_lines(lines):
    ret = dict()
    for l in lines:
        start, end = l.split('-')
        if start not in ret:
            ret[start] = [end]
        else:
            ret[start] = ret[start] + [end]

        if end not in ret:
            ret[end] = [start]
        else:
            ret[end] = ret[end] + [start]
    return ret


def dfs(graph):
    start_adjacents = graph[START]
    paths = []
    path = [START]
    for adj in start_adjacents:
        dfs_iterate(graph, adj, copy.copy(path), paths)
    return paths


def dfs_iterate(graph, adj, path, paths):
    path.append(adj)
    if adj == END:
        paths.append(path)
        return
    adjacents = filter_adjacents(graph[adj], path)
    for nadj in adjacents:
        dfs_iterate(graph, nadj, copy.copy(path), paths)


def filter_adjacents(adjacents, current_path):
    adjacents = [x for x in adjacents if x != START]
    double_used = [x for x in current_path if x.islower()]
    double_used = len(set(double_used)) != len(double_used)
    adjacents = [
        x for x in adjacents if x.isupper() or (
            x not in current_path
            or
            not double_used
        )
    ]
    return adjacents


def run(filename):
    content = load(filename)
    graph = parse_lines(content)
    results = dfs(graph)
    print(f"{len(results)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
