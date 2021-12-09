def load(filename):
    with open(filename, 'r') as f:
        vals = f.readlines()[0].split(',')
        return [int(v) for v in vals]


def fuel_calculation(target, current):
    return sum([x for x in range(1, abs(current - target) + 1)])


def calculate(target, positions):
    return sum([fuel_calculation(target, p) for p in positions])


def run(filename):
    initial_values = load(filename)
    start = min(initial_values)
    end = max(initial_values)
    lowest_fuel = None
    for val in range(start, end + 1):
        calculated = calculate(val, initial_values)
        lowest_fuel = calculated if lowest_fuel is None else min(
            lowest_fuel, calculated
        )
    print(f"Lowest: {lowest_fuel}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
