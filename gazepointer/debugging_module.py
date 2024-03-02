import os
import time
from typing import Optional

import cv2

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class DebuggingModule(GazePointerModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Controls the frequency of print statements
        self.last_print_time = time.time()

        # Specify how frquently to print in seconds
        self.print_interval = 0.5

        # Template for debugging
        self.debugging_template = ""

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if not input_data:
            return None

        if input_data.header == "keypoint":
            keypoint_str = f"Keypoint shape: {input_data.payload['face_2d'].shape}"
            self.debugging_template += "\n" + keypoint_str
            self.display_keypoints(input_data)

        elif input_data.header == "pnp":
            angle_x = input_data.payload["angle_x"]
            angle_y = input_data.payload["angle_y"]
            angle_z = input_data.payload["angle_z"]
            disp_x = input_data.payload["disp_x"]
            disp_y = input_data.payload["disp_y"]
            disp_z = input_data.payload["disp_z"]
            pnp_str = f"Raw angles: x: {angle_x}, y: {angle_y}, z: {angle_z} displacements: x: {disp_x}, y: {disp_y}, z: {disp_z}"
            self.debugging_template += "\n" + pnp_str

        elif input_data.header == "kalman":
            angle_x = input_data.payload["angle_x"]
            angle_y = input_data.payload["angle_y"]
            angle_z = input_data.payload["angle_z"]
            disp_x = input_data.payload["disp_x"]
            disp_y = input_data.payload["disp_y"]
            disp_z = input_data.payload["disp_z"]
            kalman_str = f"Filtered angles: x: {angle_x}, y: {angle_y}, z: {angle_z} displacements: x: {disp_x}, y: {disp_y}, z: {disp_z}"
            self.debugging_template += "\n" + kalman_str

        elif self.input_data.header == "projection":
            x_px = input_data.payload["x_px"]
            y_px = input_data.payload["y_px"]
            projection_str = f"Projection: x: {x_px}, y: {y_px}"
            self.debugging_template += "\n" + projection_str
            self.display_point(x_px, y_px)

        elif self.input_data.header == "screen":
            pass  # TODO

        elif self.input_data.header == "control":
            pass  # TODO

        if time.time() - self.last_print_time > self.print_interval:
            self.last_print_time = time.time()
            os.system("clear")
            self.sort_debugging_template()
            print(self.debugging_template)
            self.debugging_template = ""

        return None

    def sort_debugging_template(self):
        # Split the string into a list of lines
        lines = self.debugging_template.split("\n")
        # Sort the list
        lines.sort()
        # Join the list back into a string
        self.debugging_template = "\n".join(lines)

    def display_keypoints(self, keypoint_data: Data) -> None:
        face_2d = keypoint_data.payload["face_2d"]
        frame = keypoint_data.payload["frame"]
        height, width = frame.shape[:2]

        # Overlay keypoints on the frame

        for i, (x, y) in enumerate(face_2d):
            # Draw a circle at each point
            # Assuming you want to complete the color as green with full fill
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

            # Display the index 'i' near each point
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                frame,
                str(i),
                (int(x) + 5, int(y) - 5),
                font,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

        cv2.imshow("Video Feed", frame)
        cv2.waitKey(1)

    def display_point(self, x_px: int, y_px: int) -> None:
        """Display the gaze point on the screen"""
