from queue import PriorityQueue


def load(filename):
    lines = None
    with open(filename, 'r') as f:
        lines = [x.rstrip() for x in f.readlines()]
        lines = [[int(y) for y in l] for l in lines]
    nodes = set()
    graph = dict()
    limitx = len(lines[0])
    limity = len(lines)
    for ridx, row in enumerate(lines):
        for cidx, _ in enumerate(row):
            nodes.add((cidx, ridx))
            graph[(cidx, ridx)] = dict()
            neighbours = ((cidx, ridx+1), (cidx, ridx-1),
                          (cidx+1, ridx), (cidx-1, ridx))
            for n in neighbours:
                if n[0] < 0 or n[0] > limitx - 1 or n[1] < 0 or n[1] > limity - 1:
                    continue
                graph[(cidx, ridx)][n] = lines[n[1]][n[0]]
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
