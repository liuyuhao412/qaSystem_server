from flask import Blueprint
from hashlib import md5
login_view = Blueprint('login_view',__name__)

def md5_encryption(input):
    m = md5()
    m.update(input.encode())
    output = m.hexdigest()
    return output

from .login import *
from .register import *