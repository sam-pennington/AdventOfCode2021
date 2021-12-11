
def is_opening_token(token):
    return token in ('(', '[', '{', '<')


def is_closing_token(token):
    return token in (')', ']', '}', '>')


def paired_close_token(token):
    if '(' == token:
        return ')'
    elif '[' == token:
        return ']'
    elif '{' == token:
        return '}'
    elif '<' == token:
        return '>'
    else:
        raise NotImplementedError()


def load_file(filename):
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
        return lines


def parse_line(line):
    stack = []
    for c in line:
        assert(is_opening_token(c) or is_closing_token(c))
        if is_opening_token(c):
            stack.append(c)
        else:
            opener = stack.pop()
            if paired_close_token(opener) != c:
                return c
    return None


def score_invalid(invalid):
    if ')' == invalid:
        return 3
    elif ']' == invalid:
        return 57
    elif '}' == invalid:
        return 1197
    elif '>' == invalid:
        return 25137
    else:
        raise NotImplementedError()


def score(invalids):
    return sum([score_invalid(x) for x in invalids])


def run(filename):
    lines = load_file(filename)
    corrupted = []
    for l in lines:
        invalid = parse_line(l)
        if invalid is not None:
            corrupted.append(invalid)
    print(f"{corrupted}")
    print(f"{score(corrupted)}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
