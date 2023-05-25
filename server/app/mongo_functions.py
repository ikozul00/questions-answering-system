from dotenv import dotenv_values
from pymongo import MongoClient
from gridfs import GridFS

config = dotenv_values()

def get_database():
   CONNECTION_STRING = f'mongodb://{config["MONGODB_USERNAME"]}:{config["MONGODB_PASSWORD"]}@mongo:27017/'
   client = MongoClient(CONNECTION_STRING)
   return client['ocrdb']
#TODO: see do I need to save an image
def add_new_task(db, id, title, image):
    collection = db["results"]
    fs= GridFS(db)
    file_id = fs.put(image, filename=title+".jpeg")
    return collection.insert_one({"_id": id,"title": title,"image":file_id, "status": "STARTED"})


def update_task(collection, id, result):
    filter = {"_id": id}
    newvalues = { "$set": { 'status': "SUCCESS", 'result': result } }
    collection.update_one(filter, newvalues, upsert=True)


def get_tasks(collection):
    return collection.find({},{ "_id": 1, "status": 1, "title": 1 })

def get_result_data(db, id):
    data = db["results"].find_one({"_id":id})
    if data == None:
        return None, None
    fs= GridFS(db)
    image = fs.get(data["image"]).read()
    return data, image
 

  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
   dbname = get_database()