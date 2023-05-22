import cv2 as cv 
import sys
import numpy as np

def read_image(file):
    img = np.asarray(bytearray(file), dtype="uint8")
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    if img is None:
        sys.exit("Could not read the imag.")
    return img

def display_image(image, name):
    cv.imshow(name, image)
    cv.waitKey(0)