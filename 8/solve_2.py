def categorise_easy(code):
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
        return None


def bucket_unknowns(inputs):
    ret = {}
    for i in inputs:
        if categorise_easy(i) is None:
            if len(i) not in ret:
                ret[len(i)] = [i]
            else:
                ret[len(i)] = ret[len(i)] + [i]
    return ret


def find_three(unknowns, categorised):
    potentials = [x for x in unknowns[5] if len(
        set(categorised[1]).difference(set(x))
    ) == 0]
    assert(len(potentials) == 1)
    return potentials[0]


def categorise_length_six(unknowns, categorised):
    potentials = [x for x in unknowns[6] if len(
        set(categorised[1]).difference(set(x))
    ) == 0]
    potential_six = [x for x in unknowns[6] if x not in potentials]
    assert(len(potential_six) == 1)
    # Could be nine or zero
    potential_nine = [x for x in potentials if len(
        set(categorised[4]).difference(set(x))
    ) == 0]
    assert(len(potential_nine) == 1)
    potential_zero = [x for x in potentials if x not in potential_nine]
    assert(len(potential_zero) == 1)
    assert(potential_zero[0] != potential_nine[0])
    assert(potential_six[0] != potential_nine[0])
    assert(potential_six[0] != potential_zero[0])
    return potential_zero[0], potential_six[0], potential_nine[0]


def categorise_two_five(unknowns, categorised):
    assert(categorised[3] is not None)
    assert(categorised[9] is not None)
    assert(categorised[8] is not None)
    # mask out 8 with nine to get the hook for 2.
    # then use that and the known 3 to get 5.
    two_hook = list(set(categorised[8]).difference(set(categorised[9])))
    assert(len(two_hook) == 1)
    two_hook = two_hook[0]
    search = [x for x in unknowns[5] if x != categorised[3]]
    two = [x for x in search if two_hook in x]
    five = [x for x in search if x not in two]
    assert(len(two) == 1)
    assert(len(five) == 1)
    return two[0], five[0]


def analyse(inputs):
    categorised = [None] * 10
    for c in inputs:
        if categorise_easy(c) is not None:
            categorised[categorise_easy(c)] = c
    bucketed_unknowns = bucket_unknowns(inputs)

    categorised[3] = find_three(bucketed_unknowns, categorised)
    categorised[0], categorised[6], categorised[9] = categorise_length_six(
        bucketed_unknowns, categorised
    )
    categorised[2], categorised[5] = categorise_two_five(
        bucketed_unknowns, categorised
    )
    assert(all([x is not None for x in categorised]))
    assert(len(set(categorised)) == len(categorised))

    return categorised


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
    numbers = []
    for inputs, outputs in parsed:
        categorised = analyse(inputs)
        line_output = []
        for o in outputs:
            for idx, x in enumerate(categorised):
                if (len(x) == len(o)) and len(set(o).difference(set(x))) == 0:
                    line_output.append(str(idx))
        numbers.append(int("".join(line_output)))
    print(f"{sum(numbers)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
