import queue
import threading
import unittest

from gazepointer.data_message import Data, StopData
from gazepointer.multiplexing import QueueSplitter


class QueueSplitterTest(unittest.TestCase):
    def setUp(self):
        """Setup method to create a QueueSplitter instance before each test."""
        self.input_queue = queue.Queue()
        # Example with two output queues.
        self.output_queues = [queue.Queue() for _ in range(2)]
        self.splitter = QueueSplitter(self.input_queue, self.output_queues)

    def test_initialization(self):
        """Test the initialization of QueueSplitter."""
        self.assertIsInstance(self.splitter.input_queue, queue.Queue)
        self.assertEqual(len(self.splitter.output_queues), 2)
        self.assertIsInstance(self.splitter.output_queues[0], queue.Queue)
        self.assertIsInstance(self.splitter.output_queues[1], queue.Queue)
        self.assertEqual(len(self.splitter.threads), 0)

    def test_start(self):
        """Test the start method of QueueSplitter."""
        self.splitter.start()
        self.assertEqual(len(self.splitter.threads), 1)
        self.assertTrue(isinstance(self.splitter.threads[0], threading.Thread))
        self.assertTrue(self.splitter.threads[0].is_alive())
        self.splitter.stop()

    def test_split_and_stop(self):
        """Test the split functionality and stopping  of QueueSplitter."""
        # Put some data into the input queue.
        test_data = [Data(i) for i in range(3)]

        for item in test_data:
            self.input_queue.put(item)

        # Start the splitter
        self.splitter.start()

        # Stop the splitter
        self.splitter.stop()

        # Check if data is correctly distributed to output queues

        for output_queue in self.output_queues:
            self.assertEqual(output_queue.qsize(), len(test_data))

            for i in range(len(test_data)):
                self.assertIs(output_queue.get(), test_data[i])

         # Ensure that the thread has stopped

        for thread in self.splitter.threads:
            self.assertFalse(thread.is_alive())

if __name__ == '__main__':
    unittest.main()
