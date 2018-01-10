import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps

def insert_to_db(task):
    client = MongoClient()
    db = client.todo_database
    try:
        return_values = db.tasks.insert_one(task)
        id = return_values.inserted_id
        return dumps(db.tasks.find_one({"_id" : ObjectId(id)}))
    except:
        return "exception"
