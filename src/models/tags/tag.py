from src.common.database import Database
import src.models.tags.constants as TagConstants
import uuid


class Tag(object):
    def __init__(self, name, username, counter=1, _id=None):
        self.name = name
        self.username = username
        self.counter = counter
        self._id = uuid.uuid4().hex if _id is None else _id

    def increment_counter(self):
        self.counter += 1
        self.update()

    def decrement_counter(self):
        self.counter -= 1
        if self.counter == 0:
            self.delete()
        else:
            self.update()

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "username": self.username,
            "counter": self.counter
        }

    def save_to_mongo(self):
        Database.insert(TagConstants.COLLECTION, self.json())

    def update(self):
        Database.update(TagConstants.COLLECTION, {'_id': self._id}, self.json())

    def delete(self):
        Database.remove(TagConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def find_by_name(cls, name, username):
        return cls(**Database.find_one(TagConstants.COLLECTION, {'name': name, 'username': username}))

    @classmethod
    def find_by_username(cls, username):
        return [cls(**elem) for elem in Database.find(TagConstants.COLLECTION, {'username': username})]

    @staticmethod
    def exists(name, username):
        return Database.find_one(TagConstants.COLLECTION, {'name': name, 'username': username})


