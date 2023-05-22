from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from celery.result import AsyncResult
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
    id=imagetask.delay(base64.b64encode(content).decode('utf-8'), title)
    return {"id": str(id)}

@app.post("/updateStatus/")
async def update_status_of_task(id: str):
    result=AsyncResult(id)
    print(result.ready())
    print("result")
    print(result.get())
    return {"id": str(id)}