import queue
import unittest

from gazepointer.debugging_module import DebuggingModule
from gazepointer.keypoint_module import KeypointModule


class TestKeypointDisplay(unittest.TestCase):

    def setUp(self):
        self.keypoint_queue = queue.Queue()
        self.keypoint_module = KeypointModule(output_queue=self.keypoint_queue)
        self.debug_module = DebuggingModule(input_queue=self.keypoint_queue)

    def test_display_keypoints(self):
        try:
            self.keypoint_module.start()
            self.debug_module.start(use_thread=False)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            self.debug_module.stop()
            self.keypoint_module.stop()


if __name__ == "__main__":
    unittest.main()
