import pymongo, json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps, RELAXED_JSON_OPTIONS, DatetimeRepresentation

def insert_to_db(task):
    client = MongoClient()
    db = client.todo_database
    try:
        return_values = db.tasks.insert_one(task)
        id_ = return_values.inserted_id
        task_details = dumps(db.tasks.find_one({"_id" : ObjectId(id_)}), \
                        json_options = RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_func(json.loads(task_details))
        client.close()
        return [formatted_task_details, 1]
    except:
        client.close()
        return ["Cannot add task in the ToDo list", 0]

def list_tasks_from_db(userid):
    client = MongoClient()
    db = client.todo_database
    task_list = []
    count = db.tasks.find({"created_by" : userid}).count()
    if count == 0:
        client.close()
        return ["No task added from this userid", 0]
    cursor = db.tasks.find({"created_by" : userid})
    for each_task in cursor:
        each_task_details = dumps(each_task, json_options= RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_func(json.loads(each_task_details))
        task_list.append(formatted_task_details)
        client.close()
    return [task_list, 1]

def task_from_db(userid, taskid):
    client = MongoClient()
    db = client.todo_database
    count = db.tasks.find({"created_by": userid, \
                            "_id" : ObjectId(taskid)}).count()
    if count == 0:
        client.close()
        return ["Invalid Task Id", 0]
    task_details = dumps(db.tasks.find_one({"created_by": userid, \
                "_id": ObjectId(taskid)}), json_options = RELAXED_JSON_OPTIONS)
    formatted_task_details = formatting_func(json.loads(task_details))
    client.close()
    return [formatted_task_details, 1]

def update_task_in_db(content, userid, taskid):
    client = MongoClient()
    db = client.todo_database
    return_values = db.tasks.update_one({"created_by": userid, \
                                "_id" : ObjectId(taskid)}, {"$set" : content})
    if return_values.matched_count == 0:
        client.close()
        return ["Invalid Task Id", 0]
    elif return_values.matched_count == 1 and return_values.modified_count == 0:
        client.close()
        return ["Nothing to modify", 0]
    elif return_values.matched_count == 1 and return_values.modified_count == 1:
        client.close()
        task_details = dumps(db.tasks.find_one({"created_by": userid, \
                "_id" : ObjectId(taskid)}), json_options = RELAXED_JSON_OPTIONS)
        formatted_task_details = formatting_func(json.loads(task_details))
        client.close()
        return [formatted_task_details, 1]

def delete_task_from_db(userid, taskid):
    client = MongoClient()
    db = client.todo_database
    return_values = db.tasks.delete_one({"created_by": userid, \
                                        "_id" : ObjectId(taskid)})
    if return_values.deleted_count == 0:
        client.close()
        return ["Incorrect task Id for the given user", 0]
    elif return_values.deleted_count == 1:
        client.close()
        return ["Task deleted successfully", 1]

def formatting_func(data):
    data["_id"] = data["_id"]["$oid"]
    data["created_time"] = data["created_time"]["$date"]
    data["deadline"] = data["deadline"]["$date"]
    return data
