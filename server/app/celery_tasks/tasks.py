from celery import Celery
from . import celeryconfig
import numpy as np
import cv2 as cv 
from PIL import Image
from openai.error import RateLimitError

from app.mongo_functions import get_database
from app.image_functions import read_image
from app.ocr import prepare_images, apply_tesseract, get_image_orientation
import base64
from app.chatgpt import clean_text, get_answers

# Configure Celery
celeryApp = Celery('tasks')
celeryApp.config_from_object(celeryconfig)


# Define a Celery task
@celeryApp.task
def add(x, y):
    result = x + y
    return result


@celeryApp.task
def prepare_images_task(content):
    content=base64.b64decode(content.encode('utf-8'))
    image= read_image(content)
    orientation = get_image_orientation(image)
    parts = prepare_images(image, orientation)
    #because each part is of type numpy.ndarray which is not JSON serializable
    serialized_parts = [part.tolist() for part in parts]
    return serialized_parts

@celeryApp.task
def apply_tesseract_task(parts):
    text=[]
    for image in parts:
        img_array = np.array(image, dtype=np.uint8)
        img = Image.fromarray(img_array)
        result = apply_tesseract(img)
        text.append(result)
    text = ''.join(text)
    return text

@celeryApp.task(bind=True)
def get_answers_task(self,text):
    try:
        cleanresult = clean_text(text)
    except RateLimitError as exc:
        raise self.retry(exc=exc, countdown=30)

    try:
        answers = get_answers(cleanresult)
    except RateLimitError as exc:
        raise self.retry(exc=exc, countdown=30)

    return answers


    

    

    
    

    
