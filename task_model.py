import datetime, json, re
import db_handler

def insert_task(content, userid):
    res = validate_task_fields(content)
    if res[1] == 0:
        return create_json_response(res)
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
    if re.fullmatch(("\s*"), content["title"]) is not None or \
            re.fullmatch(("\s*"), content["description"]) is not None or \
            re.fullmatch(("\s*"), content["deadline"]) is not None:
        return ("Empty fields and Spaces are not allowed", 0, 400)
    try:
        content["deadline"] = datetime.datetime.strptime(content["deadline"], '%d %b %Y %H:%M:%S')
        current_time = datetime.datetime.now()
        time_left = content["deadline"] - current_time
        if time_left.days < 0:
            return ("DEADLINE cannot be in the past", 0, 400)
        return (content, 1, 200)
    except:
        return ("DEADLINE not in the right format", 0, 400)

def create_json_response(result):
    if result[1] == 1:
        json_sent = {"status" : "success", "data" : result[0]}
    elif result[1] == 0:
        json_sent = {"status" : "failure", "error" : result[0]}
    return (json.dumps(json_sent), result[2])
