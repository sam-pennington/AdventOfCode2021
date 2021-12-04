import copy


def counts(bits):
    return len([x for x in bits if x == '0']), len([x for x in bits if x == '1'])


def most_common(bits):
    ''' Have to move from the previous version as system lib max returns the first item found in the case of equal occurrences '''
    zeros, ones = counts(bits)
    if ones >= zeros:
        return '1'
    return '0'


def least_common(bits):
    ''' Have to move from the previous version as system lib min returns the first item found in the case of equal occurrences '''
    zeros, ones = counts(bits)
    if zeros <= ones:
        return '0'
    return '1'


def filter_lists(lists, bit_pos, value):
    ''' Perform the filtering. Strip out any items that dont have the specified value at the specified bit location. '''
    return [l for l in lists if l[bit_pos] == value]


def generic_filter(bit_lists, original_list, comparitor):
    bls = copy.copy(bit_lists)
    search = copy.copy(original_list)
    bits = len(original_list[0])
    for i in range(0, bits):
        m = comparitor(bls[i])
        search = filter_lists(search, i, m)
        bls = bit_lists_gen(search)
        if len(search) == 1:
            break
    assert(len(search) == 1)
    return search[0]


def filter_oxygen(bit_lists, original_list):
    return generic_filter(bit_lists, original_list, most_common)


def filter_scrubber(bit_lists, original_list):
    return generic_filter(bit_lists, original_list, least_common)


def bit_lists_gen(starting):
    ''' 
    Generate the bit representation of the first bits from all the numbers, then the second, and so on.
    e.g.
    01101
    10110
    00011

    outputs

    010
    100
    110
    011
    101

    It's a transpose basically.
    '''
    bit_lists = []
    for l in starting:
        for idx, value in enumerate(l):
            if idx >= len(bit_lists):
                bit_lists.append([])
            bit_lists[idx].append(value)
    return bit_lists


def main():

    bit_lists = []
    original_bit_strings = []

    with open('input.txt', 'r') as f:
        original_bit_strings = [l[:-1] for l in f]  # Strip the newline

    bit_lists = bit_lists_gen(original_bit_strings)

    # Just deal with strings everywhere (or rather lists of chars) so here at the end we need to convert the
    # string that represents a binary number into an int
    o = int("".join(filter_oxygen(bit_lists, original_bit_strings)), 2)
    s = int("".join(filter_scrubber(bit_lists, original_bit_strings)), 2)
    print(f"{o * s}")


if __name__ == "__main__":
    main()
