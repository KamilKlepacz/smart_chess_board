""" connection example file

"""
from Board import *
import time


def led_example()->None:
    board = Board(None)
    
    for x in range(8):
        for y in range(8):
    
            print(str(board))
            board.fill_w_color(RGB.green())# clean display with black color

            board[(x,y)] = RGB.red() # update board display

            board.display() # send update to arduino board
            board.read_board() # get current board state from arduino 
            time.sleep(1) # wait for second 
    
    board.close_connection()

def button_matrix_example()->None:
    board = Board.connect_on_port("COM3")
    while(True):
        board.read_board()
        print(str(board))
        time.sleep(1)
    
    
def serial_monitor(port:str,baudrate=115200)->None:
    arduino = serial.Serial(port=port, baudrate=baudrate,timeout = 30)
    arduino_setup = ''
    print("connecting...")
    while(arduino_setup.find("ready") == -1):
        arduino_setup = str(arduino.readline())
        print(arduino_setup)
    print("connection ready\n")
    
    while(True):
        arduino.write(bytes("ok\n", 'utf-8'))
        payload = str(arduino.readline())
        print(payload)
        
        
        
def led_connection(port:str)->None:    
    board = Board.connect_on_port(port)
    while(True):
        for x in range(2):
            for y in range(2):
            
                print(str(board))
                board.fill_w_color(RGB.green())# clean display with green color
                board[(x,y)] = RGB.red() # update board display

                board.display() # send update to arduino board
                # board.update_board() # get current board state from arduino 
                time.sleep(1) # wait for second 



def full_connection(port:str)->None:
    board = Board.connect_on_port(port)
    while(True):
        for x in range(board.BOARD_HEIGHT):
            for y in range(board.BOARD_WIDTH):
            
                print(str(board))
                
                board.display() 
                board.read_voltage() 
                
                
                board.fill_w_color(RGB.white())
                board[(x,y)] = RGB.red()
                
                time.sleep(1) 
    
    board.close_connection()

def chess_colors(port:str)->None:
    board = Board.connect_on_port(port)
    board.set_chess_colors()
    board.display() 
    
if __name__ == "__main__":
    # led_example()
    # button_matrix_example()
    # serial_monitor("COM3")
    # led_connection("COM3")
    full_connection("COM3")
    # chess_colors("COM3")
    