import numpy as np


def main():

    values = []

    with open('input.txt', 'r') as f:
        values = [int(x) for x in f]

    data = np.array(values)

    # convolution is a bit of a heavyweight concept for this.
    # https://stackoverflow.com/a/20036959 explains it better than I can.
    # TLDR; because we are using a size three array of ones (np.ones) as the second 'signal' it just
    #       boils down to doing what I want which is the sliding window sum.
    # Could also of just done something with itertools islice https://docs.python.org/3/library/itertools.html#itertools.islice
    output = np.convolve(data, np.ones(3, dtype=int), 'valid')

    previous = None
    increased = 0
    decreased = 0

    for v in output:
        if previous is not None:
            if v > previous:
                increased = increased + 1
            elif v < previous:
                decreased = decreased + 1
        previous = v

    print(f"increased: {increased}; decreased: {decreased}")


if __name__ == "__main__":
    main()
