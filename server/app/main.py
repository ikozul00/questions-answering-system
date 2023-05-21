from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from app.image_functions import read_image
from app.ocr import prepare_images, apply_tesseract
from app.celery_tasks.tasks import add, imagetask
import base64


app = FastAPI()

class Item(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadImage/")
async def create_upload_image(file: Annotated[UploadFile, File()], title: Annotated[str, Form()],):
    content = await file.read()
    id=imagetask.delay(base64.b64encode(content).decode('utf-8'))
    return {"id":id}