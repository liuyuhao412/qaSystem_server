from flask import Blueprint
from hashlib import md5
login_view = Blueprint('login_view',__name__)

def md5_encryption(input):
    m = md5()
    m.update(input.encode())
    output = m.hexdigest()
    return output

def generate_random_token(length=32):
    token = secrets.token_hex(length)
    md5_token = md5_encryption(token)
    return md5_token

from .login import *
from .register import *