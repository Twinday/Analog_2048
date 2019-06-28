import random as rnd
import static as s

class Game:
    def __init__(self):
        self.lup = (0, 0)
        self.select_cell = []
        self.matrix = list()
        self.GameWidth = 5
        self.GameHeight = 5
        self.score = 0

    def create_level(self):
        self.matrix.clear()
        for i in range(self.GameHeight):
            row = []
            for j in range(self.GameWidth):
                row.append(0)
            self.matrix.append(row)
        self._add_new_blocks(3)
        self.score = 0

    def _random_block(self):
        coeff = rnd.random()
        if coeff > 0.7:
            return rnd.randint(2, 3)
        else:
            return 1

    def _random_place(self):
        indexes = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                   indexes.append((i, j))
        r = rnd.randint(0, len(indexes) - 1)
        return indexes[r]

    def _add_new_blocks(self, n):
        for a in range(n):
            place = self._random_place()
            self.matrix[place[0]][place[1]] = self._random_block()

    def move_border(self, side):
        map = {
            'up': (self.lup[0] - 1, self.lup[1]),
            'down': (self.lup[0] + 1, self.lup[1]),
            'left': (self.lup[0], self.lup[1] - 1),
            'right': (self.lup[0], self.lup[1] + 1)
        }

        if side == 'up':
            if self.lup[0] > 0:
                self.lup = map[side]
        if side == 'down':
            if self.lup[0] < len(self.matrix) - 1:
                self.lup = map[side]
        if side == 'left':
            if self.lup[1] > 0:
                self.lup = map[side]
        if side == 'right':
            if self.lup[1] < len(self.matrix[0]) - 1:
                self.lup = map[side]
        pass

    def _create_path_matrix(self, end):
        result = []
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 0:
                    row.append("0")
                elif self.matrix[i][j] > 0:
                    row.append("1")
            result.append(row)
        result[end[0]][end[1]] = "0"
        return result

    def _search_path(self, p1, p2):
        matrix_path = self._create_path_matrix(p2)
        flag = s.search_path(matrix_path, p1, p2)
        if flag:
            return True
        else:
            return False

    def _select_blocks(self):
        if len(self.select_cell) > 0:
            cell = (self.lup[0], self.lup[1])
            a = self.select_cell[0]
            if cell != a:
                if self.matrix[cell[0]][cell[1]] == self.matrix[a[0]][a[1]] and self._search_path(a, cell):
                    self.matrix[cell[0]][cell[1]] += 1
                    self.matrix[a[0]][a[1]] = 0
                    self.score += self.matrix[cell[0]][cell[1]]
                    self._add_new_blocks(1)
                elif self.matrix[cell[0]][cell[1]] == 0:
                    self.matrix[cell[0]][cell[1]] = self.matrix[a[0]][a[1]]
                    self.matrix[a[0]][a[1]] = 0
                    self._add_new_blocks(2)

            self.select_cell.clear()
        else:
            block = (self.lup[0], self.lup[1])
            if self.matrix[block[0]][block[1]] > 0:
                self.select_cell.append(block)

    def check_end_game(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 12:
                    return True
        return False

    def update(self):
        self._select_blocks()

    def getGameWidth(self):
        return self.GameWidth

    def getGameHeight(self):
        return self.GameHeight

    def __getitem__(self, key):
        return self.matrix[key[0]][key[1]]

    def getLup(self):
        return self.lup

    def get_score(self):
        return self.score

    def get_select_cell(self):
        return self.select_cell
