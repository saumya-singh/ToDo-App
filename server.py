from flask import Flask, request, render_template, url_for, session, redirect
from flask_json import FlaskJSON, JsonError, as_json
from flask_pymongo import PyMongo
import task_model, login_model, json, os

app = Flask(__name__, static_folder = 'static', static_url_path = '')
FlaskJSON(app)

app.config['MONGO_DBNAME'] = 'todo_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_database'
mongo = PyMongo(app)

@app.route('/')
def register_page():
	return render_template('register.html')

@app.route('/login/')
def login_page():
	return render_template('login.html')

@app.route('/api/register/', methods=['POST'])
@as_json
def register():
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = login_model.user_registration(content)
	return result[0], result[1]

@app.route('/api/login/', methods=['POST'])
@as_json
def login():
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = login_model.user_validation(content)
	if result[1] == 200:
		session['userid'] = result[0]['data']['_id']
	return result[0], result[1]

@app.route('/logout/')
def logout():
	if 'userid' in session:
		session.pop('userid', None)
	return "redirect", 302

@app.route('/tasks/')
def task_page():
	if 'userid' in session:
		return render_template('task.html')
	else:
		return render_template('login.html')

@app.route('/api/tasks/', methods = ["POST"])
def insert():
	if 'userid' in session:
		userid = session.get('userid')
		content = json.loads(request.get_json())
		if not isinstance(content, dict):
			raise JsonError(description='Invalid JSON')
		result = task_model.insert_task(content, userid)
		return result[0], result[1]
	else:
		return redirect('/login/', 302)

@app.route('/api/tasks/', methods = ["GET"])
def get_all_tasks():
	if 'userid' in session:
		userid = session.get('userid')
		result = task_model.get_tasks_list(userid)
		return result[0], result[1]
	else:
		return redirect('/login/', 302)

@app.route('/api/tasks/<taskid>/', methods = ["GET"])
def get_task(taskid):
	if 'userid' in session:
		userid = session.get('userid')
		result = task_model.get_one_task(userid, taskid)
		return result[0], result[1]
	else:
		return redirect('/login/', 302)

@app.route('/api/tasks/<taskid>/', methods = ["PUT"])
def update(taskid):
	if 'userid' in session:
		userid = session.get('userid')
		content = request.get_json()
		if not isinstance(content, dict):
			raise JsonError(description='Invalid JSON')
		result = task_model.update_task(content, userid, taskid)
		return result[0], result[1]
	else:
		return redirect('/login/', 302)

@app.route('/api/tasks/<taskid>/', methods = ["DELETE"])
def delete(taskid):
	if 'userid' in session:
		userid = session.get('userid')
		result = task_model.delete_task(userid, taskid)
		return result[0], result[1]
	else:
		return redirect('/login/', 302)

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True)
