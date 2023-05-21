from celery import Celery
from . import celeryconfig

from app.image_functions import read_image
from app.ocr import prepare_images, apply_tesseract
import base64


# Configure Celery
celeryApp = Celery('tasks')
celeryApp.config_from_object(celeryconfig)


# Define a Celery task
@celeryApp.task
def add(x, y):
    result = x + y
    return result


@celeryApp.task
def imagetask(content):
    content=base64.b64decode(content.encode('utf-8'))
    image= read_image(content)
    parts = prepare_images(image)
    text=[]
    for part in parts:
        result = apply_tesseract(part)
        print(result)
        for word in result["text"]:
            text = ''.join(word)
    text = ''.join(text)
    return text
