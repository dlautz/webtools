from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.models.tasks.task import Task
from src.models.users.user import User
import datetime
import src.models.users.decorators as user_decorators


task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/list', methods=['GET', 'POST'])
def get_tasks():

    if request.method == 'POST':
        list = request.form['listNames']
        session['list'] = list

        return redirect(url_for('.get_tasks'))

    tasks = Task.find_by_username(session['username'], session['list'])
    user = User.find_by_username(session['username'])

    return render_template('tasks/tasks.html', tasks=tasks, lists=user.lists)


@task_blueprint.route('/new', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task = request.form['task']
        category = request.form['category']
        status = 'open'
        list = request.form['listNames']
        due = datetime.datetime.strptime(request.form['due'], '%Y-%m-%d')

        new_task = Task(task, session['username'], category, due, status, list)
        new_task.save_to_mongo()

        return redirect(url_for('.get_tasks'))

    user = User.find_by_username(session['username'])

    return render_template('tasks/new_task.html', lists=user.lists)


@task_blueprint.route('/edit/<string:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    updated_task = Task.find_by_id(task_id)

    if request.method == 'POST':
        task = request.form['task']
        category = request.form['category']
        list = request.form['listNames']
        due = datetime.datetime.strptime(request.form['due'], '%Y-%m-%d')

        updated_task.task = task
        updated_task.category = category
        updated_task.list = list
        updated_task.due = due

        updated_task.update()

        return redirect(url_for('.get_tasks'))

    user = User.find_by_username(session['username'])

    return render_template('tasks/edit_task.html', task=updated_task, lists=user.lists)


@task_blueprint.route('/complete/<string:task_id>')
def complete_task(task_id):
    task = Task.find_by_id(task_id)

    task.status = 'completed'
    task.update()

    return redirect(url_for('.get_tasks'))


@task_blueprint.route('/<string:task_id>')
def get_task(task_id):
    pass


@task_blueprint.route('/delete/<string:task_id>')
def delete_task(task_id):
    task = Task.find_by_id(task_id)
    task.delete()

    return redirect(url_for('.get_tasks'))

