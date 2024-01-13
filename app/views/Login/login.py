from . import login_view
from flask import request,jsonify
from app.models.user import UserModel,LoginLogModel
from app import db

@login_view.route('/login',methods=['POST'])
def login():
    username = request.args.get('Username').strip()
    password = request.args.get('Password').strip()
    if username == '':
        return jsonify({'code':'0', 'msg': '请输入账号'})
    elif password =='':
        return jsonify({'code':'0', 'msg': '请输入密码'})
    else:
        loginUser = UserModel.query.filter(UserModel.username==username).first()
        if loginUser:
            if loginUser.password == password:
                if loginUser.role == 'admin':
                    LoginLog = LoginLogModel(user_id=loginUser.id,username=loginUser.username)
                    db.session.add(LoginLog)
                    db.session.commit()
                    return  jsonify({'code':'2', 'msg': '登录成功'})
                else:
                    LoginLog = LoginLogModel(user_id=loginUser.id,username=loginUser.username)
                    db.session.add(LoginLog)
                    db.session.commit()
                    return jsonify({'code':'1', 'msg': '登录成功'}) 
        else:
            return jsonify({'code':'0','msg':'账号或密码错误'})