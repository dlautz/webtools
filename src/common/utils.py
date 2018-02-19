from werkzeug.security import generate_password_hash, check_password_hash
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password, method='sha256', salt_length=8)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return check_password_hash(hashed_password, password)

    # Look for better email validation
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False