from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadImage/")
async def create_upload_image(file: Annotated[bytes, File()], title: Annotated[str, Form()],):
    print(title)
    with open('image.jpg','wb') as image:
        image.write(file)
        image.close()
    return 'got it'