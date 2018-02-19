from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from src.models.users.user import User
from src.models.tasks.task import Task
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            if User.register_user(username, password, email):
                session['username'] = username
                user = User.find_by_username(username)
                session['list'] = user.lists[0]
                flash("Welcome! You are now registered.")
                return redirect(url_for('.user_notebooks'))
        except UserErrors.UserError as e:
            flash(e.message)
            return redirect(url_for('.register_user'))

    return render_template("users/register.html")


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            if User.is_login_valid(username, password):
                session['username'] = username
                user = User.find_by_username(username)
                session['list'] = user.lists[0]

                return redirect(url_for('.user_notebooks'))
        except UserErrors.UserError as e:
            flash(e.message)
            return redirect(url_for('.login_user'))

    return render_template("users/login.html")  # Need to send message with errors


@user_blueprint.route('/logout')
def logout_user():
    session['username'] = None
    session.clear()
    return redirect(url_for('home'))


@user_blueprint.route('/notebooks')
@user_decorators.requires_login
def user_notebooks():
    user = User.find_by_username(session['username'])
    notebooks = user.get_notebooks()
    tags = user.get_tags()
    return render_template('users/notebooks.html', notebooks=notebooks, tags=tags)


@user_blueprint.route('/lists', methods=['GET', 'POST'])
@user_decorators.requires_login
def manage_lists():
    # This will handle displaying form and adding new list
    user = User.find_by_username(session['username'])

    if request.method == 'POST':
        new_list = request.form['newList']

        user.lists.append(new_list)
        user.update()

        return redirect(url_for('.manage_lists', lists=user.lists))

    return render_template('users/manage_lists.html', lists=user.lists)


@user_blueprint.route('/default_list', methods=['POST'])
@user_decorators.requires_login
def default_list():
    user = User.find_by_username(session['username'])

    new_default = request.form['defaultList']

    user.lists.remove(new_default)
    user.lists.insert(0, new_default)

    user.update()
    session['list'] = user.lists[0]

    return redirect(url_for('.manage_lists', lists=user.lists))


@user_blueprint.route('/delete_list', methods=['POST'])
@user_decorators.requires_login
def delete_list():
    user = User.find_by_username(session['username'])

    remove_list = request.form['deleteList']

    list_tasks =  Task.find_by_list(user.username, remove_list)

    for list_task in list_tasks:
        list_task.delete()

    user.lists.remove(remove_list)
    user.update()
    session['list'] = user.lists[0]

    return redirect(url_for('.manage_lists', lists=user.lists))

