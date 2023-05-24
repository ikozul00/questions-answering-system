from celery import Celery
from . import celeryconfig
import numpy as np
import cv2 as cv 
from PIL import Image
from openai.error import RateLimitError

from app.mongo_functions import get_database, update_task
from app.image_functions import read_image
from app.ocr import prepare_images, apply_tesseract, get_image_orientation
import base64
from app.chatgpt import clean_text, get_answers

# Configure Celery
celeryApp = Celery('tasks')
celeryApp.config_from_object(celeryconfig)



@celeryApp.task(bind=True, max_retries=50, retry_backoff=True)
def prepare_images_task(self, content):
    try:
        content=base64.b64decode(content.encode('utf-8'))
        image= read_image(content)
        orientation = get_image_orientation(image)
        parts = prepare_images(image, orientation)
        #because each part is of type numpy.ndarray which is not JSON serializable
        serialized_parts = [part.tolist() for part in parts]
        return serialized_parts

    except Exception as exc:
        self.retry(exc=exc)

@celeryApp.task(bind=True, max_retries=50, retry_backoff=True)
def apply_tesseract_task(self, parts):
    try:
        text=[]
        for image in parts:
            img_array = np.array(image, dtype=np.uint8)
            img = Image.fromarray(img_array)
            result = apply_tesseract(img)
            text.append(result)
        text = ''.join(text)
        return text

    except Exception as exc:
        self.retry(exc=exc)


@celeryApp.task(bind=True, max_retries=50, retry_backoff=True)
def get_answers_task(self,text):
    try:
        try:
            cleanresult = clean_text(text)
        except RateLimitError as exc:
            raise self.retry(exc=exc, countdown=30)

        try:
            answers = get_answers(cleanresult)
        except RateLimitError as exc:
            raise self.retry(exc=exc, countdown=30)

        return answers

    except Exception as exc:
        self.retry(exc=exc)


@celeryApp.task(bind=True, max_retries=50, retry_backoff=True)
def save_task_result(self, result):
    try:
        db=get_database()
        id = self.request.id
        update_task(db["results"], id, result)

    except Exception as exc:
        self.retry(exc=exc)


    

    

    
    

    
