from . import login_view,md5_encryption,generate_random_token
from flask import request,jsonify
from app.models.user import UserModel,LoginLogModel
from datetime import datetime,timedelta
from app import db
import secrets
# 生成随机 Token


@login_view.route('/login',methods=['POST'])
def login():
    ip = request.headers.get('X-Forwarded-For')
    if not ip:
        ip = request.remote_addr
    username = request.args.get('Username').strip()
    password = request.args.get('Password').strip()
    if username == '':
        return jsonify({'code':'0', 'msg': 'Please input username'})
    elif password =='':
        return jsonify({'code':'0', 'msg': 'Please input password'})
    else:
        loginUser = UserModel.query.filter(UserModel.username==username).first()
        if loginUser:
            if loginUser.password == md5_encryption(password):
                if loginUser.role == 'admin':
                    time = datetime.utcnow() + timedelta(hours=8)
                    role = loginUser.role
                    LoginLog = LoginLogModel(user_id=loginUser.id,username=loginUser.username,role=role,login_time=time,ip=ip)
                    db.session.add(LoginLog)
                    db.session.commit()
                    store = {'token':generate_random_token(),'username':loginUser.username}
                    return  jsonify({'code':'2','store':store ,'msg': 'Login successful'})
                else:
                    time = datetime.utcnow() + timedelta(hours=8)
                    role = loginUser.role
                    LoginLog = LoginLogModel(user_id=loginUser.id,username=loginUser.username,role=role,login_time=time,ip=ip)
                    db.session.add(LoginLog)
                    db.session.commit()
                    store = {'token':generate_random_token(),'username':loginUser.username}
                    return jsonify({'code':'1', 'store':store,'msg': 'Login successful'}) 
            else:
                return jsonify({'code':'0','msg':'Username or password error'})
        else:
            return jsonify({'code':'0','msg':'Username or password error'})