from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.models.notebooks.notebook import Notebook
from src.models.tags.tag import Tag
import src.models.users.decorators as user_decorators


notebook_blueprint = Blueprint('notebooks', __name__)


@notebook_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_notebook():
    if request.method == 'POST':
        title = request.form['title']

        notebook = Notebook(title, session['username'])
        notebook.save_to_mongo()

        return redirect(url_for('users.user_notebooks'))

    return render_template('notebooks/new_notebook.html')


@notebook_blueprint.route('/delete/<string:notebook_id>')
@user_decorators.requires_login
def delete_notebook(notebook_id):
    notebook = Notebook.find_by_id(notebook_id)

    notes = notebook.get_notes()

    for note in notes:
        for tag in note.tags:
            Tag.find_by_name(tag).decrement_counter()
        note.delete()

    notebook.delete()

    return redirect(url_for('users.user_notebooks'))


@notebook_blueprint.route('/edit/<string:notebook_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_notebook(notebook_id):
    notebook = Notebook.find_by_id(notebook_id)
    if request.method == 'POST':
        title = request.form['title']

        notebook.title = title
        notebook.update()

        return redirect(url_for('notes.get_notes', notebook_id=notebook._id))

    return render_template('notebooks/edit_notebook.html', notebook=notebook)