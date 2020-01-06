import numpy as np

class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.grid_to_parts()

        self.info = {0:{'vertadj':[3,6], 'rowadj':[1,2], 'coladj':[1,2]},
            1:{'vertadj':[4,7], 'rowadj':[0,2], 'coladj':[1,2]},
            2:{'vertadj':[5,8], 'rowadj':[0,1], 'coladj':[1,2]},
            3:{'vertadj':[0,6], 'rowadj':[4,5], 'coladj':[0,2]},
            4:{'vertadj':[1,7], 'rowadj':[3,5], 'coladj':[0,2]},
            5:{'vertadj':[2,8], 'rowadj':[3,4], 'coladj':[0,2]},
            6:{'vertadj':[0,3], 'rowadj':[7,8], 'coladj':[0,1]},
            7:{'vertadj':[1,4], 'rowadj':[6,8], 'coladj':[0,1]},
            8:{'vertadj':[2,5], 'rowadj':[6,7], 'coladj':[0,1]}
        }

    def update_grid(self, tile_row, tile_col, num):
        self.grid[9*tile_row + tile_col] = num
        print('only {} more tiles left!'.format(self.grid.count(0)))
        self.grid_to_parts()

    def grid_to_parts(self):
        self.rows = [self.grid[i:i+9] for i in range(0, len(self.grid), 9)]
        self.cols = [[row[i] for row in self.rows] for i in range(9)]
        self.squares = [list(np.concatenate([row[i:i+3] for row in self.rows[j:j+3]])) for j in range(0, len(self.rows), 3) for i in range(0, len(self.rows), 3)]

    def print_grid(self):
        print(''.center(20, '-'))
        for row in self.rows[::-1]:    
            print('|' + ' '.join(str(i) for i in row) + '|')
        print(''.center(20, '-'))

    def check_sol(self):
        if not all(sorted(row) == list(range(1,10)) for row in self.rows): return False
        if not all(sorted(square) == list(range(1,10)) for square in self.squares): return False
        return True

    def get_square(self, row, col):
        return 3*(row // 3) + (col % 3)

    def check_simple_force(self, tile_row, tile_col, num):
        square_num = self.get_square(tile_row, tile_col)
        row, col, square = self.rows[tile_row], self.cols[tile_col], self.squares[square_num]
        if num in row or num in col or num in square: return

        #square_info = self.info[square_num]
        tile_info = self.info[3*(tile_row//3) + tile_col%3]
        if tile_row == 4 and tile_col == 0 and num == 2:print(tile_info, 3*(tile_row//3) + tile_col%3)

        if row[tile_col] != 0: return
        if num in self.rows[tile_row//3 + tile_info['coladj'][0]] and num in self.rows[tile_row//3 + tile_info['coladj'][1]]:
            if num in self.cols[tile_col//3 + tile_info['coladj'][0]] and num in self.cols[tile_col//3 + tile_info['rowadj'][1]]:    
                print('made it this far!')
                self.update_grid(tile_row, tile_col, num)
                return True
            elif self.rows[tile_row][tile_info['rowadj'][0]] != 0 and self.rows[tile_row][tile_info['rowadj'][1]] != 0:
                print('made it this far!')
                self.update_grid(tile_row, tile_col, num)
                return True
    
    def check_row_finish(self, tile_row):
        row = self.rows[tile_row]
        if row.count(0) == 1:
            self.update_grid(tile_row, row.index(0), sum(set(list(range(1,10))) - set(row)))
            return True

        elif row.count(0) == 2:
            for element in set(list(range(1,10))) - set(row):
                self.check_simple_force(tile_row, row.index(0), element)
    
    def check_col_finish(self, tile_col):
        col = self.cols[tile_col]
        if col.count(0) == 1:
            self.update_grid(col.index(0), tile_col, sum(set(list(range(1,10))) - set(col)))

        elif col.count(0) == 2:
            for element in set(list(range(1,10))) - set(col):
                self.check_simple_force(col.index(0), tile_col, element)
    
    def check_square_finish(self, square_num):
        square = self.squares[square_num]
        if square.count(0) == 1:
            self.update_grid(square.index(0) // 3, square.index(0) % 3, sum(set(list(range(9))) - set(square)))

        if square.count(0) == 2:
            # see if same row or col
            pass
        else:
            #if self.check_simple_force()
            pass

    def solve(self):
        loops = 0
        while loops < 100:#not self.check_sol():
            for square_num in range(9):
                self.check_square_finish(square_num)
            #print('this is the {}th loop!'.format(loops))
            for tile_row, row in enumerate(self.rows):
                self.check_row_finish(tile_row)
                self.check_col_finish(tile_row)
                for tile_col, num in enumerate(row):
                    if num == 0:
                        for i in range(1,10):
                            self.check_simple_force(tile_row, tile_col, i)
            loops += 1
        return self.grid

test_grid     = [0,3,7,0,0,0,0,5,0,0,5,0,0,3,7,4,0,8,6,0,0,0,0,5,3,1,0,0,0,0,0,4,0,0,8,2,0,8,1,0,5,0,6,7,0,7,4,0,0,2,0,0,0,0,0,6,2,4,0,0,0,0,5,3,0,5,6,9,0,0,4,0,0,1,0,0,0,0,9,2,0]

grid = Sudoku(test_grid)
grid.solve()
grid.print_grid()