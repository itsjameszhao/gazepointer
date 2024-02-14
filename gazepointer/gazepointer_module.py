"""Defines the Module class for GazePointer data processing"""

import queue
import threading
from abc import ABC, abstractmethod
from typing import Optional

from gazepointer.data_message import Data


class GazePointerModule(ABC):
    """A module to be used in our image processing pipeline"""

    def __init__(
        self,
        input_queue: Optional[queue.Queue] = None,
        output_queue: Optional[queue.Queue] = None,
    ) -> None:
        self.input_queue: Optional[queue.Queue] = input_queue
        self.output_queue: Optional[queue.Queue] = output_queue
        self.stop_event: threading.Event = threading.Event()
        # Add a thread attribute
        self.thread: Optional[threading.Thread] = None

    @abstractmethod
    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        """Data processing logic, needs to be implemented in subclass"""

    def _run(self) -> None:
        """The original start logic that runs in a separate thread"""
        print("Starting module...")

        while not self.stop_event.is_set():
            try:
                data: Optional[Data] = (
                    self.input_queue.get(block=True, timeout=0.1)
                    if self.input_queue
                    else None
                )
            except queue.Empty:
                continue
            result: Optional[Data] = self.process_function(data)

            if self.output_queue:
                try:
                    self.output_queue.put(result, block=False)
                except queue.Full:
                    print(f"Output queue for {self.__class__.__name__} full")

    def start(self, use_thread=True) -> None:
        """Starts the data processing module in a separate thread"""

        if use_thread: 
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
            print("Module started in a new thread.")
        
        else:
            self._run()

    def stop(self) -> None:
        """Stop the data processing module"""
        print("Stopping module...")
        self.stop_event.set()

        if self.thread:
            self.thread.join()  # Wait for the thread to finish
