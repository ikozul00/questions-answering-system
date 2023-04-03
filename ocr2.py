
import pytesseract
import numpy as np
import cv2 as cv 
import sys

custom_oem_psm_config = r'--oem 3 --psm 11'
filename = '2kolokvij.jpg'

def read_image():
    #cv2.IMREAD_UNCHANGED: It specifies to load an image as such including alpha channel.
    img = cv.imread(filename, cv.IMREAD_UNCHANGED)
    if img is None:
        sys.exit("Could not read the image.")
    return img

def display_image(image):
    cv.imshow('img2', image)
    cv.waitKey(0)

#turn into gray image
def get_grayscale(image):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


#change to rgb ?
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#resize
def resize(image, factor):
    height, width = image.shape[:2]
    return cv.resize(image,(factor*width, factor*height), interpolation = cv.INTER_LINEAR)

#rotation with respect to center - how to detect amount of rotation?
def rotate(image, degree_x, degree_y):
    cols, rows= image.shape
    M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),degree_x,degree_y)
    return cv.warpAffine(image,M,(cols,rows))

def add_border(image):
    return cv.copyMakeBorder(image,10,10,10,10,cv.BORDER_REFLECT)

#maybe change to adaptive thresholding?
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
        x,y,w,h = cv.boundingRect(c)
        line_items_coordinates.append([(x,y), (width, y+h)])

    return line_items_coordinates






# # params=pytesseract.image_to_data(img, lang="hrv+eng", output_type=Output.DICT)
# # print(params)

# output=pytesseract.run_and_get_output(img)
# print(output)


# # img1 = np.array(Image.open(filename))
img=read_image()
img=get_grayscale(img)

#find regions
line_items_coordinates = mark_regions(img)
# img=resize(img, 2)
# img=add_border(img)
# img=rotate(img,-2,1)
# img=remove_noise(img)
# img=thresholding(img)
# display_image(img)

for c in line_items_coordinates:
    # cropping image img = image[y0:y1, x0:x1]
    cropped_image = img[c[0][1]:c[1][1], c[0][0]:c[1][0]]    
    resized=resize(cropped_image, 2)
    with_border=add_border(resized)
    # img=rotate(img,-2,1)
    without_noise=remove_noise(with_border)
    threshed=thresholding(without_noise)
    display_image(dilated)

    text = pytesseract.image_to_string(threshed, lang="hrv+eng", config=custom_oem_psm_config)
    print(text)

# with open(filename+'.txt', 'w') as f:
#     f.writelines(text)

# # cv2.imshow('img2', img)
# # cv2.waitKey(0)
