import queue
import unittest

from gazepointer.data_message import Data
from gazepointer.screen_module import ScreenModule


class TestKeypointDisplay(unittest.TestCase):

    def setUp(self):
        self.screen_queue = queue.Queue()
        self.screen_module = ScreenModule(input_queue=self.screen_queue)

    def test_screen_module(self):
        try:
            # put Data in the screen queue and test that it works on the screen
            for i in range(10):
                self.screen_queue.put(Data(header="screen", payload=[100, 200]))
                self.screen_queue.put(Data(header="screen", payload=[110, 220]))
                self.screen_queue.put(Data(header="screen", payload=[130, 240]))
                self.screen_queue.put(Data(header="screen", payload=[140, 260]))
                self.screen_queue.put(Data(header="screen", payload=[150, 280]))
                self.screen_queue.put(Data(header="screen", payload=[200, 300]))
                self.screen_queue.put(Data(header="mouse", payload="click"))
                self.screen_queue.put(Data(header="screen", payload=[300, 400]))

            self.screen_module.start()
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            self.screen_module.stop()


if __name__ == "__main__":
    unittest.main()
