#!/usr/bin/env python3
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_pymongo import PyMongo
import task_model

app = Flask(__name__)
FlaskJSON(app)

app.config['MONGO_DBNAME'] = 'todo_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_database'
mongo = PyMongo(app)

@app.route('/api/users/<userid>/tasks/', methods = ["POST"])
@as_json
def insert(userid):
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = task_model.insert_task(content, userid)
	return result[0], result[1]

@app.route('/api/users/<userid>/tasks/', methods = ["GET"])
@as_json
def get_all_tasks(userid):
	result = task_model.get_tasks_list(userid)
	return result[0], result[1]

@app.route('/api/users/<userid>/tasks/<taskid>/', methods = ["GET"])
@as_json
def get_task(userid, taskid):
	result = task_model.get_one_task(userid, taskid)
	return result[0], result[1]

@app.route('/api/users/<userid>/tasks/<taskid>/', methods = ["PUT"])
@as_json
def update(userid, taskid):
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = task_model.update_task(content, userid, taskid)
	return result[0], result[1]

@app.route('/api/users/<userid>/tasks/<taskid>/', methods = ["DELETE"])
@as_json
def delete(userid, taskid):
	result = task_model.delete_task(userid, taskid)
	return result[0], result[1]

if __name__ == '__main__':
   app.run(debug = True)