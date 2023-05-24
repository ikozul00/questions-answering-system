from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values()

def get_database():
   CONNECTION_STRING = f'mongodb://{config["MONGODB_USERNAME"]}:{config["MONGODB_PASSWORD"]}@mongo:27017/'
   client = MongoClient(CONNECTION_STRING)
   return client['ocrdb']

def add_new_task(collection, id, title, image):
    return collection.insert_one({"_id": id,"title": title,"image":image, "status": "STARTED"})


def update_task(collection, id, result):
    print(id)
    filter = {"_id": id}
    newvalues = { "$set": { 'status': "SUCCESS", 'result': result } }
    collection.update_one(filter, newvalues, upsert=True)

def get_done_tasks(collection):
    filter = {"status":"SUCCESS"}
    projection = {"status":0}
    result=list(collection.find(filter, projection))
    return result
 

  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
   dbname = get_database()