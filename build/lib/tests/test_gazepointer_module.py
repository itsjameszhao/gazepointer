import queue
import threading
import unittest
from typing import Optional
from unittest.mock import MagicMock

from gazepointer.gazepointer_module import Data, GazePointerModule

# A concrete implementation of GazePointerModule for testing


class TestGazePointerModule(GazePointerModule):
    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        # For testing, simply return the input data

        return input_data


class GazePointerModuleTests(unittest.TestCase):
    def setUp(self):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.module = TestGazePointerModule(self.input_queue, self.output_queue)

    def test_process_function_called_with_data(self):
        # Test that process_function is called with the correct data
        data = Data()
        self.input_queue.put(data)
        self.module.process_function = MagicMock(return_value=data)
        self.module.start()
        self.module.stop()
        self.module.process_function.assert_called_with(data)

    def test_output_queue_receives_processed_data(self):
        # Test that the output queue receives the processed data
        data = Data()
        self.input_queue.put(data)
        self.module.start()
        processed_data = self.output_queue.get(timeout=2)
        self.module.stop()
        self.assertEqual(processed_data, data)

    def test_module_stops_gracefully(self):
        # Test that the module stops gracefully when
        self.assertFalse(self.module.stop_event.is_set())
        self.module.start()
        self.module.stop()
        self.assertTrue(self.module.stop_event.is_set())

    def test_output_queue_full_handled_gracefully(self):
        # Test that the module handles a full output queue gracefully
        self.input_queue.put(Data())
        self.input_queue.put(Data())
        self.module.output_queue = MagicMock()
        self.module.output_queue.full.side_effect = [True, False]
        self.module.start()
        self.module.stop()
        # Check that the module tried to put data into the full queue and handled the exception
        self.module.output_queue.put.assert_called()


if __name__ == "__main__":
    unittest.main()
