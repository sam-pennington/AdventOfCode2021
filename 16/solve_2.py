from functools import reduce

HEX_MAP = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def map_hexadecimal(hex):
    return HEX_MAP[hex]


def convert_hexadecimal(line):
    ret = "".join([map_hexadecimal(x) for x in line])
    return ret


def load(filename):
    lines = None
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    assert(len(lines) == 1)
    return lines[0]


def parse_header(header):
    version = int(header[0:3], 2)
    tid = header[3:]
    tid = 'LITERAL' if int(tid, 2) == 4 else 'OPERATOR'
    return version, tid


def parse_literal(stream):
    stream = stream[6:]
    number = ""
    # Groups of 5 till we hit a 5 leading with a zero.
    # Once we hit the last one we then work out how many short
    # we are of a 4 bit boundary. That will then be the
    # zero padding at end.
    step = 5
    idx = 0
    while True:
        segment = stream[idx:idx+step]
        number = number + segment[1:]
        idx = idx + step
        if segment.startswith('0'):
            break
    offset = len(number) % 4
    padding = 4 - offset
    padding = padding if padding < 4 else 0
    print(f"parse_literal:result => {int(number, 2)}")
    return int(number, 2), stream[idx+padding:]


def parse_operator_type(header):
    tid = int(header[3:], 2)
    if 0 == tid:
        return 'sum'
    if 1 == tid:
        return 'product'
    if 2 == tid:
        return 'minimum'
    if 3 == tid:
        return 'maximum'
    if 5 == tid:
        return 'greater than'
    if 6 == tid:
        return 'less than'
    if 7 == tid:
        return 'equal to'


def parse_operator(stream):

    header = stream[0:6]
    t = parse_operator_type(header)

    print(f"parse_operator:op_type => {t}")
    stream = stream[6:]
    tid = stream[0]
    print(f"parse_operator:type => {tid}")
    stream = stream[1:]
    vals = []
    if tid == '0':
        bit_length = int(stream[0:15], 2)
        print(f"parse_operator:bit_length => {bit_length}")
        stream = stream[15:]
        sub = stream[0:bit_length]
        stream = stream[bit_length:]
        while len(sub):
            try:
                l, sub = extract_packet(sub)
                if type(l) == list:
                    vals = vals + l
                else:
                    vals = vals + [l]
            except IndexError:
                break
    else:
        packet_length = int(stream[0:11], 2)
        print(f"parse_operator:packet_count => {packet_length}")
        stream = stream[11:]
        for _ in range(packet_length):
            l, s = extract_packet(stream)
            stream = s
            if type(l) == list:
                vals = vals + l
            else:
                vals = vals + [l]

    vals = evaluate(t, vals)

    return vals, stream


def evaluate(t, vals):
    print(f"evaluate:vals => {t}({vals})")
    if t == 'sum':
        s = 0
        for v in vals:
            s = s + v
        v = s
    elif t == 'product':
        v = reduce(lambda x, y: x * y, vals)
    elif t == 'minimum':
        v = min(vals)
    elif t == 'maximum':
        v = max(vals)
    elif t == 'greater than':
        assert(len(vals) == 2)
        v = 1 if vals[0] > vals[1] else 0
    elif t == 'less than':
        assert(len(vals) == 2)
        v = 1 if vals[0] < vals[1] else 0
    elif t == 'equal to':
        assert(len(vals) == 2)
        v = 1 if vals[0] == vals[1] else 0
    else:
        raise Exception("Unrecognised operator")

    print(f"evaluate:result => {v}")

    return v


def extract_packet(stream):
    header = stream[0:6]
    print(f"extract_packet:header => {header}")
    version, tid = parse_header(header)
    print(f"extract_packet:version:tid => {version}:{tid}")
    if tid == 'LITERAL':
        l, sub = parse_literal(stream)
        return l, sub
    else:
        l, sub = parse_operator(stream)
        return l, sub


def extract(stream):
    v, remainder = extract_packet(stream)
    print(f"Stream remainder: {remainder}")
    return v


def run(filename):
    content = load(filename)
    converted = convert_hexadecimal(content)
    v = extract(converted)
    print(f"{v}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
