import hashlib
import os

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
BOT_TOKEN_HASH = hashlib.sha256(os.environ['BOT_TOKEN'].encode())
COOKIE_NAME = 'auth-token'
