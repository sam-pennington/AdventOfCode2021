FORWARD = 1
DOWN = 2
UP = 3

MAPPING = {
    'forward': FORWARD,
    'down': DOWN,
    'up': UP
}


def parse_instruction(instruction):
    r = MAPPING.get(instruction, None)
    assert(r is not None)
    return r


def apply(position, instruction, amount):
    ret = {
        'depth': position['depth'],
        'horizontal': position['horizontal']
    }

    if instruction == FORWARD:
        ret['horizontal'] = ret['horizontal'] + amount
    elif instruction == UP:
        ret['depth'] = ret['depth'] - amount
    else:
        ret['depth'] = ret['depth'] + amount

    return ret


def main():

    position = {
        'depth': 0,
        'horizontal': 0
    }

    with open('input.txt', 'r') as f:
        for line in f:
            instruction, amount = line.split(' ')
            parsed_instruction = parse_instruction(instruction)
            parsed_amount = int(amount)
            position = apply(position, parsed_instruction, parsed_amount)

        print(position)
        print(f"answer {position['depth'] * position['horizontal']}")


if __name__ == "__main__":
    main()
