from typing import Annotated, List
from fastapi import FastAPI, File, UploadFile, Form, Request
from pydantic import BaseModel
import base64
from celery.result import AsyncResult
from celery import chain
from pymongo import MongoClient
from dotenv import dotenv_values

from app.celery_tasks.tasks import prepare_images_task, apply_tesseract_task, get_answers_task
from app.mongo_functions import get_database, update_task, get_done_tasks, add_new_task


config = dotenv_values()


app = FastAPI()

class Item(BaseModel):
    name: str

class StatusArgs(BaseModel):
    ids: List[str]

@app.on_event("startup")
def startup_db_client():

    app.mongodb_client = MongoClient(f'mongodb://{config["MONGODB_USERNAME"]}:{config["MONGODB_PASSWORD"]}@mongo:27017/')
    app.database = app.mongodb_client["ocrdb"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadImage/")
async def create_upload_image(request:Request, file: Annotated[UploadFile, File()], title: Annotated[str, Form()],):
    content = await file.read()
    task = chain( prepare_images_task.s() | apply_tesseract_task.s() | get_answers_task.s())
    id=task.delay(base64.b64encode(content).decode('utf-8'))
    db_id = add_new_task(request.app.database["results"], str(id), title, content)
    return {"id": str(id)}

@app.get("/doneResults/")
async def get_done_tasks(request:Request):
    done = get_done_tasks(request.app.database["results"])
    return done


#how to solve this with update many?
@app.post("/updateStatus/")
async def update_status_of_task(request:Request,ids: StatusArgs):
    inprogess = []
    done = []
    for id in ids:
        task=AsyncResult(id)
        status="STARTED"
        if task.ready():
            result = task.get()
            print(result)
            update_task(request.app.database["results"], id, result)
            status="SUCCESS"
    return {"status": status}