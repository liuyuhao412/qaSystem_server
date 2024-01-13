from flask import Blueprint
login_view = Blueprint('login_view',__name__)

from .login import *
from .register import *