import queue
import unittest

from gazepointer.keypoint_module import ScreenModule


class TestKeypointDisplay(unittest.TestCase):

    def setUp(self):
        self.screen_queue = queue.Queue()
        self.screen_module = ScreenModule(input_queue=self.keypoint_queue)

    def test_screen_module(self):
        try:
            # TODO put Data in the screen queue and test that it works on the screen
            self.screen_module.start()
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            self.screen_module.stop()


if __name__ == "__main__":
    unittest.main()
