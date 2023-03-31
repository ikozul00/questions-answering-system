# from PIL import Image
import pytesseract
import numpy as np
import cv2 

filename = 'primjer2.jpeg'
img = cv2.imread(filename)

h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img) 
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)


norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)




# img1 = np.array(Image.open(filename))
text = pytesseract.image_to_string(img, lang="hrv")

with open('output2.txt', 'w') as f:
    f.writelines(text)

# cv2.imshow('img2', img)
# cv2.waitKey(0)
