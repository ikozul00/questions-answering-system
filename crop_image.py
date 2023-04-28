import cv2 as cv 
import image_transfromations as transformations


def mark_regions(image):
    blured = transformations.remove_noise_GaussianBlur(image)
    threshed =transformations.adaptive_thresholding_inverted(blured)
    dilated = transformations.dilate(threshed)

     # Find contours, highlight text areas, and extract ROIs
    contours, hierarchy = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    line_items_coordinates = []
    height, width = image.shape

    for c in contours:
        area = cv.contourArea(c)
        #so it only reads questions not random text on sides ex. number of points
        if area > 10000:
            x,y,w,h = cv.boundingRect(c)
            line_items_coordinates.insert(0,[(x,y), (width, y+h)])

    return line_items_coordinates