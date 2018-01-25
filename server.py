from flask import Flask, request, render_template, url_for
from flask_json import FlaskJSON, JsonError, as_json
from flask_pymongo import PyMongo
import task_model, login_model, json
from flask_login import LoginManager

app = Flask(__name__, static_folder = 'static', static_url_path = '')
FlaskJSON(app)
login = LoginManager(app)

app.config['MONGO_DBNAME'] = 'todo_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_database'
mongo = PyMongo(app)


# from flask import render_template, flash, redirect, url_for, request
# from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.urls import url_parse
# from app import app, db
#
# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     posts = [
#         {
#             'author': {'username': 'John'},
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'username': 'Susan'},
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html', title='Home', posts=posts)


@app.route('/api/login/', methods=['POST'])
def login():
	# if current_user.is_authenticated:
    #     return redirect(url_for('index'))
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = login_model.user_validation(content)
	return result[0], result[1]

@app.route('/api/register/', methods=['POST'])
@as_json
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
	content = request.get_json()
	if not isinstance(content, dict):
		raise JsonError(description='Invalid JSON')
	result = login_model.user_registration(content)
	return result[0], result[1]

# def login():
# 	# if current_user.is_authenticated:
#     #     return redirect(url_for('index'))
# 	content = json.loads(request.get_json())
# 	if not isinstance(content, dict):
# 		raise JsonError(description='Invalid JSON')
# 	result = login_model.user_validation(content)
# 	return result[0], result[1]
#
#
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/users/123/tasks/')
def task_page():
	return render_template('task.html')

@app.route('/api/users/<userid>/tasks/', methods = ["POST"])
@as_json
def insert(userid):
	content = json.loads(request.get_json())
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
