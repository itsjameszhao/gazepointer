import math
from typing import Optional, Tuple

import cv2
import numpy as np

from gazepointer.config import (
    CAMERA_HEIGHT_ABOVE_SCREEN_METERS,
    SCREEN_DIAGONAL_SIZE_METERS,
    SCREEN_HEIGHT_PX,
    SCREEN_WIDTH_PX,
)
from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class ProjectionModule(GazePointerModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        screen_diagonal_size_px = math.sqrt(SCREEN_WIDTH_PX**2 + SCREEN_HEIGHT_PX**2)
        screen_width_meters = (
            SCREEN_DIAGONAL_SIZE_METERS * SCREEN_WIDTH_PX / screen_diagonal_size_px
        )
        screen_height_meters = (
            SCREEN_DIAGONAL_SIZE_METERS * SCREEN_HEIGHT_PX / screen_diagonal_size_px
        )

        physical_screen_corner_coords = np.float32(
            [
                [-screen_width_meters / 2, -CAMERA_HEIGHT_ABOVE_SCREEN_METERS],
                [screen_width_meters / 2, -CAMERA_HEIGHT_ABOVE_SCREEN_METERS],
                [
                    -screen_width_meters / 2,
                    -CAMERA_HEIGHT_ABOVE_SCREEN_METERS - screen_height_meters,
                ],
                [
                    screen_width_meters / 2,
                    -CAMERA_HEIGHT_ABOVE_SCREEN_METERS - screen_height_meters,
                ],
            ]
        )
        pixel_screen_corner_coords = np.float32(
            [
                [0, 0],
                [SCREEN_WIDTH_PX, 0],
                [0, SCREEN_HEIGHT_PX],
                [SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX],
            ]
        )
        # Get the transformation matrix
        self.transformation_matrix = cv2.getPerspectiveTransform(
            physical_screen_corner_coords, pixel_screen_corner_coords
        )

    def project(
        self, angle_x, angle_y, angle_z, disp_x, disp_y, disp_z
    ) -> Tuple[float, float]:
        """Projects the gaze point to the screen. Returns the x and y pixel
        coordinates of the gaze point."""

        # First convert the 3d coordinates to 2d meter coordinates on the
        # screen plane
        x_meters = disp_x + disp_z * math.tan(-angle_y)
        y_meters = disp_y + disp_z * math.tan(angle_x)

        # Then convert the meter coordinates to pixel coordinates
        physical_point = np.float32([[[x_meters, y_meters]]])
        pixel_point = cv2.transform(physical_point, self.transformation_matrix)[0]
        x_px = int(pixel_point[0][0])
        y_px = int(pixel_point[0][1])

        return x_px, y_px, x_meters, y_meters

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if not input_data or input_data.header != "kalman":

            return None

        angle_x = input_data.payload["angle_x"]
        angle_y = input_data.payload["angle_y"]
        angle_z = input_data.payload["angle_z"]
        disp_x = input_data.payload["disp_x"]
        disp_y = input_data.payload["disp_y"]
        disp_z = input_data.payload["disp_z"]

        x_px, y_px, x_m, y_m = self.project(
            angle_x, angle_y, angle_z, disp_x, disp_y, disp_z
        )
        payload = {"x_px": x_px, "y_px": y_px, "x_m": x_m, "y_m": y_m}

        return Data(header="projection", payload=payload)
