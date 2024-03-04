from copy import copy
from typing import Optional

from gazepointer.config import ALPHA_2D
from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class Kalman3DModule(GazePointerModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.alpha = ALPHA_2D
        self.smooth_x_px = 0
        self.smooth_y_px = 0
        self.smooth_angle_z = 0
        self.smooth_disp_x = 0
        self.smooth_disp_y = 0
        self.smooth_disp_z = 0

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if not input_data or input_data.header != "pnp":
            return None

        angle_x = input_data.payload["angle_x"]
        angle_y = input_data.payload["angle_y"]
        angle_z = input_data.payload["angle_z"]
        disp_x = input_data.payload["disp_x"]
        disp_y = input_data.payload["disp_y"]
        disp_z = input_data.payload["disp_z"]

        self.smooth_x_px = self.alpha * angle_x + (1 - self.alpha) * self.smooth_x_px
        self.smooth_y_px = self.alpha * angle_y + (1 - self.alpha) * self.smooth_y_px
        self.smooth_angle_z = (
            self.alpha * angle_z + (1 - self.alpha) * self.smooth_angle_z
        )
        self.smooth_disp_x = self.alpha * disp_x + (1 - self.alpha) * self.smooth_disp_x
        self.smooth_disp_y = self.alpha * disp_y + (1 - self.alpha) * self.smooth_disp_y
        self.smooth_disp_z = self.alpha * disp_z + (1 - self.alpha) * self.smooth_disp_z

        payload = {
            "angle_x": copy(self.smooth_x_px),
            "angle_y": copy(self.smooth_y_px),
            "angle_z": copy(self.smooth_angle_z),
            "disp_x": copy(self.smooth_disp_x),
            "disp_y": copy(self.smooth_disp_y),
            "disp_z": copy(self.smooth_disp_z),
        }
        return Data(header="kalman", payload=payload)
