from copy import copy
from typing import Optional

from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class FilterModule(GazePointerModule):

    def __init__(self, alpha, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.alpha = alpha
        self.smooth_angle_x = None
        self.smooth_angle_y = None

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        angle_x = input_data.payload["angle_x"]
        angle_y = input_data.payload["angle_y"]

        if self.smooth_angle_x is None or self.smooth_angle_y is None:
            self.smooth_angle_x = angle_x
            self.smooth_angle_y = angle_y
        else:
            self.smooth_angle_x = (
                self.alpha * angle_x + (1 - self.alpha) * self.smooth_angle_x
            )
            self.smooth_angle_y = (
                self.alpha * angle_y + (1 - self.alpha) * self.smooth_angle_y
            )

        payload = {
            "angle_x": copy(self.smooth_angle_x),
            "angle_y": copy(self.smooth_angle_y),
        }
        return Data(header="filter", payload=payload)
