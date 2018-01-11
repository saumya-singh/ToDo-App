import datetime, json
import db_handler

def insert_task(content, userid):
    title = content["title"]
    description = content["description"]
    deadline = content["deadline"]
    if title == None or description == None or deadline == None:
        result = ["Fields cannot remain empty", 0]
        return create_json_response(result)
    try:
        deadline = datetime.datetime.strptime(deadline, '%d %b %Y %H:%M:%S')
    except:
        result = ["DEADLINE not in the right format", 0]
        return create_json_response(result)
    task = {"title" : title, "description" : description, \
            "created_time" : datetime.datetime.utcnow(), "created_by" : userid,\
            "deadline" : deadline, "completed" : False}
    result = db_handler.insert_to_db(task)
    return create_json_response(result)

def get_tasks_list(userid):
    result = db_handler.list_tasks_from_db(userid)
    return create_json_response(result)

def get_one_task(userid, taskid):
    result = db_handler.task_from_db(userid, taskid)
    return create_json_response(result)

def update_task(content, userid, taskid):
    if "deadline" in content:
        try:
            content["deadline"] = datetime.datetime.strptime(content["deadline"],\
                                    '%d %b %Y %H:%M:%S')
        except:
            result = ["DEADLINE not in the right format", 0]
            return create_json_response(result)
    result = db_handler.update_task_in_db(content, userid, taskid)
    return create_json_response(result)

def delete_task(userid, taskid):
    result = db_handler.delete_task_from_db(userid, taskid)
    return create_json_response(result)

def create_json_response(result):
    if result[1] == 1:
        json_send = {"status" : "success", "data" : result[0]}
    elif result[1] == 0:
        json_send = {"status" : "failure", "error" : result[0]}
    return json.dumps(json_send)

if __name__ == '__main__':
    pass
