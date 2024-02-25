import time
from typing import Optional

import cv2
import keyboard
import mediapipe as mp
import numpy as np

from gazepointer.config import FRAME_RATE
from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class KeypointModule(GazePointerModule):
    """Module to output the 68 Dlib keypoints"""

    def __init__(self, toggle_key="space", *args, **kwargs):
        super().__init__(*args, **kwargs)

        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.toggle_key = toggle_key
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:

        # Check whether the Caps Lock key is pressed

        if keyboard.is_pressed(self.toggle_key):
            # Capture frame-by--frame
            success, image = self.cap.read()
            image = cv2.cvtColor(
                cv2.flip(image, 1), cv2.COLOR_BGR2RGB
            )  # flipped for selfie view

            image.flags.writeable = False

            results = self.face_mesh.process(image)

            image.flags.writeable = True

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            img_h, img_w, img_c = image.shape
            face_2d = []
            face_3d = []

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if (
                            idx == 33
                            or idx == 263
                            or idx == 1
                            or idx == 61
                            or idx == 291
                            or idx == 199
                        ):
                            if idx == 1:
                                (lm.x * img_w, lm.y * img_h)
                                (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                            face_2d.append([x, y])
                            face_3d.append(([x, y, lm.z]))

                face_2d = np.array(face_2d, dtype=np.float64)

                face_3d = np.array(face_3d, dtype=np.float64)

                payload = {"face_2d": face_2d, "face_3d": face_3d, "frame": image}

                return Data(header="keypoints", payload=payload)
        else:
            time.sleep(0.05)

        return None
