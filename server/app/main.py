from typing import Annotated, List
from fastapi import FastAPI, File, UploadFile, Form, Request
from pydantic import BaseModel
import base64
from celery.result import AsyncResult
from celery import chain
from pymongo import MongoClient
from dotenv import dotenv_values

from app.celery_tasks.tasks import prepare_images_task, apply_tesseract_task, get_answers_task, save_task_result
from app.mongo_functions import get_database, get_tasks, add_new_task, get_result_data


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
    task = chain( prepare_images_task.s() | apply_tesseract_task.s() | get_answers_task.s() | save_task_result.s())
    id=task.delay(base64.b64encode(content).decode('utf-8'))
    db_id = add_new_task(request.app.database, str(id), title, content)
    return {"id": str(id)}

@app.get("/getResults")
async def get_results(request: Request):
    tasks = get_tasks(request.app.database["results"])
    tasks = list(tasks)
    done=[]
    inprogress=[]

    for task in tasks:
        if task["status"] == "STARTED":
            inprogress.append({"id":task["_id"], "title": task["title"]})
        elif task["status"] == "SUCCESS":
            done.append({"id":task["_id"], "title": task["title"]})

    return {"done": done, "inprogress": inprogress}



@app.get("/getTaskData")
async def get_task_data(request: Request, id:str):
    result, image = get_result_data(request.app.database, id)
    if result == None:
        return {"id":"Id doesn't exist"}
    encoded_image = base64.b64encode(image).decode('utf-8')
    return {"id": result["_id"], "title": result["title"], "answers":result["result"], "image":encoded_image}