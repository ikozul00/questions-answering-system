
import pytesseract
from image_functions import read_image, display_image
import image_transfromations as transformations
from crop_image import mark_regions

# # params=pytesseract.image_to_data(img, lang="hrv+eng", output_type=Output.DICT)
# # print(params)

def prepare_images(image):
    images = []
    img=transformations.get_grayscale(image)
    line_items_coordinates = mark_regions(img)
    for coordinates in line_items_coordinates:
        # cropping image img = image[y0:y1, x0:x1]
        cropped = img[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]    
        deskewed=transformations.deskew_image(cropped)
        resized=transformations.resize(deskewed, 2)
        with_border=transformations.add_border(resized)
        without_noise=transformations.remove_noise(with_border)
        threshed=transformations.adaptive_thresholding(without_noise)
        images.append(threshed)
    return images

def apply_tesseract(image):
    custom_oem_psm_config = r'--oem 3 --psm 1'
    data = pytesseract.image_to_data(image, lang="hrv+eng", config=custom_oem_psm_config, output_type=pytesseract.Output.DICT)
    return data

# #it returns a dictionary find out how to get data!!!!
#     data = pytesseract.image_to_data(threshed, lang="hrv+eng", config=custom_oem_psm_config, output_type=pytesseract.Output.DICT)
#     number_of_items= data["text"].length
#     print(number_of_items)
# #     whole_text.append(text)



# # with open('./results/'+filename+'_result1data'+'.txt', 'w') as f:
# #     f.writelines(whole_text)

