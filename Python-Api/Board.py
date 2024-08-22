

import copy
from dataclasses import dataclass, field
import serial
from typing import List, Tuple
from numpy import uint16, uint32, uint8
import time


@dataclass
class RGB:
    """
        Helper class for descrying color
    """
    r: uint8
    g: uint8
    b: uint8
# Todo more colors

    @staticmethod
    def red() :
        return RGB(r=255, g=0, b=0)

    @staticmethod
    def blue() :
        return RGB(r=0, g=0, b=255)
    
    @staticmethod
    def black():
        return RGB(r=0,g=0,b=0)
    
    @staticmethod
    def white():
        return RGB(r = 255,g=255,b=255)
    
    @staticmethod
    def green():
        return RGB(r=0, g=255, b=0)
    
    def __str__(self)->str:
        """
        RGB to string casting in HEX form, output e.g. "ff0000" for color red

        Returns:
            str: collor in HEX encoding in string form 
        """
        str_r = str(hex(self.r))[2:]
        if self.r <= 16: 
            str_r = '0' + str_r
            
        str_g = str(hex(self.g))[2:]
        if self.g <= 16: 
            str_g = '0' + str_g
        
        str_b = str(hex(self.b))[2:]
        if self.b <= 16: 
            str_b = '0' + str_b
        
        return str_r + str_g + str_b

@dataclass(init=False)
class BoardLedStripState:
    BOARD_WIDTH: uint8 = 8
    BOARD_HEIGHT: uint8 = 8
    _led_strip: List[RGB] = None

    def __init__(self, size_w=8, size_h=8, color_list=None, default_color=RGB.white()):
        self.BOARD_WIDTH  = size_h
        self.BOARD_HEIGHT = size_w
        
        if color_list is not None:
            self._led_strip = color_list
        else:
            self._led_strip = []
            for _ in range(self.BOARD_HEIGHT * self.BOARD_WIDTH):
                self._led_strip.append(default_color)
    
    def _translate_addr(self, w, h) -> int:
        if w >= self.BOARD_WIDTH or w < 0:
            raise ValueError("Coordinate out of range: w")
        if h >= self.BOARD_WIDTH or h < 0:
            raise ValueError("Coordinate out of range: h")
        return h * self.BOARD_WIDTH + w

    def set_color(self, w: uint8, h: uint8, color: RGB):
        self._led_strip[self._translate_addr(w, h)] = color
        
    def get_color(self, w: uint8, h: uint8) -> RGB:
        return self._led_strip[self._translate_addr(w, h)]

    def __getitem__(self, i):
        if i < self.BOARD_HEIGHT * self.BOARD_WIDTH:
            return self._led_strip[i]
        raise StopIteration

@dataclass(init=False)
class BoardSquareState:
    BOARD_WIDTH: uint8 = 8
    BOARD_HEIGHT: uint8 = 8
    __squares: List[bool] = field(default_factory=list)

    def __init__(self, size_w: uint8=8, size_h: uint8=8, state_list: List[bool]=None, default_state: bool=False):
        self.BOARD_WIDTH  = size_h
        self.BOARD_HEIGHT = size_w
        if state_list is not None:
            self.__squares = state_list
        else:
            for _ in range(self.BOARD_HEIGHT * self.BOARD_WIDTH):
                self.__squares.append(default_state)
        
    
    def _translate_addr(self, w, h) -> int:
        if w >= self.BOARD_WIDTH or w < 0:
            raise ValueError("Coordinate out of range: w")
        if h >= self.BOARD_WIDTH or h < 0:
            raise ValueError("Coordinate out of range: h")
        return h * self.BOARD_WIDTH + w

    def get_state(self, w: uint8, h: uint8) -> bool:
        return self.__squares[self._translate_addr(w, h)]


class Board:
    
    # TODO make board fields non static
    BOARD_WIDTH: uint8 = 8
    BOARD_HEIGHT: uint8 = 8
    _action_number = None
    _squares: List[bool] = None
    _led_strip: List[RGB] = None

    def __init__(self, device: serial.Serial) -> None:
        """
        Create an Board using specified `device` to communicate with

        Args:
            device (Serial): Serial device used for communication

        """
        self._squares = []
        self._led_strip = []
        for _ in range(self.BOARD_HEIGHT * self.BOARD_WIDTH):
            self._led_strip.append(RGB.red())
            
        for _ in range(self.BOARD_HEIGHT * self.BOARD_WIDTH):
            self._squares.append(False)
        self.arduino = device
        
        if device == None:
            return
        
        arduino_setup = ""
        # todo async clock that will terminate connecting after 30s
       
        print("connecting...")
        while(arduino_setup.find("ready") == -1):
            arduino_setup = str(self.arduino.readline())
            print(arduino_setup)
        print("connection ready\n")
     
    @staticmethod
    def connect_on_port(port: str, baudrate=115200, timeout = 30):
        """
        creates board object connected to arduino board via specified port
        
        Args:
            port (str): COM port id to connect on e.g. "COM3"
            baudrate (int, optional): connection baudrate Defaults to 115200.

        Returns:
            Board: connected board object
        """
        
        return Board(serial.Serial(port=port, baudrate=baudrate,timeout=timeout))
    
    def __str__(self)->str:
        """
        convert board to str for debug proposes

        Returns:
            str: converted boar 
        """
        output = "\n"
        for x in range(self.BOARD_HEIGHT):
            
            for y in range(self.BOARD_WIDTH):
                output = " "+ output + str(self._led_strip[self.conv_1_d((x,y))]) + " "
            
            output+='\n'
            
            for y in range(self.BOARD_WIDTH):
                if self._squares[self.conv_1_d((x,y))]:
                    output = output +"  "+"ON"+"   "
                else:
                    output = output +"  "+"OFF"+"  "
            output+='\n'
            
        # las character is new line, we don't want that 
        # so return everything but last character
        return output[:-1]
    
    def set_chess_colors(self, white_color:RGB = RGB.white(), black_color:RGB = RGB.black()):
        flip = True
        for h in range(self.BOARD_HEIGHT):
            for w in range(self.BOARD_WIDTH):
                if(h%2==0):
                    if(w%2==0):
                        self._led_strip[w * 8 + h] = white_color
                    else:
                        self._led_strip[w * 8 + h] = black_color
                else:
                    if (w%2==1):
                        self._led_strip[w * 8 + h] = white_color
                    else:
                        self._led_strip[w * 8 + h] = black_color
        
        
    def chess_animation(self,white_color:RGB = RGB.white(), black_color:RGB = RGB.black()):
        for h in range(self.BOARD_HEIGHT):
            for w in range(self.BOARD_WIDTH):
                
                self._led_strip[w * 8 + h] = RGB.white()
                
                time.sleep(0.1)

                # flip = not flip
    
    def fill_w_color(self,new_collor:RGB)->None:
        """
        overrides every led with specified new_collor

        Args:
            new_collor (RGB): color to which every led will be converted 
        """
        for id, _ in enumerate(self._led_strip):
            self._led_strip[id] = new_collor

    def __decode_payload(payload:str)->str:
        # ToDo define errors detected by arduino board and map every with unique flag 
        """
        separates and acts on error flags from button state array

        Args:
            payload (str): _description_
            
        Returns:
            str: square states 
        """
        
        return payload
    
    def display_from_board_led_strip_state(self, board_state:BoardLedStripState)->None:
        assert(type(board_state) == BoardLedStripState)
        assert(board_state.BOARD_HEIGHT == self.BOARD_HEIGHT)
        assert(board_state.BOARD_WIDTH == self.BOARD_WIDTH)    
        assert(len(board_state._led_strip) == len(self._led_strip))
        
        update_board = board_state._led_strip != self._led_strip
        
        #if board state didn't change do nothing
        if not update_board:
            return 
        
        self._led_strip = copy.deepcopy(board_state._led_strip)
        self.display()
    
    def display(self) -> None:
        """
        Update Arduino chessboard colors with new ones 
        """
        if self.arduino is not None:
            
            message = self.generate_led_state()
            print("\n\n\n")
            print(message)
            print("\n")
            self.arduino.write(bytes("set" + message + "\n", 'utf-8'))
            result = str(self.arduino.readline())
            print(result)
            print("\n\n\n")
            if(result.find("ok") == -1):
                raise Exception(result)
            
            
            
    def get_board_led_strip_state(self)->BoardLedStripState:
        return BoardLedStripState(size_w = self.BOARD_WIDTH,
                                  size_h= self.BOARD_HEIGHT,
                                  color_list=copy.deepcopy(self._led_strip))
    def get_board_square_state(self)->BoardSquareState:
        return BoardSquareState(size_w = self.BOARD_WIDTH,
                                  size_h= self.BOARD_HEIGHT,
                                  state_list=copy.deepcopy(self._squares))
    def read_voltage(self)->None:
        if self.arduino is not None:
            self.arduino.write(bytes("get\n", 'utf-8'))
   
        payload = str(self.arduino.readline())
   
        if(payload.find("ok") == -1):
                raise Exception(payload)
    
        
        read_square_states = payload[4:-3] 
    
        print(read_square_states,end='\n')
    
    def read_board(self) -> None:
        """
        Update board with reading from Arduino
        """
        
        if self.arduino is not None:
            self.arduino.write(bytes("get\n", 'utf-8'))
            
            payload = str(self.arduino.readline())
            
            read_square_states = payload[2:-3]#self.__decode_payload(payload[:-1])
            
            parsed_square_states = read_square_states.split(' ')

            self._action_number = int(read_square_states[-1])

            for i in range(self.BOARD_HEIGHT*self.BOARD_WIDTH):
                if parsed_square_states[i] == '1':
                    self._squares[i] = True
                elif parsed_square_states[i] == '0':
                    self._squares[i] = False
                else:
                    raise Exception("invalid character :>" +str(parsed_square_states[i])+"<")
    
    @property
    def action_number(self)->uint32:
        """
        current __action_number getter
   
        Returns:
            uint32: __action_number
        """
        return self._action_number
    
    def close_connection(self)->None:
        """
            close connection to arduino device
            should be run before closing app
        """
        if self.arduino is not None:
            self.arduino.close()

    def generate_led_state(self)->str:
        state = ""
        for led in self._led_strip:
            state += str(led) + ' '
        return state
    
        
        
    def __getitem__(self, position: Tuple[uint8, uint8]) -> Tuple[RGB, bool]:
        """getter for state of specied square 

        Args:
            position (Tuple[uint8, uint8]): position in question

        Returns:
            Tuple[RGB, bool]: color and occupation of square (in that order) 
        """
        position_1_d = self.conv_1_d(position)
        return (self._led_strip[position_1_d], self._squares[position_1_d])

    def __setitem__(self, position: Tuple[uint8, uint8], color: RGB) -> None:
        """settor for specied square color 

        Args:
            position (Tuple[uint8, uint8]): position of square in question
            color (RGB): new collor of square
        """
        position_1_d = self.conv_1_d(position)
        self._led_strip[position_1_d] = color

    
    def conv_1_d(self, position_2_d: Tuple[uint8, uint8]) -> uint16:
        """
        convert point in 2 dimension space to point in one dimension space

        Args:
            position_2_d (Tuple[uint8, uint8]): pair of values (length in x dimension, length in y dimension )

        Raises:
            Exception: Incorrect position, passed value is incorrect

        Returns:
            uint16: point in one dimension space
        """
        if position_2_d[0] > self.BOARD_HEIGHT or position_2_d[1] > self.BOARD_WIDTH:
            raise Exception("Incorrect position")

        return self.BOARD_HEIGHT*position_2_d[0] + position_2_d[1]
    
