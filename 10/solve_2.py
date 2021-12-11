import math


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


def complete_line(line):
    stack = []
    for c in line:
        assert(is_opening_token(c) or is_closing_token(c))
        if is_opening_token(c):
            stack.append(c)
        else:
            opener = stack.pop()
            assert(c == paired_close_token(opener))
    # Anything left in the stack now is the completion set.
    closing = []
    list.reverse(stack)
    for s in stack:
        closing.append(paired_close_token(s))
    return closing


def score_closing(token):
    if ')' == token:
        return 1
    elif ']' == token:
        return 2
    elif '}' == token:
        return 3
    elif '>' == token:
        return 4
    else:
        raise NotImplementedError()


def score(closings):
    scores = [score_closing(x) for x in closings]
    total = 0
    for score in scores:
        total = total * 5
        total = total + score
    return total


def run(filename):
    lines = load_file(filename)
    incomplete_lines = [l for l in lines if parse_line(l) is None]
    closings = [complete_line(l) for l in incomplete_lines]
    scored = [score(l) for l in closings]
    sorted_scored = sorted(scored)
    middle = math.ceil(len(sorted_scored) / 2)
    print(f"{sorted_scored[middle-1]}")


def main():
    filename = "input.txt"
    run(filename)


if __name__ == "__main__":
    main()
