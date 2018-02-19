import os


SECRET_KEY = os.urandom(24)
JWT_SECRET_KEY = os.urandom(24)
DEBUG = True
ADMINS = frozenset([
    "dlautz", "dave"
])