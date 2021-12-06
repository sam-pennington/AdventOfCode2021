def evaluate_day(values):
    ret = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0
    }
    for i in range(8, -1, -1):
        if i == 0:
            ret[8] = values[0]
            ret[6] = ret[6] + values[0]
        else:
            ret[i - 1] = values[i]
    return ret


def load(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = [x.rstrip() for x in f.readlines()]
    ret = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0
    }
    for l in lines:
        for value in [int(v) for v in l.split(",")]:
            ret[value] = ret[value] + 1
    return ret


def run(filename):
    initial_values = load(filename)
    for _ in range(0, 256):
        initial_values = evaluate_day(initial_values)
    total = sum(initial_values.values())
    print(f"{total}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
