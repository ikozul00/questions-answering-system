import cv2 as cv 
import numpy as np

#turn into gray image
def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#resize
def resize(image, factor):
    height, width = image.shape[:2]
    return cv.resize(image,(factor*width, factor*height), interpolation = cv.INTER_LINEAR)


def add_border(image):
    return cv.copyMakeBorder(image,10,10,10,10,cv.BORDER_REFLECT)

def thresholding(image):
    ret,th = cv.threshold(image,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    return th

def adaptive_thresholding(image):
    thresh = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    return thresh

def adaptive_thresholding_inverted(image):
    return cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,11,10)

def remove_noise(image):
    return cv.medianBlur(image,5)

def remove_noise_GaussianBlur(image):
    return cv.GaussianBlur(image,(9,9),0)

# Dilate to combine adjacent text contours
def dilate(image):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (9,9))
    return cv.dilate(image, kernel, iterations=4)


#https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
def deskew_image(image):
    # flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv.bitwise_not(image)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    threshed = thresholding(gray)
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(threshed > 0))
    angle = cv.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle
    # rotate the image to deskew it
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv.warpAffine(image, rotation_matrix, (w, h),cv.INTER_CUBIC, cv.BORDER_REPLICATE)
    return rotated