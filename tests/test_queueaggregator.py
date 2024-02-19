import unittest
from queue import Queue
from unittest.mock import patch

from gazepointer.data_message import Data
from gazepointer.multiplexing import QueueAggregator


class TestQueueAggregator(unittest.TestCase):
    def setUp(self):
        """Setup method to create queues and QueueAggregator instance before each test"""
        self.input_queues = [Queue() for _ in range(2)]
        self.output_queue = Queue()
        self.aggregator = QueueAggregator(self.input_queues, self.output_queue)

    def test_initialization(self):
        """Test the initialization of QueueAggregator"""
        self.assertEqual(len(self.aggregator.input_queues), 2)
        self.assertIs(self.aggregator.output_queue, self.output_queue)
        self.assertEqual(len(self.aggregator.threads), 0)

    @patch("threading.Thread.start")
    def test_start(self, mock_start):
        """Test starting the aggregator"""
        self.aggregator.start()
        self.assertEqual(len(self.aggregator.threads), 2)
        mock_start.assert_called()

    def test_aggregate_and_stop(self):
        """Test data aggregation and stopping the aggregator"""
        # Put some data in the input queues

        for i, input_queue in enumerate(self.input_queues):
            for j in range(3):
                input_queue.put(Data(header=f"Data {i}-{j}"))

        # Start the aggregator
        self.aggregator.start()

        # Wait for the aggregator to finish
        self.aggregator.stop()

        # Check if all data has been moved to the output queue
        output_data = []

        while not self.output_queue.empty():
            output_data.append(self.output_queue.get().header)

        expected_data = [f"Data {i}-{j}" for i in range(2) for j in range(3)]
        self.assertEqual(sorted(output_data), sorted(expected_data))


if __name__ == "__main__":
    unittest.main()
