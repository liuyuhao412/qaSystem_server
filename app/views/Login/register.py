from . import login_view
from flask import request,jsonify,request
from app.models.user import UserModel,VerificationCodeModel
from datetime import datetime,timedelta
from flask_mail import Mail,Message
from app import db,mail
import random

def sendEmail(to):
    code = ''.join(random.choice('0123456789') for i in range(6))
    msg = Message(subject='问答系统',recipients=[to],body=f'【问答系统】登录验证码 {code},10分钟有效,请勿告知他人。')
    mail.send(msg)
    return code

@login_view.route('/send_code',methods=['POST'])
def send_code():
    email = request.args.get('Username').strip()
    if email == '':
        return jsonify({'code':'0', 'msg': 'Please input email'})
    else:
        registerUser = UserModel.query.filter(UserModel.email==email).first()
        if registerUser:
            return jsonify({'code':'0', 'msg': 'email is already'})
        else:
            code = sendEmail(email)
            # VerificationCode = VerificationCodeModel()
            return jsonify({'code':'1', 'msg': 'Verification code sent successfully'})

@login_view.route('/register',methods=['POST'])
def register():
    username = request.args.get('Username').strip()
    code = request.args.get('Code').strip()
    password = request.args.get('Password').strip()
    confirme_password = request.args.get('ConfirmePassword').strip()
    if username == '':
        return jsonify({'code':'0', 'msg': 'Please input username'})
    elif code == '':
        return jsonify({'code':'0', 'msg': 'Please input code'})
    elif password =='':
        return jsonify({'code':'0', 'msg': 'Please input password'})
    elif confirme_password == '':
        return jsonify({'code':'0', 'msg': 'Please input password again'})
    elif password != confirme_password:
        return jsonify({'code':'0', 'msg': 'Two passwords do not match'})
    else:
        registerUser = UserModel.query.filter(UserModel.username==username).first()
        if registerUser:
            return jsonify({'code':'0', 'msg': 'Username is already'})
        else:
            return jsonify({'code':'1', 'msg': 'Register successfully'})