
import pytesseract
import numpy as np
import cv2 as cv 
import sys

custom_oem_psm_config = r'--oem 3 --psm 11'
filename = '2kolokvij.jpg'

def read_image():
    #cv2.IMREAD_UNCHANGED: It specifies to load an image as such including alpha channel, TODO: remove alpha channel
    img = cv.imread(filename)
    if img is None:
        sys.exit("Could not read the image.")
    return img

def display_image(image, name):
    cv.imshow(name, image)
    cv.waitKey(0)

#turn into gray image
def get_grayscale(image):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


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



def mark_regions(image):
    blured = remove_noise_GaussianBlur(image)
    threshed =adaptive_thresholding_inverted(blured)
    dilated = dilate(threshed)

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



# # params=pytesseract.image_to_data(img, lang="hrv+eng", output_type=Output.DICT)
# # print(params)


img=read_image()
img=get_grayscale(img)

#find regions
line_items_coordinates = mark_regions(img)

whole_text=[]

for c in line_items_coordinates:
    # cropping image img = image[y0:y1, x0:x1]
    cropped = img[c[0][1]:c[1][1], c[0][0]:c[1][0]]    
    deskewed=deskew_image(cropped)
    resized=resize(deskewed, 2)
    with_border=add_border(resized)
    without_noise=remove_noise(with_border)
    threshed=adaptive_thresholding(without_noise)
    # display_image(threshed, "image")

    text = pytesseract.image_to_string(threshed, lang="hrv+eng", config=custom_oem_psm_config)
    whole_text.append(text)



with open(filename+'.txt', 'w') as f:
    f.writelines(whole_text)

