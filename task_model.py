#!/usr/bin/env python3

import pymongo
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps

'''client = MongoClient()
db = client.todo_database'''

def insert_task_model(title, description, deadline, userid):
    client = MongoClient()
    db = client.todo_database
    deadline = datetime.datetime.strptime(deadline, '%d %b %Y %H:%M:%S')
    task = {"title" : title, "description" : description, \
            "created_time" : datetime.datetime.utcnow(), "created_by" : userid,\
            "deadline" : deadline, "completed" : False}
    try:
        return_values = db.tasks.insert_one(task)
        id = return_values.inserted_id
        return dumps(db.tasks.find_one({"_id" : ObjectId(id)}))
    except:
        return "exception"

if __name__ == '__main__':
    pass
