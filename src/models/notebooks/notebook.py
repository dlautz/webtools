from src.common.database import Database
from src.models.notes.note import Note
import src.models.notebooks.constants as NotebookConstants
import uuid


class Notebook(object):
    def __init__(self, title, author, num_notes=0, _id=None):
        self.title = title
        self.author = author
        self.num_notes = num_notes
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_notes(self):
        return Note.from_notebook(self._id)

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(NotebookConstants.COLLECTION, {'_id': id}))

    def save_to_mongo(self):
        Database.insert(NotebookConstants.COLLECTION, self.json())

    def json(self):
        return {
            'title': self.title,
            'author': self.author,
            'num_notes': self.num_notes,
            '_id': self._id
        }

    @classmethod
    def find_by_username(cls, username):
        return [cls(**elem) for elem in Database.find(NotebookConstants.COLLECTION, {'author': username})]

    def delete(self):
        Note.delete_notes(self._id)
        Database.remove(NotebookConstants.COLLECTION, {'_id': self._id})

    def increment_note(self):
        self.num_notes += 1
        self.update()

    def decrement_note(self):
        self.num_notes -= 1
        self.update()

    def update(self):
        Database.update(NotebookConstants.COLLECTION, {'_id': self._id}, self.json())