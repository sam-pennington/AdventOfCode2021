def categorise(code):
    l = len(code)
    if l == 2:
        return 1
    elif l == 4:
        return 4
    elif l == 3:
        return 7
    elif l == 7:
        return 8
    else:
        # todo
        return -1


def parse(line):
    inputs, outputs = line.split(" | ")
    inputs = inputs.split(" ")
    outputs = outputs.split(" ")
    return (inputs, outputs)


def load_and_parse(filename):
    lines = None
    with open(filename, 'r') as f:
        lines = f.readlines()
    parsed = [parse(l.rstrip()) for l in lines]
    return parsed


def run(filename):
    parsed = load_and_parse(filename)
    categorised = []
    for _, outputs in parsed:
        categorised = categorised + \
            [x for x in outputs if categorise(x) in (1, 4, 7, 8)]
    print(f"{len(categorised)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
