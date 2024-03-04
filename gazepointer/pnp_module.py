import time
from typing import Optional

import cv2
import numpy as np

from gazepointer.config import X_ANGLE_BIAS, X_ANGLE_GAIN, Y_ANGLE_BIAS, Y_ANGLE_GAIN
from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class PnPModule(GazePointerModule):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_time = time.time()

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if not input_data or input_data.header != "keypoint":
            return None
        face_2d = input_data.payload["face_2d"]
        face_3d = input_data.payload["face_3d"]
        img_w, img_h, img_c = input_data.payload["frame"].shape

        focal_length = 1 * img_w

        cam_matrix = np.array(
            [[focal_length, 0, img_h / 2], [0, focal_length, img_w / 2], [0, 0, 1]]
        )
        distortion_matrix = np.zeros((4, 1), dtype=np.float64)

        success, rotation_vec, translation_vec = cv2.solvePnP(
            face_3d, face_2d, cam_matrix, distortion_matrix
        )

        if success:
            # getting rotational of face
            rmat, jac = cv2.Rodrigues(rotation_vec)

            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
            # See doc/coords.jpg for coordinate system
            angle_x = X_ANGLE_GAIN * (
                angles[0] * 360 / 180 * np.pi + X_ANGLE_BIAS
            )  # convert to radians
            angle_y = Y_ANGLE_GAIN * (
                -1 * angles[1] * 360 / 180 * np.pi + Y_ANGLE_BIAS
            )  # convert to radians
            angle_z = angles[2] * 360 / 180 * np.pi  # convert to radians
            disp_x = 0  # TODO hard-coded for now, change later
            disp_y = 0  # TODO hard-coded for now, change later
            disp_z = 0.5  # TODO hard-coded for now, change later

            payload = {
                "angle_x": angle_x,
                "angle_y": angle_y,
                "angle_z": angle_z,
                "disp_x": disp_x,
                "disp_y": disp_y,
                "disp_z": disp_z,
            }

            return Data(header="pnp", payload=payload)

        return None
