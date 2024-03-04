import queue
import unittest

from gazepointer.debugging_module import DebuggingModule
from gazepointer.kalman2d_module import Kalman3DModule
from gazepointer.keypoint_module import KeypointModule
from gazepointer.multiplexing import QueueAggregator, QueueSplitter
from gazepointer.pnp_module import PnPModule
from gazepointer.projection_module import ProjectionModule


class TestPnP(unittest.TestCase):

    def setUp(self):
        # Set up queues
        self.keypoint_output_queue = queue.Queue()
        self.keypoint_intermediate_queue = queue.Queue()

        self.pnp_input_queue = queue.Queue()
        self.pnp_output_queue = queue.Queue()
        self.pnp_intermediate_queue = queue.Queue()

        self.kalman_input_queue = queue.Queue()
        self.kalman_output_queue = queue.Queue()
        self.kalman_intermediate_queue = queue.Queue()

        self.projection_input_queue = queue.Queue()
        self.projection_output_queue = queue.Queue()

        self.debug_input_queue = queue.Queue()

        # Set up keypoint module
        self.keypoint_output_splitter = QueueSplitter(
            input_queue=self.keypoint_output_queue,
            output_queues=[self.keypoint_intermediate_queue, self.pnp_input_queue],
        )
        self.keypoint_module = KeypointModule(output_queue=self.keypoint_output_queue)

        # Set up PnP module
        self.pnp_output_splitter = QueueSplitter(
            input_queue=self.pnp_output_queue,
            output_queues=[self.pnp_intermediate_queue, self.kalman_input_queue],
        )
        self.pnp_module = PnPModule(
            input_queue=self.pnp_input_queue, output_queue=self.pnp_output_queue
        )

        # Set up Kalman module
        self.kalman_output_splitter = QueueSplitter(
            input_queue=self.kalman_output_queue,
            output_queues=[self.kalman_intermediate_queue, self.projection_input_queue],
        )
        self.kalman3d_module = Kalman3DModule(
            input_queue=self.kalman_input_queue, output_queue=self.kalman_output_queue
        )

        # Set up projection module
        self.projection_module = ProjectionModule(
            input_queue=self.projection_input_queue,
            output_queue=self.projection_output_queue,
        )

        # Set up debugging module
        self.debug_input_aggregator = QueueAggregator(
            input_queues=[
                self.keypoint_intermediate_queue,
                self.pnp_intermediate_queue,
                self.kalman_intermediate_queue,
                self.projection_output_queue,
            ],
            output_queue=self.debug_input_queue,
        )
        self.debug_module = DebuggingModule(input_queue=self.debug_input_queue)

    def test_display_keypoints(self):
        try:
            self.keypoint_module.start()
            self.keypoint_output_splitter.start()
            self.pnp_module.start()
            self.pnp_output_splitter.start()
            self.kalman3d_module.start()
            self.kalman_output_splitter.start()
            self.projection_module.start()

            self.debug_input_aggregator.start()
            self.debug_module.start(use_thread=False)
        except KeyboardInterrupt:
            self.debug_module.stop()
            self.debug_input_aggregator.stop()
            self.projection_module.stop()
            self.kalman_output_splitter.stop()
            self.kalman3d_module.stop()
            self.pnp_output_splitter.stop()
            self.pnp_module.stop()
            self.keypoint_output_splitter.stop()
            self.keypoint_module.stop()


if __name__ == "__main__":
    unittest.main()
