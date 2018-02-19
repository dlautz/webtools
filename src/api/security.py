from src.common.utils import Utils
from src.models.users.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and Utils.check_hashed_password(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)