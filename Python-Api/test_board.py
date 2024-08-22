import unittest
from Board import *

class TestBoard(unittest.TestCase):
    def test_board_init(self):
        board = Board(device=None)
    
        for x in range(board.BOARD_HEIGHT ):
            for y in range(board.BOARD_WIDTH):
                self.assertEqual(board[(x,y)] , (RGB.red(),False))
    def test_get_set_item(self):
        
        board = Board(device=None)
    
        for x in range(board.BOARD_HEIGHT ):
            for y in range(board.BOARD_WIDTH):
                board[(x,y)] = RGB(r=127,g=127,b=127)
        
        
        for x in range(board.BOARD_HEIGHT ):
            for y in range(board.BOARD_WIDTH):
                self.assertEqual( board[(x,y)] , (RGB(127,127,127),False)) 
    
    def test_conv_1_d(self):
        
        board = Board(None)
        for x in range(0,8):
            for y in range(0,8):
                self.assertEqual( board.conv_1_d((x,y)) , x * 8 + y)
                
        invalid_test_cases = [(-1,0),(0,-1),(8,0),(0,8)]
        for x,y in invalid_test_cases:
            self.assertRaises(Exception,board.conv_1_d((x,y)))
            
    def test_get_action_number(self):
        board = Board(device = None)
        self.assertEqual(board.action_number , 0)

class TestRGB(unittest.TestCase):
    def test_str(self):
        color = RGB(r=255,g=0,b=0)
        self.assertEqual(color.__str__(),"ff0000")

        color = RGB(r=0,g=0,b=0)
        self.assertEqual(color.__str__(),"000000")
       
        color = RGB(15, 212, 31)
        self.assertEqual(color.__str__(),"0fd41f")
        
        color = RGB(110, 54, 74)
        self.assertEqual(color.__str__(),"6e364a")
        
        color = RGB(13, 9, 11)
        self.assertEqual(color.__str__(),"0d090b")
        
        
if __name__ == '__main__':
    unittest.main()
    