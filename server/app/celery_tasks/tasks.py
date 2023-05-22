from celery import Celery
from . import celeryconfig

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


@celeryApp.task(bind=True)
def imagetask(self,content, title):
    content=base64.b64decode(content.encode('utf-8'))
    image= read_image(content)
    orientation = get_image_orientation(image)
    parts = prepare_images(image, orientation)
    text=[]
    for part in parts:
        result = apply_tesseract(part)
        text.append(result)
    text = ''.join(text)
    cleanresult = clean_text(text)
    answers = get_answers(cleanresult)
    print(answers)
    print(self.request.id)
    return {"id": "id"}
