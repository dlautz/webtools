from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.models.notes.note import Note
from src.models.notebooks.notebook import Notebook
from src.models.users.user import User
from src.models.tags.tag import Tag
import datetime
import src.models.users.decorators as user_decorators


note_blueprint = Blueprint('notes', __name__)


@note_blueprint.route('/list/<string:notebook_id>')
@user_decorators.requires_login
def get_notes(notebook_id):
    notebook = Notebook.find_by_id(notebook_id)
    notes = notebook.get_notes()

    user = User.find_by_username(session['username'])
    tags = user.get_tags()

    return render_template('notebooks/notes.html', notes=notes, notebook_title=notebook.title, notebook_id=notebook._id, tags=tags)


@note_blueprint.route('/new/<string:notebook_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_note(notebook_id):
    if request.method == 'POST':
        title = request.form['title']
        content = ""

        notebook = Notebook.find_by_id(notebook_id)
        notebook.increment_note()

        new_note = Note(notebook_id, notebook.title, title, content, session['username'])
        new_note.save_to_mongo()

        # return redirect(url_for('.get_notes', notebook_id=notebook_id))
        return redirect(url_for('.edit_note', note_id=new_note._id))

    return render_template('notes/new_note.html')


@note_blueprint.route('/<string:note_id>')
@user_decorators.requires_login
def get_note(note_id):
    note = Note.find_by_id(note_id)
    return render_template('notes/note.html', note=note)


@note_blueprint.route('/edit/<string:note_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_note(note_id):
    note = Note.find_by_id(note_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notebook = request.form['notebookNames']

        if notebook != note.notebook_title:
            old_notebook = Notebook.find_by_title(note.notebook_title)
            old_notebook.decrement_note()

            new_notebook = Notebook.find_by_title(notebook)
            new_notebook.increment_note()

            note.notebook_title = new_notebook.title
            note.notebook_id = new_notebook._id

        note.title = title
        note.content = content
        note.last_updated = datetime.datetime.utcnow()

        note.update()

        return redirect(url_for('.get_notes', notebook_id=note.notebook_id))

    notebooks = Notebook.find_by_username(session['username'])

    return render_template('notes/edit_note.html', note=note, notebooks=notebooks)


@note_blueprint.route('/add_tag/<string:note_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def add_tag(note_id):
    note = Note.find_by_id(note_id)
    if request.method == 'POST':
        new_tag = request.form['name']
        existing_tag = request.form['userTags']

        if new_tag:

            if new_tag in note.tags:
                return "Tag already exists for that note"  # setup error for this situation.

            else:

                note.add_tag(new_tag)

                if Tag.exists(new_tag, session['username']) is not None:
                    Tag.find_by_name(new_tag, session['username']).increment_counter()
                else:
                    Tag(new_tag, session['username']).save_to_mongo()

        else:

            if existing_tag in note.tags:
                return "Tag already exists for that note"  # setup error for this situation.

            else:

                note.add_tag(existing_tag)

                Tag.find_by_name(existing_tag, session['username']).increment_counter()

        return redirect(url_for('.get_notes', notebook_id=note.notebook_id))

    tags = Tag.find_by_username(session['username'])

    return render_template('notes/add_tag.html', note=note, tags=tags)


@note_blueprint.route('/remove_tag/<string:note_id>/<string:tag>')
@user_decorators.requires_login
def remove_tag(note_id, tag):
    note = Note.find_by_id(note_id)

    note.remove_tag(tag)
    Tag.find_by_name(tag, session['username']).decrement_counter()

    return redirect(url_for('.get_notes', notebook_id=note.notebook_id))


@note_blueprint.route('/delete/<string:note_id>')
@user_decorators.requires_login
def delete_note(note_id):
    note = Note.find_by_id(note_id)
    notebook_id = note.notebook_id
    notebook = Notebook.find_by_id(notebook_id)

    for tag in note.tags:
        Tag.find_by_name(tag, session['username']).decrement_counter()

    note.delete()
    notebook.decrement_note()

    return redirect(url_for('.get_notes', notebook_id=notebook_id))


@note_blueprint.route('/tag/<string:tag>')
@user_decorators.requires_login
def get_tag(tag):
    notes = Note.find_by_tag(tag, session['username'])

    return render_template('notes/by_tag.html', notes=notes, tag_name=tag)




