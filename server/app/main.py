from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form, Request
from pydantic import BaseModel
from typing import List
from celery.result import AsyncResult
from app.celery_tasks.tasks import add, imagetask
import base64
from app.mongo_functions import get_database
from pymongo import MongoClient
from app.mongo_functions import update_task, get_done_tasks
from dotenv import dotenv_values

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
async def create_upload_image(file: Annotated[UploadFile, File()], title: Annotated[str, Form()],):
    content = await file.read()
    id=imagetask.delay(base64.b64encode(content).decode('utf-8'), title)
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