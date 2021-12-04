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


def apply(aim, position, instruction, amount):
    aim_ret = aim

    pos_ret = {
        'depth': position['depth'],
        'horizontal': position['horizontal']
    }

    if instruction == FORWARD:
        pos_ret['horizontal'] = pos_ret['horizontal'] + amount
        pos_ret['depth'] = pos_ret['depth'] + (aim_ret * amount)
    elif instruction == UP:
        aim_ret = aim_ret - amount
    else:
        aim_ret = aim_ret + amount

    return aim_ret, pos_ret


def main():

    aim = 0

    position = {
        'depth': 0,
        'horizontal': 0
    }

    with open('input.txt', 'r') as f:
        for line in f:
            instruction, amount = line.split(' ')
            parsed_instruction = parse_instruction(instruction)
            parsed_amount = int(amount)
            aim, position = apply(
                aim, position, parsed_instruction, parsed_amount)

        print(position)
        print(f"answer: {position['depth'] * position['horizontal']}")


if __name__ == "__main__":
    main()
