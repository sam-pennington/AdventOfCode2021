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
    print(f"parse_literal:raw_stream => {stream}")
    stream = stream[6:]
    print(f"parse_literal:sans_header => {stream}")
    # Fast path
    if len(stream) == 5:
        return int(stream[1:], 2), ""

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
        if idx+step >= len(stream):
            break
    offset = len(number) % 4
    padding = 4 - offset
    padding = padding if padding < 4 else 0
    return int(number, 2), stream[idx+padding:]


def parse_operator(stream):
    stream = stream[6:]
    tid = stream[0]
    print(f"parse_operator:type => {tid}")
    stream = stream[1:]
    vret = 0
    if tid == '0':
        bit_length = int(stream[0:15], 2)
        print(f"parse_operator:bit_length => {bit_length}")
        stream = stream[15:]
        sub = stream[0:bit_length]
        stream = stream[bit_length:]
        while len(sub) > 6:
            version, sub = extract_packet(sub)
            vret = vret + version
    else:
        packet_length = int(stream[0:11], 2)
        print(f"parse_operator:packet_count => {packet_length}")
        stream = stream[11:]
        for i in range(packet_length):
            v, s = extract_packet(stream)
            stream = s
            vret = vret + v
    return vret, stream


def extract_packet(stream):
    print(f"extract_packet:stream => {stream}")
    header = stream[0:6]
    print(f"extract_packet:header => {header}")
    version, tid = parse_header(header)
    print(f"extract_packet:version:tid => {version}:{tid}")
    if tid == 'LITERAL':
        l, sub = parse_literal(stream)
        return (version, sub)
    else:
        o, sub = parse_operator(stream)
        return (version + o, sub)


def extract(stream):
    v = 0
    while len(stream) > 7:
        v1, s = extract_packet(stream)
        stream = s
        v = v + v1
    return v


def run(filename):
    content = load(filename)
    converted = convert_hexadecimal(content)
    res = extract(converted)
    print(f"{res}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
