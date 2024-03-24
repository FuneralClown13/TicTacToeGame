import random

class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return not bool(self.value)


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return property()
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)
    is_human_win = Descriptor()
    is_computer_win = Descriptor()
    is_draw = Descriptor()

    def __init__(self):
        self.pole = tuple([tuple([Cell() for _ in '...']) for _ in '...'])
        self.reset()

    def init(self):
        for row in self.pole:
            for cell in row:
                cell.value = self.FREE_CELL
        self.reset()

    def reset(self):
        self.free_cells = sum([[(r, c) for c in range(3)] for r in range(3)], [])
        self.is_human_win = False
        self.is_computer_win = False
        self.is_draw = False

    def get_star_coords(self, coords):
        r, c = coords
        coords_row = [(r + i, c) for i in range(-2, 3) if 0 <= r + i < 3]
        coords_col = [(r, c + i) for i in range(-2, 3) if 0 <= c + i < 3]
        coords_d1 = [(0, 0), (1, 1), (2, 2)]
        coords_d2 = [(0, 2), (1, 1), (2, 0)]
        return coords_row, coords_col, coords_d1, coords_d2

    def winning_move_handler(self, coords):
        for coord in self.get_star_coords(coords):
            c1, c2, c3 = coord
            if self[c1] != self.FREE_CELL and self[c1] == self[c2] == self[c3]:
                if self[c1] == self.HUMAN_X:
                    self.is_human_win = True
                else:
                    self.is_computer_win = True
                return coords

    def move_handler(self, coords):
        self.winning_move_handler(coords)
        if not self.free_cells and self:
            self.is_draw = True

    def show(self):
        print(*[[self.pole[r][c].value for c in range(3)] for r in range(3)], sep='\n')

    def human_go(self):
        r, c = map(int, input().split())
        if not self.pole[r][c].value:
            self.pole[r][c].value = self.HUMAN_X
            self.free_cells.remove((r, c))
        self.move_handler((r, c))

    def computer_go(self):
        r, c = random.choice(self.free_cells)
        self.pole[r][c].value = self.COMPUTER_O
        self.free_cells.remove((r, c))
        self.move_handler((r, c))

    @staticmethod
    def index_handler(indexes):
        r, c = indexes
        if type(r) != int or type(c) != int or not (0 <= r < 3 and 0 <= c < 3):
            raise IndexError('некорректно указанные индексы')
        return r, c

    def __getitem__(self, indexes):
        r, c = self.index_handler(indexes)
        return self.pole[r][c].value

    def __setitem__(self, indexes, value):
        r, c = self.index_handler(indexes)
        self.pole[r][c].value = value
        self.move_handler(indexes)
        if indexes in self.free_cells:
            self.free_cells.remove((r, c))

    def __bool__(self):
        return not any((self.is_human_win, self.is_computer_win, self.is_draw))