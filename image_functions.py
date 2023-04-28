import cv2 as cv 
import sys

def read_image(filename):
    #cv2.IMREAD_UNCHANGED: It specifies to load an image as such including alpha channel, TODO: remove alpha channel
    img = cv.imread('./examples/'+filename)
    if img is None:
        sys.exit("Could not read the image.")
    return img

def display_image(image, name):
    cv.imshow(name, image)
    cv.waitKey(0)