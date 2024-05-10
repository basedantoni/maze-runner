import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_draw_cell(self):
        num_cols = 6
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._cells[0][0].draw(10, 10, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_left_wall,
            True,
        )
        self.assertEqual(
            m1._cells[0][0].has_right_wall,
            True,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 6
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[num_cols - 1][num_cols - 1].has_bottom_wall, False)

    def test_maze_get_adjacent_cells(self):
        num_cols = 6
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        m1._cells[1][1].visited = True
        adj_cells = m1._get_adjacent_cells(1, 2)

        self.assertEqual(adj_cells, [(0,2), (2,2), (1,3)])

    def test_maze_reset_cells_visited(self):
        num_cols = 6
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(m1._cells[i][j].visited, False)

if __name__ == "__main__":
    unittest.main()
