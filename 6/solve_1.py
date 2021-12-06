def evaluate_day(values):
    ret = []
    for v in values:
        if v == 0:
            ret.append(6)
            ret.append(8)
            continue
        ret.append(v - 1)
    return ret


def load(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = [x.rstrip() for x in f.readlines()]
    ret = []
    for l in lines:
        ret = ret + [int(v) for v in l.split(",")]
    return ret


def run(filename):
    initial_values = load(filename)
    for _ in range(0, 256):
        initial_values = evaluate_day(initial_values)
    print(f"{len(initial_values)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
