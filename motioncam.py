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
width = 800
height = 608 # 600 produced a rounding warning.

camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 24

rawFrame = PiRGBArray(camera, size=(width, height))

# Let the camera "warm up"
time.sleep(0.100)

for frame in camera.capture_continuous(rawFrame, format="bgr", use_video_port=True):
    picture = frame.array

    cv2.imshow("Chinchilla", picture)

    rawFrame.truncate(0)

    if cv2.waitKey(1) == ord('q'): break


# BUG: the window doesn't close
camera.close()

print("Cool.")
