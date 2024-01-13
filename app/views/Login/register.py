from . import login_view
from flask import request,jsonify
from app.models.user import UserModel,VerificationCodeModel
from app import db

@login_view.route('/register',methods=['POST'])
def register():
    username = request.args.get('Username').strip()
    code = request.args.get('Code').strip()
    password = request.args.get('Password').strip()
    confirme_password = request.args.get('ConfirmePassword').strip()
    if username == '':
        return jsonify({'code':'0', 'msg': '请输入账号'})
    elif code == '':
        return jsonify({'code':'0', 'msg': '请输入验证码'})
    elif password =='':
        return jsonify({'code':'0', 'msg': '请输入密码'})
    elif confirme_password == '':
        return jsonify({'code':'0', 'msg': '请再次输入密码'})
    elif password != confirme_password:
        return jsonify({'code':'0', 'msg': '两次密码不一致'})
    else:
        registerUser = UserModel.query.filter(UserModel.username==username).first()
        if registerUser:
            return jsonify({'code':'0', 'msg': '账号已经存在'})
        else:
            return jsonify({'code':'1', 'msg': '注册成功'})