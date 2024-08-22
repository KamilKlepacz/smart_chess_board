from asyncio.log import logger
from itertools import count
from typing import Any, Optional
from abc import ABC, abstractmethod
import time
import logging
from multiprocessing.sharedctypes import Value

from Board import Board, BoardLedStripState
from multiprocessing import Process, Queue
from dataclasses import dataclass

from Board import *
class IWorker(ABC):
    @abstractmethod
    def update_state(self, sate):
        pass

    @abstractmethod
    def close(self):
        pass

@dataclass(init=False)
class DeviceWorker(IWorker):
    board_device: Board
    
    def __init__(self, port) -> None:
        if(port != None):
            self.board_device = Board.connect_on_port(port)
        else:
            self.board_device = Board(None)
    def update_state(self, state):
        try:
            if state is not None:
                logging.debug("displaying new colors")
                self.board_device.display_from_board_led_strip_state(state)
            logging.debug("Pooling board state")
            return self.board_device.get_board_square_state()
        except Exception as e:
            logging.error(f"Device error:\n {e}")
            return None
    
    def close(self):
        self.board_device.close_connection()
    
    # def __del__(self):
    #     self.close()

@dataclass(init=False)
class ReverseWorker(IWorker):
    active_color = RGB.white()
    background_color = RGB.black()

    def update_state(self, state):
        out = BoardLedStripState()
        for x in range(state.BOARD_WIDTH):
            for y in range(state.BOARD_WIDTH):
                if state.get_state(x, y):
                    out.set_color(x,y, self.active_color)
                else:
                    out.set_color(x,y, self.background_color)
        time.sleep(10)
        self.active_color, self.background_color = self.background_color, self.active_color
        return out

    def close(self):
        logging.debug("c@")
        pass
    
    def __del__(self):
        pass

@dataclass(init=False)
class ProcKiller(IWorker):
    count = 0
    def update_state(self, state):
        while True:
                self.count+=1
                # print(self.count)
        return 1
    
    def close(self):
        logging.debug("c@ ")
        pass
    
    
def f(inputs: Queue, outputs: Queue, worker: IWorker, should_close):
    while should_close.value != 1:
        if not inputs.empty():
            logging.debug("Input recived")
            outputs.put_nowait(worker.update_state(inputs.get_nowait()))
        time.sleep(1/60)
    worker.close()
    
@dataclass(init=False)
class ProcessHandler:
    _worker: IWorker
    _process: Process
    _inputs : Queue
    _outputs: Queue
    _should_close: Value
    def __init__(self, worker: IWorker) -> None:
        self._inputs = Queue()
        self._outputs = Queue()
        self._should_close = Value('i', 0)
        self._worker = worker
        self._process = Process(target=f, args=(self._inputs, 
                                                 self._outputs, 
                                                 self._worker, 
                                                 self._should_close))
        
        
    def update(self, state: Any) -> Optional[Any]:
        self.set(state)
        return self.get()
    
    def get(self)-> Optional[Any]:
        if self._outputs.empty():
            return None
        return self._outputs.get_nowait()

    def set(self,state:Any)->None:
        self._inputs.put_nowait(state)

    def start(self):    
        self._process.start()

    def close(self):
        self._should_close.value = 1

        # self._process.close()
        # self._process.kill
        # self._process.terminate()
        
    def __del__(self):
        self.close()
