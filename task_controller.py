#!/usr/bin/env python3
from flask import Flask, request
import task_model

app = Flask(__name__)

@app.route('/api/users/<userid>/tasks/', methods = ["POST"])
def insert(userid):
	content = request.get_json()
	return task_model.insert_task(content, userid)

@app.route('/api/users/<userid>/tasks/', methods = ["GET"])
def get_tasks(userid):
	return task_model.get_tasks_list(userid)

if __name__ == '__main__':
   app.run(debug = True)
