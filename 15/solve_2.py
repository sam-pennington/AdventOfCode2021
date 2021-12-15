from queue import PriorityQueue
import copy

DEBUG = False


def compare_all(block):
    expected = read_file_into_block('expected_all.txt')
    for i in range(len(block)):
        for c in range(len(block[i])):
            try:
                assert(expected[i][c] == block[i][c])
            except:
                print(f"(line, col): ({i},{c})")
                print(f"calculated: {block[i]}")
                print(f"expected:   {expected[i]}")
                raise Exception()


def compare_block(block):
    expected = read_file_into_block('expected_block.txt')
    for i in range(len(block)):
        for c in range(len(block[i])):
            try:
                assert(expected[i][c] == block[i][c])
            except:
                print(f"(line, col): ({i},{c})")
                print(f"calculated: {block[i]}")
                print(f"expected:   {expected[i]}")
                raise Exception()


def expand_right(block):
    r = []
    for row in block:
        working = copy.copy(row)
        for i in range(1, 5):
            incremented = [(x + (1 * i)) if (x + (1 * i))
                           < 10 else ((x + (1 * i)) - 9) for x in row]
            working = working + incremented
        r.append(working)
    return r


def increment_line(line):
    r = [(x + 1) if (x + 1) < 10 else ((x + 1) - 9) for x in line]
    return r


def expand_down(row):
    r = copy.copy(row)
    p = copy.copy(row)
    for _ in range(1, 5):
        l = []
        for row_line in p:
            l.append(increment_line(row_line))
        r = r + l
        p = copy.copy(l)
    return r


def expand(block):
    row = expand_right(block)
    if DEBUG:
        compare_block(block)
    final = expand_down(row)
    if DEBUG:
        compare_all(final)
    return final


def print_map(m):
    for l in m:
        s = "".join([str(x) for x in l])
        print(f"{s}")


def read_file_into_block(filename):
    block = None
    with open(filename, 'r') as f:
        block = [x.rstrip() for x in f.readlines()]
        block = [[int(y) for y in l] for l in block]
    return block


def load(filename):
    block = read_file_into_block(filename)
    expanded_map = expand(block)
    assert(len(block)*5 == (len(expanded_map)))
    assert(len(block[0])*5 == (len(expanded_map[0])))

    nodes = set()
    graph = dict()
    limitx = len(expanded_map[0])
    limity = len(expanded_map)
    for ridx, row in enumerate(expanded_map):
        for cidx, _ in enumerate(row):
            nodes.add((cidx, ridx))
            graph[(cidx, ridx)] = dict()
            neighbours = ((cidx, ridx+1), (cidx, ridx-1),
                          (cidx+1, ridx), (cidx-1, ridx))
            for n in neighbours:
                if n[0] < 0 or n[0] > limitx - 1 or n[1] < 0 or n[1] > limity - 1:
                    continue
                graph[(cidx, ridx)][n] = expanded_map[n[1]][n[0]]
    return nodes, graph, (limitx-1, limity-1)


def dijkstra(graph, nodes, start):
    shortest_path = {n: float('inf') for n in nodes}
    shortest_path[start] = 0

    priority = PriorityQueue()
    priority.put((0, start))

    visited = set()

    while not priority.empty():
        _, current_vertex = priority.get()
        visited.add(current_vertex)
        for neighbor in graph[current_vertex]:
            distance = graph[current_vertex][neighbor]
            if neighbor not in visited:
                old_cost = shortest_path[neighbor]
                new_cost = shortest_path[current_vertex] + distance
                if new_cost < old_cost:
                    priority.put((new_cost, neighbor))
                    shortest_path[neighbor] = new_cost
    return shortest_path


def run(filename):
    nodes, graph, end = load(filename)
    shortest = dijkstra(graph, nodes, (0, 0))
    print(f"{shortest[end]}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
