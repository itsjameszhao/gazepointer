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
        shape_np = keypoint_data.payload["shape_np"]
        frame = keypoint_data.payload["frame"]
        height, width = frame.shape[:2]

        # Overlay keypoints on the frame
        for i, (x, y) in enumerate(shape_np):
            # Draw a circle at each point
            # Assuming you want to complete the color as green with full fill
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

            # Display the index 'i' near each point
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(i), (int(x) + 5, int(y) - 5),
                        font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
        cv2.imshow('Video Feed', frame)
        cv2.waitKey(1)