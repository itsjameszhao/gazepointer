from typing import Optional

import cv2
import numpy as np

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class PnPModule(GazePointerModule):

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        face_2d = input_data.payload["face_2d"]
        face_3d = input_data.payload["face_3d"]
        img_w, img_h = input_data.payload["frame"].shape

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

            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            payload = {"x_angle": x, "y_angle": y, "z_angle": z}
            return Data(header="pnp", payload=payload)

        return None
