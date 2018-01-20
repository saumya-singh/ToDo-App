import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps, RELAXED_JSON_OPTIONS, DatetimeRepresentation
from server import mongo

def insert_to_db(task):
    try:
        return_values = mongo.db.tasks.insert_one(task)
        id_ = return_values.inserted_id
        task_details = dumps(mongo.db.tasks.find_one({"_id" : ObjectId(id_)}), \
                        json_options = RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_task_schema(json.loads(task_details))
        return (formatted_task_details, 1, 200)
    except:
        return ("Cannot add task in the ToDo list", 0, 500)

def list_tasks_from_db(userid):
    task_list = []
    count = mongo.db.tasks.find({"created_by" : userid}).count()
    if count == 0:
        return ("No task added from this userid", 0, 200)
    cursor = mongo.db.tasks.find({"created_by" : userid})
    for each_task in cursor:
        each_task_details = dumps(each_task, json_options= RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_task_schema(json.\
        loads(each_task_details))
        task_list.append(formatted_task_details)
    return (task_list, 1, 200)

def task_from_db(userid, taskid):
    count = mongo.db.tasks.find({"created_by": userid, \
                            "_id" : ObjectId(taskid)}).count()
    if count == 0:
        return ("Invalid Task Id", 0, 404)
    task_details = dumps(mongo.db.tasks.find_one({"created_by": userid, \
                "_id": ObjectId(taskid)}), json_options = RELAXED_JSON_OPTIONS)
    formatted_task_details = formatting_task_schema(json.loads(task_details))
    return (formatted_task_details, 1, 200)

def update_task_in_db(content, userid, taskid):
    return_values = mongo.db.tasks.update_one({"created_by": userid, \
                                "_id" : ObjectId(taskid)}, {"$set" : content})
    if return_values.matched_count == 0:
        return ("Invalid Task Id", 0, 404)
    elif return_values.matched_count == 1 and return_values.modified_count == 0:
        return ("Nothing to modify", 0, 200)
    elif return_values.matched_count == 1 and return_values.modified_count == 1:
        task_details = dumps(mongo.db.tasks.find_one({"created_by": userid, \
                "_id" : ObjectId(taskid)}), json_options = RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_task_schema(json.loads(task_details))
        return (formatted_task_details, 1, 200)

def delete_task_from_db(userid, taskid):
    return_values = mongo.db.tasks.delete_one({"created_by": userid, \
                                        "_id" : ObjectId(taskid)})
    if return_values.deleted_count == 0:
        return ("Task Id not found", 0, 404)
    elif return_values.deleted_count == 1:
        return ("Task deleted successfully", 1, 200)

def formatting_task_schema(data):
    data["_id"] = data["_id"]["$oid"]
    data["created_time"] = data["created_time"]["$date"]
    data["deadline"] = data["deadline"]["$date"]
    return data
