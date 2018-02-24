from src.common.database import Database
import src.models.notes.constants as NoteConstants
import uuid
import datetime


class Note(object):
    def __init__(self, notebook_id, notebook_title, title, content, author, url="", tags=[], last_updated=None, _id=None):
        self.notebook_id = notebook_id
        self.notebook_title = notebook_title
        self.title = title
        self.content = content
        self.author = author
        self.url = url
        self.tags = tags
        self.last_updated = datetime.datetime.utcnow() if last_updated is None else last_updated
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def from_notebook(cls, notebook_id):
        return [cls(**elem) for elem in Database.find(NoteConstants.COLLECTION, {'notebook_id': notebook_id})]

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(NoteConstants.COLLECTION, {'_id': id}))

    @classmethod
    def find_by_tag(cls, tag):
        return [cls(**elem) for elem in Database.find(NoteConstants.COLLECTION, {'tags': tag})]

    def update(self):
        Database.update(NoteConstants.COLLECTION, {'_id': self._id}, self.json())

    def add_tag(self, tag):
        Database.update(NoteConstants.COLLECTION, {'_id': self._id}, {'$addToSet': {'tags': tag}})

    def remove_tag(self, tag):
        Database.update(NoteConstants.COLLECTION, {'_id': self._id}, {'$pull': {'tags': tag}})

    def save_to_mongo(self):
        Database.insert(NoteConstants.COLLECTION, self.json())

    def json(self):
        return {
            'notebook_id': self.notebook_id,
            'notebook_title': self.notebook_title,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'tags': self.tags,
            'last_updated': self.last_updated,
            '_id': self._id
        }

    def delete(self):
        Database.remove(NoteConstants.COLLECTION, {'_id': self._id})

    @staticmethod
    def delete_notes(notebook_id):
        Database.remove(NoteConstants.COLLECTION, {'notebook_id': notebook_id})