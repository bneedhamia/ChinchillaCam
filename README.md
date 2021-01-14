# ChinchillaCam
A Raspberry Pi webcam to find what's living under our front porch - we suspect it's
at least one chinchilla.

Status: The code detects motion; I need to add code to upload a jpeg of the frame with motion.

The essential hardware consists of a Raspberry Pi 3 and Camera Module V2.
The software uses OpenCV (Open Computer Vision, a huge and powerful image processing library) and Python.
The idea is to continuously capture frames from the camera, use software motion-detection,
and upload any frame that has (the right) motion in it.

Tip from https://community.octoprint.org/t/anyway-to-disable-the-autofocus-for-cameras/801/11:

To disable the autofocus, enter these two commands:
1. sudo v4l2-ctl --set-ctrl=focus_auto=0
2. sudo v4l2-ctl --set-ctrl=focus_absolute=40

(The default values are auto=1 and absolute=8189)

## Files
* My blogs about the project start at [ChinchillaCam: Installing the Raspberry Pi Camera Module and OpenCV](https://needhamia.com/?p=950)
* ProjectDiary.odt = the day-to-day, detailed unfolding of the project over time
* BillOfMaterials.ods = parts list, with prices and sources
* piconfig.txt = step-by-step instructions for installing and configuring the Raspberry Pi 3, Camera Module V2, and OpenCV for camera work.
* motioncam.cfg = example configuration file. Copy this file to your home directory (/home/pi/).
The fields in motioncam.cfg are explained in the config file parsing code in the .py file.
