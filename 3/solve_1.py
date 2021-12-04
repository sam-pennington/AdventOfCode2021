

def most_common(bits):
    return max(set(bits), key=bits.count)


def least_common(bits):
    return min(set(bits), key=bits.count)


def main():

    bit_lists = []

    with open('input.txt', 'r') as f:
        for line in f:
            for idx, value in enumerate(line[:-1]):
                if idx >= len(bit_lists):
                    bit_lists.append([])
                bit_lists[idx].append(value)

    gamma = []
    epsilon = []

    for bl in bit_lists:
        mc = most_common(bl)
        lc = least_common(bl)
        gamma.append(mc)
        epsilon.append(lc)

    gamma = int("".join(gamma), 2)
    epsilon = int("".join(epsilon), 2)
    print(f"{gamma * epsilon}")


if __name__ == "__main__":
    main()
