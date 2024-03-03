import queue
import unittest

from gazepointer.debugging_module import DebuggingModule
from gazepointer.keypoint_module import KeypointModule
from gazepointer.multiplexing import QueueAggregator, QueueSplitter
from gazepointer.pnp_module import PnPModule


class TestPnP(unittest.TestCase):

    def setUp(self):
        self.keypoint_output_queue = queue.Queue()
        self.keypoint_intermediate_queue = queue.Queue()
        self.debug_input_queue = queue.Queue()
        self.pnp_input_queue = queue.Queue()
        self.pnp_output_queue = queue.Queue()
        self.debug_input_aggregator = QueueAggregator(
            input_queues=[self.keypoint_intermediate_queue, self.pnp_output_queue],
            output_queue=self.debug_input_queue,
        )
        self.keypoint_output_splitter = QueueSplitter(
            input_queue=self.keypoint_output_queue,
            output_queues=[self.keypoint_intermediate_queue, self.pnp_input_queue],
        )
        self.keypoint_module = KeypointModule(output_queue=self.keypoint_output_queue)
        self.debug_module = DebuggingModule(input_queue=self.debug_input_queue)
        self.pnp_module = PnPModule(
            input_queue=self.pnp_input_queue, output_queue=self.pnp_output_queue
        )



