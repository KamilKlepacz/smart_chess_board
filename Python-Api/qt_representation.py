import logging
import math
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from typing import List 
from PyQt5.QtCore import *

from BoardWorker import *

from Board import *

BOARD_HEIGHT = 8
BOARD_WIDTH = 8

class BoardWindow():
    _button_states = []
    _device_process = ProcessHandler(DeviceWorker(None))
    _reverse_process = ProcessHandler(ReverseWorker())
    
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.widget = QWidget()
        self.layoutGrid = QGridLayout()
        self.buttonGroup = QButtonGroup()

        self.widget.setGeometry(80, 80,2+8*82,2+8*82)
        self.widget.setStyleSheet("background-color : black")
        self.widget.setWindowTitle("Board")
        
        self._device_process.start()
        self._reverse_process.start()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_update)
        self.timer.setInterval(500) #.5 seconds
        self.timer.start()
        
        
        self.buttonGroup.idClicked.connect(self.cycle_color)
        self.widget.setLayout(self.layoutGrid)
        
        for x in range(BOARD_HEIGHT):
            for y in range(BOARD_WIDTH):
                button = QPushButton()
                button.setStyleSheet("background-color: red")
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.layoutGrid.addWidget(button, x,y)
                self.buttonGroup.addButton(button, x*BOARD_WIDTH+y)
                self._button_states.append(0)
                
        self.widget.show()
        self.app.exec()

    def on_update(self):
        logging.debug("Updating")
        active_fields = self._device_process.update(BoardLedStripState(default_color=RGB.blue))
        logging.debug(f"Active fields: {active_fields}")
        
        if active_fields == None:
            return
        
        colors = self._reverse_process.update(active_fields)

        if colors != None:
            self.update_qui_colors(colors)
            
    def close(self):
        self._device_process.close()
        self._reverse_process.close()
        
    def rainbow(self, p , max):
        
        third = p // (max // 3)
        
        if third == 0:
            
            height_in_radians = p * math.pi  / (max / 3) / 2
            
            return (math.cos(height_in_radians) * 255, math.sin(height_in_radians) * 255,0)
        
        if third == 1:
            
            p -= max//3
            
            height_in_radians = p * math.pi  / (max / 3) / 2
            
            return(0, math.cos(height_in_radians) * 255,
                    math.sin(height_in_radians) * 255)
        
        if third == 2:
            
            p -=(2 * max)//3
            
            height_in_radians = p * math.pi  / (max / 3) / 2
            
            return(math.sin(height_in_radians) * 255, 0,
                    math.cos(height_in_radians) * 255)


    # def turn_on_chess(self):
    #     self.board_handle.set_chess_colors()
    #     self.update_qui()
    #     self.board_handle.display()
    #     self.widget.show()
        
        
    # def turn_on_chess_animation(self):
    #     for i in range (10):
    #         self.board_handle.set_chess_colors(white_color=RGB.black(),black_color=RGB.white())
    #         self.update_qui()
    #         self.board_handle.display()
    #         self.widget.show()
    #         time.sleep(1)

            
    #         self.board_handle.set_chess_colors(white_color=RGB.white(),black_color=RGB.black())
    #         self.update_qui()
    #         self.board_handle.display()
    #         self.widget.show()
    #         time.sleep(1)
            
            
    def cycle_color(self,idClicked):
        return
        self._button_states[idClicked] += 1
        
        if self._button_states[idClicked] == 12:
            self._button_states[idClicked] = 0
        
        color =  self.rainbow( self._button_states[idClicked],12)
        self.board_handle._led_strip[idClicked] = RGB(round(color[0]), round(color[1]), round(color[2]))
        color = self.board_handle._led_strip[idClicked]
        print(str(color))
        self._buttons[idClicked].setStyleSheet(f"background-color : rgb({color.r},{color.g},{color.b})")
        self.board_handle.display()
        self.widget.show()
        
    def update_qui_colors(self,board_led_strip_state : BoardLedStripState):
        for index in range(self.layoutGrid.count()):
            color = board_led_strip_state._led_strip[index]
            self.layoutGrid.itemAt(index).widget().setStyleSheet(f"background-color : rgb({color.r},{color.g},{color.b})")
        
        logging.debug(f"update_qui_colors: {self.layoutGrid.itemAt(0).widget()}")
        self.widget.update()
      
def main():
    """
    sync board indefinitely  
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("heellooo")
    try:
        window = BoardWindow()
    except KeyboardInterrupt:
        window.close()
        del window

if __name__ == "__main__":
    main()
