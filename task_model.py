#!/usr/bin/env python3
import datetime, json
import db_handler

def insert_task(content, userid):
    title = content["title"]
    description = content["description"]
    deadline = content["deadline"]
    if title == None or description == None or deadline == None:
        result = ["Fields cannot remain empty", 0]
        return create_json_result(result)
    try:
        deadline = datetime.datetime.strptime(deadline, '%d %b %Y %H:%M:%S')
    except:
        result = ["DEADLINE not in the right format", 0]
        return create_json_result(result)
    task = {"title" : title, "description" : description, \
            "created_time" : datetime.datetime.utcnow(), "created_by" : userid,\
            "deadline" : deadline, "completed" : False}
    result = db_handler.insert_to_db(task)
    return create_json_result(result)

def get_tasks_list(userid):
    result = db_handler.list_tasks_from_db(userid)
    return create_json_result(result)

def get_one_task(userid, taskid):
    result = db_handler.task_from_db(userid, taskid)
    return create_json_result(result)

def create_json_result(result):
    if result[1] == 1:
        json_send = {"status" : "success", "data" : result[0]}
    elif result[1] == 0:
        json_send = {"status" : "failure", "error" : result[0]}
    return json.dumps(json_send)

if __name__ == '__main__':
    pass
