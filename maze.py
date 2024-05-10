import time, random
from cell import Cell

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)


    def _draw_cell(self, i , j):
        self._cells[i][j].draw(
            self._x1 + (i * self._cell_size_x),
            self._y1 + (j * self._cell_size_y),
            self._x1 + ((i + 1) * self._cell_size_x),
            self._y1 + ((j + 1) * self._cell_size_y)
        )

        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            need_to_visit = self._get_adjacent_cells(i, j)

            if len(need_to_visit) == 0:
                self._draw_cell(i, j)
                return
            next_cell_coords = need_to_visit[random.randrange(0, len(need_to_visit))]
            next_cell = self._cells[next_cell_coords[0]][next_cell_coords[1]]

            diff = (next_cell_coords[0] - i, next_cell_coords[1] - j)

            if diff[0] == -1 and diff[1] == 0:
                # move left
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif diff[0] == 1 and diff[1] == 0:
                # move right
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif diff[0] == 0 and diff[1] == -1:
                # move up
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif diff[0] == 0 and diff[1] == 1:
                # move down
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False

            print("\n")
            print("\n")

            self._break_walls_r(next_cell_coords[0], next_cell_coords[1])
            
    def _get_adjacent_cells(self, i, j):
        adj_cells = []
        if i - 1 >= 0 and not self._cells[i - 1][j].visited:
            adj_cells.append((i - 1, j))
        if j - 1 >= 0 and not self._cells[i][j - 1].visited:
            adj_cells.append((i, j - 1))
        if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
            adj_cells.append((i + 1, j))
        if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
            adj_cells.append((i, j + 1))

        return adj_cells

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False

    def solve(self):
        return self._solve_r(0, 0)
