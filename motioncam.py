# MotionCam: a motion-detecting webcam, that we're using to detect Chinchillas living under our porch
# This code is based on Adrian Rosebrock's examples, for example at
# http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

# What follows is an 80-column marker.
# 345678901234567890223456789032345678904234567890523456789062345678907234567890

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# dimensions (pixels) of the camera frame
width = 1024
height = 768

# dimensions (pixels) of the motion-detection frames
tinyWidth = 512
tinyHeight = 384

# weighting = the weight (Alpha) to use in averaging the background.
# A weight of 1/2 causes a weighting sequence of 1/2, 1/4, 1/8, etc.,
# making the influence of past frames drop off quickly after about 8 frames.
weighting = 0.5

# average = the grayscale, weighted average of the past N frames.
average = None

camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 24

rawFrame = PiRGBArray(camera, size=(width, height))

# Let the camera calibrate
time.sleep(0.100)

for frame in camera.capture_continuous(rawFrame, format="bgr", use_video_port=True):
    picture = frame.array

    # create a small, grayscale version of the frame, for motion detection.
    # Blur it a bit to reduce image noise.
    tinyFrame = cv2.resize(picture, (tinyWidth, tinyHeight))
    grayFrame = cv2.cvtColor(tinyFrame, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.GaussianBlur(grayFrame, (5, 5), 0)

    
    cv2.imshow("Chinchilla", tinyFrame)

    # Reset the camera buffer for the next frame.
    rawFrame.truncate(0)

    if cv2.waitKey(1) == ord('q'): break


# BUG: the window doesn't close
camera.close()

print("Cool.")
