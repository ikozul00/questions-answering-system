
import pytesseract
from image_functions import read_image, display_image
import image_transfromations as transformations
from crop_image import mark_regions

custom_oem_psm_config = r'--oem 3 --psm 1'
filename = '2kolokvij.jpg'

# # params=pytesseract.image_to_data(img, lang="hrv+eng", output_type=Output.DICT)
# # print(params)


img=read_image(filename)
img=transformations.get_grayscale(img)

#find regions
line_items_coordinates = mark_regions(img)

whole_text=[]

for c in line_items_coordinates:
    # cropping image img = image[y0:y1, x0:x1]
    cropped = img[c[0][1]:c[1][1], c[0][0]:c[1][0]]    
    deskewed=transformations.deskew_image(cropped)
    resized=transformations.resize(deskewed, 2)
    with_border=transformations.add_border(resized)
    without_noise=transformations.remove_noise(with_border)
    threshed=transformations.adaptive_thresholding(without_noise)
    # display_image(threshed, "image")

#it returns a dictionary find out how to get data!!!!
    data = pytesseract.image_to_data(threshed, lang="hrv+eng", config=custom_oem_psm_config, output_type=pytesseract.Output.DICT)
    number_of_items= data["text"].length
    print(number_of_items)
#     whole_text.append(text)



# with open('./results/'+filename+'_result1data'+'.txt', 'w') as f:
#     f.writelines(whole_text)

