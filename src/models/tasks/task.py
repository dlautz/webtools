from src.common.database import Database
import src.models.tasks.constants as TaskConstants
import uuid


class Task(object):
    def __init__(self, task, author, category, due, status, list, _id=None):
        self.task = task
        self.author = author
        self.category = category
        self.due = due
        self.status = status
        self.list = list
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(TaskConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "task": self.task,
            "author": self.author,
            "category": self.category,
            "status": self.status,
            "list": self.list,
            "due": self.due
        }

    def update(self):
        Database.update(TaskConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def find_by_username(cls, username, list):
        return [cls(**elem) for elem in Database.find(TaskConstants.COLLECTION, {'$and': [{'author': username}, {'status': 'open'}, {'list': list}]}).sort('due')]

    @classmethod
    def find_all_by_username(cls, username):
        return [cls(**elem) for elem in Database.find(TaskConstants.COLLECTION, {
            '$and': [{'author': username}, {'status': 'open'}]}).sort('due')]

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(TaskConstants.COLLECTION, {'_id': id}))

    @classmethod
    def find_by_list(cls, username, list):
        return [cls(**elem) for elem in Database.find(TaskConstants.COLLECTION, {'$and': [{'author': username}, {'list': list}]})]

    def delete(self):
        Database.remove(TaskConstants.COLLECTION, {'_id': self._id})




