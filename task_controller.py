#!/usr/bin/env python3

from flask import Flask
from flask import request
from task_model import insert_task

app = Flask(__name__)

@app.route('/api/users/<userid>/tasks/', methods = ["POST"])
def insert(userid):
	content = request.get_json()
	return insert_task(content, userid)

if __name__ == '__main__':
   app.run(debug = True)
