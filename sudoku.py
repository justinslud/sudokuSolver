import numpy as np

class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.grid_to_parts()

        self.info = {0:{'vertsquare0':3, 'vertsquare1':6, 'rowadj0':1, 'rowadj1':2, 'coladj0':1, 'coladj1':2},
            1:{'vertsquare0':4, 'vertsquare1':7, 'rowadj0':0, 'rowadj1':2, 'coladj0':1, 'coladj1':2},
            2:{'vertsquare0':5, 'vertsquare1':8, 'rowadj0':0, 'rowadj1':1, 'coladj0':1, 'coladj1':2},
            3:{'vertsquare0':0, 'vertsquare1':6, 'rowadj0':4, 'rowadj1':5, 'coladj0':0, 'coladj1':2},
            4:{'vertsquare0':1, 'vertsquare1':7, 'rowadj0':3, 'rowadj1':5, 'coladj0':0, 'coladj1':2},
            5:{'vertsquare0':2, 'vertsquare1':8, 'rowadj0':3, 'rowadj1':4, 'coladj0':0, 'coladj1':2},
            6:{'vertsquare0':0, 'vertsquare1':3, 'rowadj0':7, 'rowadj1':8, 'coladj0':0, 'coladj1':1},
            7:{'vertsquare0':1, 'vertsquare1':4, 'rowadj0':6, 'rowadj1':8, 'coladj0':0, 'coladj1':1},
            8:{'vertsquare0':2, 'vertsquare1':5, 'rowadj0':6, 'rowadj1':7, 'coladj0':0, 'coladj1':1}
        }

    def update_grid(self, row_num, col_num, num):
        self.grid[9*row_num + col_num] = num
        print('only {} more tiles left!'.format(self.grid.count(0)))
        self.grid_to_parts()
        return self.grid

    def grid_to_parts(self):
        self.rows = [self.grid[i:i+9] for i in range(0, len(self.grid), 9)]
        self.cols = [[row[i] for row in self.rows] for i in range(9)]
        self.squares = [list(np.concatenate([row[i:i+3] for row in self.rows[j:j+3]])) for j in range(0, len(self.rows), 3) for i in range(0, len(self.rows), 3)]
        return self.rows, self.cols, self.squares

    def print_grid(self):
        print(''.center(20, '-'))
        for row in self.rows[::-1]:    
            print('|' + ' '.join(str(i) for i in row) + '|')
        print(''.center(20, '-'))

    def check_sol(self):
        if not all(sorted(row) == list(range(1,10)) for row in self.rows): 
            return False
        if not all(sorted(square) == list(range(1,10)) for square in self.squares): 
            return False
        return True

    def get_square(self, row_num, col_num):
        return 3*(row_num // 3) + (col_num // 3)

    def get_tile_num(self, row_num, col_num):
        return 3*(row_num % 3) + col_num % 3

    def get_tile_neighbors_hor(self, row_num, col_num, info):
        return 3*(row_num//3) + info['coladj0'], 3*(row_num//3) + info['coladj1']

    def get_tile_neighbors_vert(self, row_num, col_num, info):
        return 3*(col_num//3) + info['coladj0'], 3*(col_num//3) + info['coladj1']
    
    def get_row_neighbors(self, row_num):
        return self.info[row_num]['rowadj0'], self.info[row_num]['rowadj1']

    def get_col_neighbors(self, col_num):
        return self.info[col_num]['rowadj0'], self.info[col_num]['rowadj1']

    def check_simple_force(self, row_num, col_num, num):
        square_num = self.get_square(row_num, col_num)
        row, col, square = self.rows[row_num], self.cols[col_num], self.squares[square_num]
        
        if row[col_num] != 0: 
            return False
        if num in row or num in col or num in square: 
            return False

        info = self.info[self.get_tile_num(row_num, col_num)]
        row1, row2 = self.get_tile_neighbors_hor(row_num, col_num, info)
        col1, col2 = self.get_tile_neighbors_vert(row_num, col_num, info)

        row3, row4 = self.get_row_neighbors(row_num)
        col3, col4 = self.get_col_neighbors(col_num)
        #if row_num == 2 and col_num == 8 and num == 7: print(row_num)
        if num in self.rows[row3] and num in self.rows[row4]:
            if num in self.cols[col3] and num in self.cols[col4]:  
                print(row_num, col_num, num, row, col, square)
                self.update_grid(row_num, col_num, num)
                return True

            elif square[info['rowadj0']] != 0 and square[info['rowadj1']] != 0:
                print(row_num, col_num, num, row, col, square)
                self.update_grid(row_num, col_num, num)
                return True

        if num in self.cols[col3] and num in self.cols[col4]:
            if square[info['vertsquare0']] != 0 and square[info['vertsquare1']] != 0:
                print(row_num, col_num, num, row, col, square)
                self.update_grid(row_num, col_num, num)
                return True


    def check_row_finish(self, row_num):
        row = self.rows[row_num]
        if row.count(0) == 1:
            self.update_grid(row_num, row.index(0), sum(set(list(range(1,10))) - set(row)))
            return True

        elif row.count(0) == 2:
            first = row.index(0)
            second = 8-row[::-1].index(0)
            for element in set(list(range(1,10))) - set(row):
                if element in self.cols[first]:
                    self.update_grid(row_num, second, element)
                elif element in self.cols[second]:
                    self.update_grid(row_num, first, element)
    
    def check_col_finish(self, col_num):
        col = self.cols[col_num]
        if col.count(0) == 1:
            self.update_grid(col.index(0), col_num, sum(set(list(range(1,10))) - set(col)))

        elif col.count(0) == 2:
            for element in set(list(range(1,10))) - set(col):
                self.check_simple_force(col.index(0), col_num, element)
    
    def get_row_col(self, square_num, tile_num):
        return 3*(square_num//3) + (tile_num//3), 3*(square_num%3) + tile_num % 3
    
    def check_square_finish(self, square_num):
        square = self.squares[square_num]
        if square.count(0) == 1:
            
            row_num, col_num = self.get_row_col(square_num, square.index(0))
            print(row_num, col_num)
            self.update_grid(row_num, col_num, sum(set(list(range(1,10))) - set(square)))


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
            print('this is the {}th loop!'.format(loops))
            for row_num, row in enumerate(self.rows):
                self.check_row_finish(row_num)
                self.check_col_finish(row_num)
                for col_num, num in enumerate(row):
                    if num == 0:
                        for i in range(1,10):
                            self.check_simple_force(row_num, col_num, i)
            if self.grid.count(0) == 0:
                if self.check_sol():
                    print('yayayy')
                else:
                    print('grid could not be solved')
                break
            loops += 1
        return self.grid

test_grid     = [0,3,7,0,0,0,0,5,0,0,5,0,0,3,7,4,0,8,6,0,0,0,0,5,3,1,0,0,0,0,0,4,0,0,8,2,0,8,1,0,5,0,6,7,0,7,4,0,0,2,0,0,0,0,0,6,2,4,0,0,0,0,5,3,0,5,6,9,0,0,4,0,0,1,0,0,0,0,9,2,0]

grid = Sudoku(test_grid)
grid.solve()
grid.print_grid()