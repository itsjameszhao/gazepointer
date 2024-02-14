from typing import Optional

import cv2
import dlib
import numpy as np

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class KeypointModule(GazePointerModule):
    """Modue to output the 68 Dlib keypoints"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            "../models/shape_predictor_68_face_landmarks.dat"
        )
        self.cap = cv2.VideoCapture(0)

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        # Capture frame-by--frame
        ret, frame = self.cap.read()

        if not ret:
            print("Failed to grab frame")

        else:
            # Convert the frame to  grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale frame
            faces = self.detector(gray, 0)

            if len(faces) > 0:
                # Find the largest face based on the area of the rectangle
                largest_face = max(faces, key=lambda rect: rect.width() * rect.height())

                # Now we only analyze the largest face
                shape = self.predictor(gray, largest_face)
                shape_np = np.zeros((68, 2), dtype="int")

                for i in range(68):
                    shape_np[i] = (shape.part(i).x, shape.part(i).y)
                    payload = {"shape_np": shape_np, "frame": frame}

                return Data(header="keypoints", payload=payload)

        return None
