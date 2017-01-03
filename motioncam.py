# motioncam: a motion-detecting webcam,
# originally written to detect Chinchillas living under our porch.
# See https://github.com/bneedhamia/ChinchillaCam for the entire project.

# Copyright (c) 2017 Bradford Needham, North Plains, Oregon, USA
# @bneedhamia, https://www.needhamia.com
# Licensed under GPL 2, a copy of which
# should have been included with this software.

# Requires a configuration file named ~/motioncam.cfg.
# See motioncam.cfg for an example of this file.

# Written for Python 2.7,
#   OpenCV 3.1, TODO add more as we go.

# This code began with Adrian Rosebrock's examples, for example at
# http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

from picamera import PiCamera # Support for the Raspberry Pi Camera Module V2
from picamera.array import PiRGBArray
import cv2 # OpenCV, the Open Computer Vision library
import json
import time
import os.path

# The JSON configuration file location
configFilename = "~/motioncam.cfg"

# Read our parameters from a JSON file

file = open(os.path.expanduser(configFilename), "r")
jsonString = file.read()
config = json.loads(jsonString)

# Width (in pixels) of the camera frame.
# This is the size of image to be captured by the camera
# and to be uploaded.
field = "width"
prefix = configFilename + ": image width, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 8:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# Height (in pixels) of the camera frame.
field = "height"
prefix = configFilename + ": image height, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 8:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# With (in pixels) of the motion-detection frames.
# The motion detection frames are smaller to speed processing
# and because you don't need high resolution to do basic motion detection.
field = "tinywidth"
prefix = configFilename + ": motion image width, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 8:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# Height (in pixels) of the motion-detection frames.
field = "tinyheight"
prefix = configFilename + ": motion image height, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 8:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# Number of frames per second the camera will operate at.
# The higher this number is, the more likely we'll be to miss motion.
field = "framerate"
prefix = configFilename + ": video frames per second, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 1:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# The weight (Alpha) to use in averaging the background.
# A weight of 1/2 causes a weighting sequence of 1/2, 1/4, 1/8, etc.,
# making the influence of past frames drop off quickly after about 8 frames.
field = "weighting"
prefix = configFilename + ": average weight per frame, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (float)):
    print(prefix + "is not a float: ") + repr(config[field])
    exit()
if not (config[field] > 0.0 and config[field] < 1.0):
    print(prefix + "is not between 0.0 and 1.0: " + str(config[field]))
    exit()

# Per-pixel motion comparison.
# Pixels whose grayscale value differs from the average by
# diffthreshold or more are considered "different" from the background.
# In experiments with my camera I found a noise floor of about 30.0,
# so the number should be set higher than that.
field = "diffthreshold"
prefix = configFilename + ": per pixel difference threshold, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (int, long)):
    print(prefix + "is not an integer: ") + repr(config[field])
    exit()
if config[field] < 1:
    print(prefix + "is too small: " + str(config[field]))
    exit()

# Whole image motion comparison.
# Minimum percent of "different" pixels (see diffthreshold) in the frame.
# That is, we call the frame "containing motion" if it contains
# more than percentThreshold percent of "different" pixels.
field = "percentthreshold"
prefix = configFilename + ": image percent-movement threshold, '" + field + "', "
if not field in config:
    print(prefix + "is missing")
    exit()
if not isinstance(config[field], (float)):
    print(prefix + "is not a float: ") + repr(config[field])
    exit()
if config[field] < 0.0:
    print(prefix + "is too small: " + str(config[field]))
    exit()

#========= Now that we've parsed the configuration, we can get started.

# average = the grayscale, weighted average of the past N frames.
# if average == None, we haven't read a first frame yet.
average = None

camera = PiCamera()
camera.resolution = (config["width"], config["height"])
camera.framerate = config["framerate"]

rawFrame = PiRGBArray(camera, size=(config["width"], config["height"]))

# Let the camera calibrate
time.sleep(0.100)

# framesToIgnore = number of frames left to ignore motion in.
# Used to a) let the average build before comparing frames to the average,
# and b) to ignore motion after we've detected motion
framesToIgnore = 10 + 1
for frame in camera.capture_continuous(rawFrame, format="bgr", use_video_port=True):

    
    if cv2.waitKey(1) == ord('q'): break

    picture = frame.array

    # Update the number of frames left to ignore.
    if framesToIgnore > 0:
        framesToIgnore -= 1

    # Reset the camera buffer for the next frame.
    rawFrame.truncate(0)

    # create a small, grayscale version of the frame, for motion detection.
    # Blur it a bit to reduce pixel-to-pixel boundary noise.
    tinyFrame = cv2.resize(picture, (config["tinywidth"], config["tinyheight"]))
    grayFrame = cv2.cvtColor(tinyFrame, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.GaussianBlur(grayFrame, (5, 5), 0)

    # If this is the first frame, only initialize the running average.
    if average is None:
        # Create a copy of the frame, converted into floating point intensities
        # We convert to float because accumulateWeighted() uses floats.
        # The values in grayFrame range from 0 through 255.
        average = grayFrame.copy().astype("float")

    # Perform the motion detection:
    # Find the difference between each pixel and its pixel in the average.
    absDiff = cv2.absdiff(grayFrame, cv2.convertScaleAbs(average))

    # Now that we're done using the average for this iteration,
    # add this frame into that running average.
    # Technically, accumulateWeighted() is an IIR filter,
    # smoothing out the long-term changes in the background.
    cv2.accumulateWeighted(grayFrame, average, config["weighting"])

    # For understanding how to set the threshold,
    # produce some statistics
    # To use this code, set camera.framerate = 1
    # then position the camera so there is no movement in front of it,
    # then place your hand over the camera to cause maximum change.
    # For my setup, I saw a noise floor (max change with no change in the
    # camera's view) of about 20.0, and a maximum possible difference of
    # 255.0

    if False: # change to if True: to see pixel difference statistics
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(absDiff)
        print("max pixel difference: " + str(maxVal))

    # (Unused code, kept here as an example of using calcHist)
    # histogram = cv2.calcHist([absDiff], [0], None, [10], [0.0, 256.0])
    # print(str(histogram))
   
    # Count all the pixels that are substantially different from the average.
    # That is, a different pixel will have a value of 255 in markedDiff;
    # a non-diffferent (background) pixel will have a value of 0 in markedDiff.
    markedDiff = cv2.threshold(absDiff, config["diffthreshold"], \
        255, cv2.THRESH_BINARY)[1]
    numberChanged = cv2.countNonZero(markedDiff)

    # Convert the number of pixels changed into a percentage of the image
    percentChanged = 100.0 * float(numberChanged) \
        / (float(config["tinywidth"]) * float(config["tinyheight"]))
    # print("% changed: " + str(percentChanged))

    # If there isn't motion in the picture
    # or we're ignoring this frame
    # we're done with this frame.
    if framesToIgnore > 0 or percentChanged < config["percentthreshold"]:
        continue
    framesToIgnore = config["framerate"] + 1 # That is, ignore for 1 second

    # Capture the image.
    cv2.imshow("Chinchilla", picture)

    #TODO add code to upload a Jpeg of the image to a site somewhere.
    # might use cv2.imwrite() to create a file, then upload the file.


# BUG: the window doesn't close
camera.close()

print("Done.")
