import math
from typing import Optional

import cv2
import numpy as np

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class PnPModule(GazePointerModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_points = np.array(
            [
                (0.0, 0.0, 0.0),
                (0.0, -330.0, -65.0),
                (-225.0, 170.0, -135.0),
                (225.0, 170.0, -135.0),
                (-150.0, -150.0, -125.0),
                (150.0, -150.0, -125.0),
            ]
        )
        self.dlib_indices = {
            "NOSE_TIP": 33,
            "CHIN": 8,
            "LEFT_EYE_LEFT_CORNER": 45,
            "RIGHT_EYE_RIGHT_CORNER": 36,
            "LEFT_MOUTH_CORNER": 54,
            "RIGHT_MOUTH_CORNER": 48,
        }
        self.frame_width = 1280  # Empirically determined
        self.frame_height = 720  # Empirically determined
        self.horizontal_fov_deg = 78  # Estimated value of most webcams
        # Based on https://shorturl.at/kmqAX
        self.focal_length = self.frame_width / (
            2 * math.tan(self.horizontal_fov_deg / 2)
        )  # Estimated value in pixels
        # All values of the camera matrix expressed in pixels
        self.camera_matrix = np.array(
            [
                [self.focal_length, 0, self.frame_width / 2],
                [0, self.focal_length, self.frame_height / 2],
                [0, 0, 1],
            ],
            dtype="double",
        )
        self.dist_coeffs = np.zeros((4, 1))

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:

        # Check to see that the messages are correct

        if input_data:
            assert (
                input_data.header == "keypoints"
            ), "Error: PnP module input data incorrect"

            shape_np = input_data.payload["shape_np"]
            image_points = np.array(
                [shape_np[i] for i in self.dlib_indices.values()], dtype="double"
            )
            success, rotation_vector, translation_vector = cv2.solvePnP(
                self.model_points,
                image_points,
                self.camera_matrix,
                self.dist_coeffs,
                flags=cv2.SOLVEPNP_ITERATIVE,
            )

            if success:
                print("Solve PnP success")
                print(f"Rotation vector is {rotation_vector}")
                print(f"Translation vector is {translation_vector}")
            else:
                print("Failed to solve PnP")

        return None
