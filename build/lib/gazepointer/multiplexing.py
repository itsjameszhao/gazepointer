"""Tools for splitting and aggregating Data message"""

import queue
import threading
from typing import List

from gazepointer.data_message import Data, StopData


class QueueAggregator:
    """Class to combine data from multiple queues into one"""

    def __init__(
        self, input_queues: List[queue.Queue], output_queue: queue.Queue
    ) -> None:
        self.input_queues: List[queue.Queue] = input_queues
        self.output_queue: queue.Queue = output_queue
        self.threads = List[threading.Thread] = []

    def start(self) -> None:
        """Starts the QueueAggregator, combining queues"""

        for input_queue in self.input_queues:
            thread = threading.Thread(target=self.aggregate, args=(input_queue,))
            thread.start()
            self.threads.append(thread)

    def aggregate(self, input_queue: queue.Queue) -> None:
        """Aggregates data from multiple queues together"""

        while True:
            data: Data = input_queue.get(block=True)

            if isinstance(data, StopData):
                break
            try:
                self.output_queue.put(data, block=False)
            except queue.Full:
                print(f"Output queue for {self.__class__.__name__} full")

    def stop(self) -> None:
        """Stops the operation of the QueueAggregator"""

        for input_queue in self.input_queues:
            input_queue.put(StopData(), block=True)

        for thread in self.threads:
            thread.join()


class QueueSplitter:
    """Class to multiplex a queue"""

    def __init__(
        self, input_queue: queue.Queue, output_queues: List[queue.Queue]
    ) -> None:
        self.input_queue: queue.Queue = input_queue
        self.output_queues: List[queue.Queue] = output_queues
        self.threads = List[threading.Thread] = []

    def start(self) -> None:
        """Splits data from one queue into multiple"""

        while True:
            data: Data = self.input_queue.get(block=True)

            if isinstance(data, StopData):
                break

            for output_queue in self.output_queues:
                try:
                    output_queue.put(data, block=False)
                except queue.Full:
                    print(f"Output queue for {self.__class__.__name__} full")

    def stop(self) -> None:
        """Stops the operation of the QueueSplitter"""
        self.input_queue.put(StopData(), block=True)

        for thread in self.threads:
            thread.join()
