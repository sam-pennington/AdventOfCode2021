from itertools import islice


def parse_board(unparsed):
    board = [line.split(" ") for line in unparsed]
    # Filter out any empty cells
    for idx, row in enumerate(board):
        filtered = [x for x in row if len(x) > 0]
        assert(len(filtered) == 5)
        board[idx] = filtered
    assert(len(board) == 5)
    return board


def parse_boards(unparsed):
    # Assumption on board size 5 here
    count_boards = len(unparsed) // 5
    boards = []
    for i in range(0, count_boards):
        # Assumption on board size 5 here
        board = [x for x in islice(unparsed, i*5, (i+1)*5)]
        boards.append(parse_board(board))
    return boards


def column_iterator(board):
    column = []
    for idx in range(0, len(board)):
        for row in board:
            column.append(row[idx])
        yield column
        column = []


def determine_winner(calls, boards):
    set_calls = set(calls)
    for idx, board in enumerate(boards):
        # Rows first as easier
        for row in board:
            if set(row).issubset(set_calls):
                return idx, board
        # Same concept for columns but we have to get the columns...
        for column in column_iterator(board):
            if set(column).issubset(set_calls):
                return idx, board
    return 0, None


def calculate_score(board, calls, number):
    # Easiest way is to just abandon structure, and acknowledge that there
    # shouldn't be any repeats. So we can just treat them as two sets and
    # use difference to get the set of board numbers that aren't in the calls
    # set.
    flattened = set([item for sublist in board for item in sublist])
    uncalled = flattened.difference(calls)
    print(f"uncalled: {uncalled}")
    return sum([int(x) for x in uncalled]) * int(number)


def load_data(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Boards are a defined 5x5 so we don't need the gapped lines
        lines = [line.rstrip() for line in lines if len(line.rstrip()) > 0]

    # First line is the bingo numbers
    bingo_calls = lines[0].split(",")
    # Then skip the bingo calls line and start procesing boards
    unparsed_boards = lines[1:]
    parsed_boards = parse_boards(unparsed_boards)
    # Go through the action of calling numbers, and check for winning boards
    # There must be at least 5 called numbers to win, so start with five.
    winning_boards = []

    for i in range(5, len(bingo_calls) + 1):
        temporal_call_set = list(islice(bingo_calls, 0, i))
        winning_idx, winning_board = determine_winner(
            temporal_call_set, parsed_boards
        )
        # We have to repeatedly determine boards that win with this call.
        while winning_board is not None:
            # we have to remove previous winning boards otherwise we will get the same thing
            # over and over
            del parsed_boards[winning_idx]
            winning_calls = temporal_call_set
            winning_number = winning_calls[-1]
            winning_boards.append(
                (winning_board, winning_calls, winning_number)
            )
            winning_idx, winning_board = determine_winner(
                temporal_call_set, parsed_boards
            )

    assert(len(winning_boards) > 0)
    print(f"{winning_boards[-1]}")
    winning_board, winning_calls, winning_number = winning_boards[-1]
    score = calculate_score(winning_board, winning_calls, winning_number)
    print(f"score: {score}")


def main():
    filename = "input.txt"
    load_data(filename)


if __name__ == "__main__":
    main()
