import screeninfo

"""This module contains the configuration for the application."""
# Controls the frame rate of the camera
FRAME_RATE = (
    30  # https://stackoverflow.com/questions/52068277/change-frame-rate-in-opencv-3-4-2
)

# Controls the smoothing factor of the Exponential Moving Average filter.
# The lower the value, the more smoothing is applied.
ALPHA = 0.5

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
