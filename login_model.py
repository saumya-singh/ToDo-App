# from flask_pymongo import PyMongo
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps
# from server import mongo
from passlib.apps import custom_app_context as pwd_context


def user_registration(content):
    client  = MongoClient()
    db = client.todo_database
    username = content["username"]
    email = content["email"]
    password = content["password"]
    username_exist = db.users.find_one({"username" : username})
    if username_exist is not None:
        return create_json_response("Username already exists", 0, 409)
    email_exist = db.users.find_one({"email" : email})
    if email_exist is not None:
        return create_json_response("E-mail already exists", 0, 409)
    password_hash = hash_password(password)
    user_registration_details = {"username" : username, "email" : email, \
                                            "password_hash" : password_hash}
    try:
        return_values = db.users.insert_one(user_registration_details)
        # user_id = return_values.inserted_id
        # user_details = dumps(db.users.find_one({"_id" : ObjectId(user_id)}))
        # json_user_details = json.loads(user_details)
        # json_user_details["_id"] = json_user_details["_id"]["$oid"]
        return create_json_response("User successfully added.", 1, 200)
    except:
        return create_json_response("Cannot add the user in the database", 0, 500)


def user_validation(content):
    client  = MongoClient()
    db = client.todo_database
    email = content["email"]
    password = content["password"]
    user = dumps(db.users.find_one({"email" : email}))
    if user is None:
        return create_json_response("No account with this E-mail ID", 0, 400)
    user = json.loads(user)
    user['_id'] = user['_id']['$oid']
    password_hash = user["password_hash"]
    verification_result = verify_password(password, password_hash)
    if verification_result is True:
        return create_json_response(user, 1, 200)
    if verification_result is False:
        return create_json_response("Incorrect Password", 0, 400)

def create_json_response(data, status, status_code):
    if status == 1:
        json_sent = {"status" : "success", "data" : data}
    elif status == 0:
        json_sent = {"status" : "failure", "error" : data}
    return (json_sent, status_code)

def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)
