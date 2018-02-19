import uuid
import src.models.users.constants as UserConstants
from src.common.database import Database
from src.common.utils import Utils
from src.models.notebooks.notebook import Notebook
from src.models.tags.tag import Tag
import src.models.users.errors as UserErrors


class User(object):
    def __init__(self, username, password, email, lists=['main', 'inbox'], _id=None):
        self.username = username
        self.password = password
        self.email = email
        self.lists = lists
        self._id = uuid.uuid4().hex if _id is None else _id
        self.id = self._id

    def __repr__(self):
        return "<User {}>".format(self.username)

    @staticmethod
    def is_login_valid(username, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"username": username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("User not found.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Incorrect Password")

        return True

    @staticmethod
    def register_user(username, password, email):
        user_data = Database.find_one(UserConstants.COLLECTION, {"username": username})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("Username taken.  Please choose another one.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Invalid email format.")

        User(username, Utils.hash_password(password), email).save_to_mongo()
        notebook = Notebook("inbox", username)
        notebook.save_to_mongo()

        return True

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "lists": self.lists,
            "_id": self._id
        }

    @classmethod
    def find_by_username(cls, username):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'username': username}))

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'_id': id}))

    def get_notebooks(self):
        return Notebook.find_by_username(self.username)

    def get_tags(self):
        return Tag.find_by_username(self.username)

    def update(self):
        Database.update(UserConstants.COLLECTION, {'_id': self._id}, self.json())



