from typing import Optional

import cv2

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class DebuggingModule(GazePointerModule):
    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:

       if input_data:
            if input_data.header == "keypoints":
                self.display_keypoints(input_data)

        return None

    def display_keypoints(self, keypoint_data: Data) -> None:
        shape_np = keypoint_data.payload['shape_np']
        frame = keypoint_data.payload['frame']

        # TODO add thread-safe video feed keypoint display
        print(shape_np)

        return None
