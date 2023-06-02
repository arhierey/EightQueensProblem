from random import shuffle


class Field:
    def __init__(self, column: int, row: int, ancestor=None):
        self.column = column
        self.str_column = chr(96 + column)
        self.row = row
        if ancestor:
            self.taken = ancestor.taken
            self.fig = ancestor.fig
        else:
            self.taken = False
            self.fig = None

    def __str__(self):
        return self.str_column + str(self.row) + ':' + str(self.taken) + '-' + str(self.fig)

    def __add__(self, other: tuple):
        return Field(self.column+other[0], self.row+other[1])

    def get_notation(self):
        return self.str_column + str(self.row)


class Board:
    def __init__(self, ancestor=None):
        self.files = {}
        for i in range(1, 9):
            for j in range(1, 9):
                field = Field(i, j)
                if ancestor:
                    self.files[field.get_notation()] = Field(i, j, ancestor.files[field.get_notation()])
                else:
                    self.files[field.get_notation()] = field

    def __str__(self):
        res = ''
        for index in range(8):
            res += ' '.join('1' if self.files[column+str(8-index)].taken else '0'
                            for column in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')) + '\n'
        return res

    def __eq__(self, other):
        temp = []
        for field in self.files:
            if self.files[field].fig:
                if other.files[field].fig:
                    temp.append(True)
                else:
                    temp.append(False)
        return all(temp)

    def fen(self):
        res = []
        for number in range(8, 0, -1):
            line = ''
            empty = 0
            cols = 8
            for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                if self.files[letter + str(number)].fig:
                    if empty != 0:
                        line += str(empty) + 'Q'
                        cols -= empty
                        empty = 0
                    else:
                        line += 'Q'
                    cols -= 1
                else:
                    # line += '1'
                    empty += 1

            if cols != 0:
                res.append(line + str(cols))
            else:
                res.append(line)
        res = '/'.join(line for line in res)

        return res

    def available_files(self):
        res = []
        for key in self.files:
            if not self.files[key].taken:
                res.append(key)
        shuffle(res)  # TODO: validate
        return res

    def put_queen(self, queen, file):
        queen.put(self.files[file])
        queen.take_files(self)

    def take_file(self, field):
        self.files[field.get_notation()].taken = True

    def copy(self):
        board = Board(self)
        return board


class Queen:
    def __init__(self, start_pos: tuple):
        self.pos = Field(start_pos[0], start_pos[1])
        self.directions = {'up': (0, 1), 'down': (0, -1), 'right': (1, 0), 'left': (-1, 0),
                           'left-down': (-1, -1), 'right-down': (1, -1), 'left-up': (-1, 1), 'right-up': (1, 1)}
        self.borders = {
            'up': ((0, 9), (0, 8)), 'down': ((0, 9), (1, 9)), 'left': ((1, 9), (0, 9)), 'right': ((0, 8), (0, 9)),
            'left-down': ((1, 9), (1, 9)), 'right-down': ((0, 8), (1, 9)),
            'left-up': ((1, 9), (0, 8)), 'right-up': ((0, 8), (0, 8)),
        }

    def __str__(self):
        return 'Queen on ' + str(self.pos)

    def put(self, field):
        self.pos = field

    def move(self, direction, board):
        field = self.pos

        while self.borders[direction][0][0] < field.column < self.borders[direction][0][1] \
                and self.borders[direction][1][0] < field.row < self.borders[direction][1][1]:
            field += self.directions[direction]
            board.take_file(field)

    def take_files(self, board):
        board.files[self.pos.get_notation()].taken = True
        board.files[self.pos.get_notation()].fig = True
        for d in self.directions:
            self.move(d, board)


def put_queens(queen, board, level=0):
    if board.available_files() and level < 8:
        files = board.available_files()
        for file in files:
            b = board.copy()
            b.put_queen(queen, file)
            result = put_queens(queen, b, level + 1)
            if result:
                return result
    elif level == 8:
        return board


# q = Queen((1, 1))
# b = Board()
# 
# b1 = put_queens(q, b)
# print(b1)
# print('Queens are placed on')
# for field in b1.files:
#     if b1.files[field].fig:
#         print(b1.files[field])
