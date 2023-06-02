from main import *


def board_in_list(board, boards):
    for each in boards:
        if board == each:
            return True
    return False


result = []
for _ in range(500):
    q = Queen((1, 1))
    b = Board()
    b1 = put_queens(q, b)
    if not board_in_list(b1, result):
        result.append(b1)

print('There are', len(result), 'solutions')
