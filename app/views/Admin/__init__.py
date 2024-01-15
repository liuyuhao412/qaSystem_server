from flask import Blueprint

admin_view = Blueprint('admin_view',__name__)

from .log import *