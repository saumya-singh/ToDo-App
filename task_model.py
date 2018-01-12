import datetime, json
import db_handler

def insert_task(content, userid):
    res = validate_task_fields(content)
    if res[1] == 0:
        return create_json_response(result)
    elif res[1] == 1:
        content = res[0]
    task = {"title" : content["title"], "description" : content["description"],\
            "created_time" : datetime.datetime.utcnow(), "created_by" : userid,\
            "deadline" : content["deadline"], "completed" : False}
    result = db_handler.insert_to_db(task)
    return create_json_response(result)

def get_tasks_list(userid):
    result = db_handler.list_tasks_from_db(userid)
    return create_json_response(result)

def get_one_task(userid, taskid):
    result = db_handler.task_from_db(userid, taskid)
    return create_json_response(result)

def update_task(content, userid, taskid):
    res = validate_task_fields(content)
    if res[1] == 0:
        return create_json_response(res)
    elif res[1] == 1:
        content = res[0]
    result = db_handler.update_task_in_db(content, userid, taskid)
    return create_json_response(result)

def delete_task(userid, taskid):
    result = db_handler.delete_task_from_db(userid, taskid)
    return create_json_response(result)

def validate_task_fields(content):
    if content["title"] in (None,"") or content["description"] in\
                        (None,"") or content["deadline"] in (None,""):
        return ["Fields cannot remain empty", 0]
    try:
        content["deadline"] = datetime.datetime.strptime(content["deadline"],\
                                                        '%d %b %Y %H:%M:%S')
        return [content, 1]
    except:
        return ["DEADLINE not in the right format", 0]

def create_json_response(result):
    if result[1] == 1:
        json_sent = {"status" : "success", "data" : result[0]}
    elif result[1] == 0:
        json_sent = {"status" : "failure", "error" : result[0]}
    return json_sent
