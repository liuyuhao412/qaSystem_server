from . import login_view,md5_encryption
from flask import request,jsonify,request
from app.models.user import UserModel,VerificationCodeModel
from datetime import datetime,timedelta
from flask_mail import Mail,Message
from app import db,mail
from manager import app
import random
import re 
import threading

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
def send_email_async(app,msg):
    with app.app_context():
        mail.send(msg)

def send_verification_code(to):
    code = ''.join(random.choice('0123456789') for i in range(6))
    msg = Message(subject='问答系统',recipients=[to],body=f'【问答系统】注册验证码 {code},10分钟有效,请勿告知他人。')
    thread = threading.Thread(target=send_email_async, args=(app,msg))
    thread.start()
    # code = md5_encryption(code)
    return code

@login_view.route('/register/send_code',methods=['POST'])
def send_code():
    email = request.args.get('Email').strip()
    if email == '':
        return jsonify({'code':'0', 'msg': '请输入邮箱'})
    elif not is_valid_email(email):
        return jsonify({'code':'0', 'msg': 'Email format is wrong'})
    else:
        registerUser = UserModel.query.filter(UserModel.email==email).first()
        if registerUser:
            return jsonify({'code':'0', 'msg': '该邮箱已经存在'})
        else:
            code = send_verification_code(email)
            created_time = datetime.utcnow() + timedelta(hours=8)
            expiration_time = created_time + timedelta(minutes=10)
            VerificationCode = VerificationCodeModel.query.filter(VerificationCodeModel.email==email).first()
            if VerificationCode:
                VerificationCode.code = code
                VerificationCode.created_time = created_time
                VerificationCode.expiration_time = expiration_time
                db.session.commit()
            else:
                VerificationCode = VerificationCodeModel(email=email,code=code,created_time=created_time,expiration_time=expiration_time)
                db.session.add(VerificationCode)
                db.session.commit()
            return jsonify({'code':'1', 'msg': '验证码发送成功'})

@login_view.route('/register',methods=['POST'])
def register():
    email = request.args.get('Email').strip()
    code = request.args.get('Code').strip()
    password = request.args.get('Password').strip()
    confirme_password = request.args.get('ConfirmePassword').strip()
    time = datetime.utcnow() + timedelta(hours=8)
    VerificationCode = VerificationCodeModel.query.filter(VerificationCodeModel.email==email).first()
    if VerificationCode:
        VerificationCode_is_valid = VerificationCode.is_valid
        if VerificationCode.expiration_time < time:
            VerificationCode_code = ''
        else:
            VerificationCode_code = VerificationCode.code 
    else:
        VerificationCode_is_valid=''
        VerificationCode_code = ''

    if email == '':
        return jsonify({'code':'0', 'msg': '请输入邮箱'})
    elif not is_valid_email(email):
        return jsonify({'code':'0', 'msg': '邮箱格式错误'})
    elif code == '':
        return jsonify({'code':'0', 'msg': '请输入验证码'})
    elif password =='':
        return jsonify({'code':'0', 'msg': '请输入密码'})
    elif confirme_password == '':
        return jsonify({'code':'0', 'msg': '请再次输入密码'})
    # elif md5_encryption(code) != VerificationCode_code:
    #     return jsonify({'code':'0', 'msg': '验证码错误'})
    elif code != VerificationCode_code:
        return jsonify({'code':'0', 'msg': '验证码错误'})
    elif VerificationCode_is_valid != '有效':
        return jsonify({'code':'0', 'msg': '验证码错误'})
    elif not check_password(password):
        return jsonify({'code':'0', 'msg': '密码需由8位以上、大小写字母、特殊字符组成'})
    elif password != confirme_password:
        return jsonify({'code':'0', 'msg': '两次密码不一致'})
    else:
        registerUser = UserModel.query.filter(UserModel.email==email).first()
        if registerUser:
            return jsonify({'code':'0', 'msg': '邮箱已经存在'})
        else:
            register_time = datetime.utcnow() + timedelta(hours=8)
            md5_pwd = md5_encryption(password)
            newUser = UserModel(username=email,email=email, password=md5_pwd,register_time=register_time)
            VerificationCode = VerificationCodeModel.query.filter(VerificationCodeModel.email==email).first()
            VerificationCode.is_valid = '无效'
            db.session.add(newUser)
            db.session.commit()
            return jsonify({'code':'1', 'msg': '注册成功'})