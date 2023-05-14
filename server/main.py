from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from image_functions import read_image
from ocr import prepare_images, apply_tesseract

app = FastAPI()

class Item(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadImage/")
async def create_upload_image(file: Annotated[UploadFile, File()], title: Annotated[str, Form()],):
    content = await file.read()
    image= read_image(content)
    parts = prepare_images(image)
    text=[]
    for part in parts:
        print(part)
        result = apply_tesseract(part)
        for word in result["text"]:
            text.append(word)
    text = ''.join(text)
    print(text)
    return {"result":text}