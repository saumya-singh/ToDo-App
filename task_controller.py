#!/usr/bin/env python3

from flask import Flask
from flask import request
from InsertModel import insert_task_model
import pprint, json

app = Flask(__name__)

@app.route('/api/users/<userid>/tasks/', methods = ["POST"])
def insert_task(userid):
	content = request.get_json()
	title = content["title"]
	description = content["description"]
	deadline = content["deadline"]
	result = insert_task_model(title, description, deadline, userid)
	return result

if __name__ == '__main__':
   app.run(debug = True)
