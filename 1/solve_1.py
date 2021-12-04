

def main():

    previous = None
    increased = 0
    decreased = 0
    with open('input.txt', 'r') as f:
        for line in f:
            value = int(line)
            if previous is not None:
                if value > previous:
                    increased = increased + 1
                elif value < previous:
                    decreased = decreased + 1
            previous = value

    print(f"increased: {increased}; decreased: {decreased}")


if __name__ == "__main__":
    main()
