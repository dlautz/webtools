from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, create_jwt, get_jwt_identity
from src.models.users.user import User
from src.models.tasks.task import Task
from src.models.notebooks.notebook import Notebook
from src.models.notes.note import Note
from src.common.utils import Utils
import datetime

api_blueprint = Blueprint('api', __name__)


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@api_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.find_by_username(username)
    if user and Utils.check_hashed_password(password, user.password):
        ret = {'jwt': create_jwt(identity=username)}
        return jsonify(ret), 200

    return jsonify({"msg": "Bad username or password"}), 401


@api_blueprint.route('/protected')
@jwt_required
def protected():
    return jsonify({"hello from": get_jwt_identity()}), 200


@api_blueprint.route('/tasks')
@jwt_required
def get_tasks():
    tasks = Task.find_all_by_username(get_jwt_identity())
    if len(tasks) == 0:
        return jsonify({"msg": "no tasks"}), 204

    tasks_json = [task.json() for task in tasks]

    return jsonify({"tasks": tasks_json}), 200


@api_blueprint.route('/create_task', methods=['POST'])
@jwt_required
def create_task():
    data = request.get_json()
    print(data)
    task = data['task']
    category = 'new'
    status = 'open'
    list = 'inbox'
    due = datetime.datetime.utcnow()

    new_task = Task(task, get_jwt_identity(), category, due, status, list)
    new_task.save_to_mongo()

    return jsonify({"msg": "task created"}), 201


@api_blueprint.route('/create_note', methods=['POST'])
@jwt_required
def create_note():
    data = request.get_json()
    title = ""
    content = data['url'] + '\n\n' + data['note']

    notebook = Notebook.find_by_title('inbox')
    notebook.increment_note()

    new_note = Note(notebook._id, notebook.title, title, content, get_jwt_identity())
    new_note.save_to_mongo()

    return jsonify({"msg": "note created"}), 201