from flask import Blueprint
from hashlib import md5

admin_view = Blueprint('admin_view',__name__)

def md5_encryption(input):
    m = md5()
    m.update(input.encode())
    output = m.hexdigest()
    return output


from .admin_log import *
from .admin_code import *
from .admin_user import *