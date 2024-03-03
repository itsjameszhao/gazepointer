# Image processing pipeline
# keypoint module (generate facial keypoints from the video stream)
#                         |                                                   \
#                         v                                                    v
# pnp module (compute x y z roll pitch yaw of the head)                 # contol module (did they blink and close their eyes)
#                         |                                                       |
#                        v                                                       |
# kalman module, kalman filtering (filter out the noise in the x y z roll pitch yaw of the head)
#                        |                                                       |
#                        v                                                       v
# Projection module, project person's gaze onto the screen
#                                                        \
#                                                         v
# Screen module (control the mouse on the screen)

# Purpose of screen module: receive data stream from 2 modules: 1) projection module 2) control module
# Inputs:
# (From projection module)
# Data(header="screen", x, y) pixel location on the screen

# (From control module)
# Data(header="mouse", payload="click")

# The control module controls the mouse with PyAutoGUI (pyautogui)
# We need to do pyautogui commands asynchronously (asyncio)
# Pyautogui documentation:

# Test screeen module
# Open Chrome and hard code
# List of screen coordinates (10,20), (30, 40)
# Send those coordinates to screen module with time delay
# Verify that it works and can click

import asyncio
from typing import Optional

import pyautogui

from gazepointer.config import FRAME_RATE
from gazepointer.data_message import Data
from gazepointer.gazepointer_module import GazePointerModule


class ScreenModule(GazePointerModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def async_click(self):
        pyautogui.click()

    async def async_move_mouse(self, x, y):
        pyautogui.moveTo(x, y, 1 / FRAME_RATE)

    def process_function(self, input_data: Optional[Data]) -> Optional[Data]:
        if (
            input_data is None
            or input_data.header is None
            or input_data.payload is None
        ):
            return None
        if input_data.header == "mouse":
            payload = input_data.payload
            if payload == "click":
                asyncio.run(self.async_click())
        if input_data.header == "screen":
            x, y = input_data.payload
            asyncio.run(self.async_move_mouse(x, y))

        return None
