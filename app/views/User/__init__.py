from flask import Blueprint
from hashlib import md5
user_view = Blueprint('user_view',__name__)

from .chat import *
from .history import *
from .home import *
