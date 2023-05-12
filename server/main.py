from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/uploadimage/")
async def create_upload_image(file: bytes = File(...)):
    with open('image.jpg','wb') as image:
        image.write(file)
        image.close()
    return 'got it'