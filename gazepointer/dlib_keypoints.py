import cv2
import dlib
import numpy as np

# Initialize dlib's face detector (HOG-based) and create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")

# Capture the video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")

        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale form
    faces = detector(gray, 0)

    # Loop over the face detections

    for face in faces:
        # Determine the facial landmarks for the face region
        shape = predictor(gray, face)
        shape_np = np.zeros((68, 2), dtype="int")

        for i in range(0, 68):
            shape_np[i] = (shape.part(i).x, shape.part(i).y)

        # Loop over the (x, y)-coordinates for the facial landmarks and draw them on the image

        for x, y in shape_np:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Break the loop when 'q' is pressed

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
