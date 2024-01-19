from flask import Blueprint
from hashlib import md5
import re
admin_view = Blueprint('admin_view',__name__)

def md5_encryption(input):
    m = md5()
    m.update(input.encode())
    output = m.hexdigest()
    return output

def is_valid_email(email):
    # 正则表达式用于检查邮箱格式
    email_pattern = r'^\S+@\S+\.\S+$' 
    return re.match(email_pattern, email) is not None

def check_password(password):
    # 密码要求：8位以上，包含数字、大小写字母和特殊字符
    pattern = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=])[0-9a-zA-Z!@#$%^&*()-_+=]{8,}$')
    
    # 使用正则表达式检查密码格式
    if pattern.match(password):
        return True
    else:
        return False
    
def to_json(input_list):
    result_list = [{'id': idx + 1, 'name': item} for idx, item in enumerate(input_list)]
    return result_list

def paginate(data_list, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_data = data_list[start_index:end_index]
    return paginated_data


from .admin_log import *
from .admin_code import *
from .admin_user import *
from .admin_model import *
from .upload_file import *