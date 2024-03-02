from typing import Optional

import cv2
import numpy as np
import time

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class PnPModule(GazePointerModule):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_time = time.time()
        
    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if not input_data:
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

            x_angle = angles[0] * 360
            y_angle = -1 * angles[1] * 360
            z_angle = angles[2] * 360
            x_disp = 0  # TODO hard-coded for now, change later
            y_disp = 0  # TODO hard-coded for now, change later
            z_disp = 0.5  # TODO hard-coded for now, change later

            payload = {
                "x_angle": x_angle,
                "y_angle": y_angle,
                "z_angle": z_angle,
                "x_disp": x_disp,
                "y_disp": y_disp,
                "z_disp": z_disp,
            }
            FPS = 1 / (time.time() - self.last_time)
            if FPS == 0:
                FPS = -1
            print(f"Angles: x: {x_angle} y: {y_angle} z: {z_angle} || Displacements: x: {x_disp} y: {y_disp} z: {z_disp} || FPS: {FPS}", end='\r')
            self.last_time = time.time()
            return Data(header="pnp", payload=payload)

        return None
