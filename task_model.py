#!/usr/bin/env python3
import datetime
import db_handler

def insert_task(content, userid):
    title = content["title"]
    description = content["description"]
    deadline = content["deadline"]
    deadline = datetime.datetime.strptime(deadline, '%d %b %Y %H:%M:%S')
    task = {"title" : title, "description" : description, \
            "created_time" : datetime.datetime.utcnow(), "created_by" : userid,\
            "deadline" : deadline, "completed" : False}
    return db_handler.insert_to_db(task)

if __name__ == '__main__':
    pass
