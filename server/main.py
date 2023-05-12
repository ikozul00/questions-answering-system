from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadimage/")
async def create_upload_image(file: UploadFile):
    with open('image.jpg','wb') as image:
        image.write(file)
        image.close()
    return {"filename": file.filename}