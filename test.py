import unittest
from sudoku import *

class test_sudoku(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nums = [0,3,7,0,0,0,0,5,0,0,5,0,0,3,7,4,0,8,6,0,0,0,0,5,3,1,0,0,0,0,0,4,0,0,8,2,0,8,1,0,5,0,6,7,0,7,4,0,0,2,0,0,0,0,0,6,2,4,0,0,0,0,5,3,0,5,6,9,0,0,4,0,0,1,0,0,0,0,9,2,0]
        cls.grid = Sudoku(cls.nums)
    
    def test_parts(self):
        rows, cols, squares = self.grid.grid_to_parts()
        self.assertEqual(rows[0], self.nums[:9])
        self.assertEqual(cols[0], [self.nums[i] for i in range(0,81,9)])
        self.assertTrue(all([len(square) == 9 for square in squares]))
        
if __name__ == '__main__':
    unittest.main()
