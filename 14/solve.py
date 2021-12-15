import copy


def load(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = [x.rstrip() for x in f.readlines()]
    template = lines[0]
    steps = dict()
    for s in lines[2:]:
        key, val = s.split(' -> ')
        key = (key[0], key[1])
        steps[key] = val
    return template, steps


def evolve(template, steps, iterations):
    iteration = dict()
    for i in range(len(template)-1):
        key = (template[i], template[i+1])
        if key not in iteration:
            iteration[key] = 1
        else:
            iteration[key] = iteration[key] + 1
    scoring = None
    for i in range(iterations):
        working = dict()
        scoring = {}
        scoring[template[-1]] = 1
        for k in iteration:
            if k in steps:
                new_pairs = ((k[0], steps[k]), (steps[k], k[1]))
                if k[0] not in scoring:
                    scoring[k[0]] = 0
                if steps[k] not in scoring:
                    scoring[steps[k]] = 0
                scoring[k[0]] = scoring[k[0]] + iteration[k]
                scoring[steps[k]] = scoring[steps[k]] + iteration[k]
                for new_pair in new_pairs:
                    if new_pair not in working:
                        working[new_pair] = iteration[k]
                    else:
                        working[new_pair] = working[new_pair] + iteration[k]
        iteration = copy.copy(working)

    return scoring


def commons(evolved):
    return max(evolved.values()), min(evolved.values())


def run(filename):
    template, steps = load(filename)
    evolved = evolve(template, steps, 40)
    ma, mi = commons(evolved)
    print(f"{ma - mi}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
