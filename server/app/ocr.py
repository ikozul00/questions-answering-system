
import pytesseract
import app.image_transfromations as transformations
from app.crop_image import mark_regions

def get_image_orientation(image):
    results = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
    return results["orientation"]

def prepare_images(image, orientation):
    images = []
    img=transformations.get_grayscale(image)
    line_items_coordinates = mark_regions(img)
    for coordinates in line_items_coordinates:
        # cropping image img = image[y0:y1, x0:x1]
        cropped = img[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]  
        deskewed=transformations.deskew_image(cropped, orientation)
        resized=transformations.resize(deskewed, 2)
        with_border=transformations.add_border(resized)
        without_noise=transformations.remove_noise(with_border)
        threshed=transformations.adaptive_thresholding(without_noise)
        images.append(threshed)
    return images

def apply_tesseract(image):
    custom_oem_psm_config = r'--oem 3 --psm 1'
    data = pytesseract.image_to_string(image, lang="hrv+eng", config=custom_oem_psm_config)
    return data




