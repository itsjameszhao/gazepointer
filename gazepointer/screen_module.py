# Image processing pipeline
# keypoint module (generate facial keypoints from the video stream)
                        |                                                   \
                        v                                                    v
# pnp module (compute x y z roll pitch yaw of the head)                 # contol module (did they blink and close their eyes)
                        |                                                       |
                        v                                                       |  
# kalman module, kalman filtering (filter out the noise in the x y z roll pitch yaw of the head) 
                        |                                                       |
                        v                                                       v
# Projection module, project person's gaze onto the screen
                                                        \
                                                         v
                                                        # Screen module (control the mouse on the screen)

# Purpose of screen module: receive data stream from 2 modules: 1) projection module 2) control module
# Inputs:
# (From projection module)
# Data(header="screen", x, y) pixel location on the screen

# (From control module)
# Data(header="mouse_left_down")
# Data(header="mouse_left_up")
# Data(header="mouse_right_up")
# Data(header="mouse_right_down")


# The control module controls the mouse with PyAutoGUI (pyautogui)
# We need to do pyautogui commands asynchronously (asyncio)
# Pyautogui documentation: 