import math

import screeninfo

"""This module contains the configuration for the application."""
# Controls the frame rate of the camera
FRAME_RATE = (
    30  # https://stackoverflow.com/questions/52068277/change-frame-rate-in-opencv-3-4-2
)

# Controls the smoothing factor of the Exponential Moving Average filter.
# The lower the value, the more smoothing is applied.
# First filter, for smoothing the 3d x y z roll pitch yaw
ALPHA_3D = 0.3

# Second filter, for smoothing the 2d x_px y_px points
ALPHA_2D = 0.3

# Angle Bias, for offsetting viewing angle. In radians.
# This is a temporary fix TODO
X_ANGLE_BIAS = -10 / 180 * math.pi
Y_ANGLE_BIAS = 0 / 180 * math.pi
X_ANGLE_GAIN = 2.5  # Gain for the angle
Y_ANGLE_GAIN = 1.5

# Screen parameters
CAMERA_HEIGHT_ABOVE_SCREEN_METERS = float(
    input("Enter the height of the camera above the screen in meters: ")
)
SCREEN_DIAGONAL_SIZE_METERS = float(
    input("Enter the diagonal size of the screen in meters: ")
)
SCREEN_HEIGHT_PX = screeninfo.get_monitors()[0].height
SCREEN_WIDTH_PX = screeninfo.get_monitors()[0].width

# Controls the frequency of print statements in the debugging module
PRINT_INTERVAL = 0.5  # Measured in seconds
