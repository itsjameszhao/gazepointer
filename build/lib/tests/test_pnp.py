import queue
import unittest

from gazepointer.debugging_module import DebuggingModule
from gazepointer.keypoint_module import KeypointModule
from gazepointer.multiplexing import QueueSplitter
from gazepointer.pnp_module import PnPModule


class TestPnP(unittest.TestCase):

    def setUp(self):
        self.keypoint_output_queue = queue.Queue()
        self.debug_input_queue = queue.Queue()
        self.pnp_input_queue = queue.Queue()
        self.keypoint_output_splitter = QueueSplitter(
            input_queue=self.keypoint_output_queue,
            output_queues=[self.debug_input_queue, self.pnp_input_queue],
        )
        self.keypoint_module = KeypointModule(output_queue=self.keypoint_output_queue)
        self.debug_module = DebuggingModule(input_queue=self.debug_input_queue)
        self.pnp_module = PnPModule(input_queue=self.pnp_input_queue)

    def test_display_keypoints(self):
        self.pnp_module.start()
        self.keypoint_module.start()
        self.keypoint_output_splitter.start()
        self.debug_module.start(use_thread=False)


if __name__ == "__main__":
    unittest.main()
