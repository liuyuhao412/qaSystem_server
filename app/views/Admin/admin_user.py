from . import admin_view,md5_encryption,is_valid_email,check_password
from flask import request,jsonify
from app.models.user import UserModel,VerificationCodeModel,LoginLogModel
from datetime import datetime,timedelta
from app import db

@admin_view.route('/admin_user/get_user',methods=['POST'])
def user_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    username = request.args.get('username')
    role = request.args.get('role')
    if not username:
        username = ''
    if not role:
        role = ''
    query = UserModel.query
    if username!='':
        query = query.filter(UserModel.username.like('%{username}%'.format(username=username)))
    if role!='':
        query = query.filter(UserModel.role.like('%{role}%'.format(role=role)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    users = pagination.items
    data = [user.to_json() for user in users]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})


@admin_view.route('/admin_user/add_user',methods=['POST'])
def add_user():
    username = request.args.get('username')
    email = request.args.get('email')
    role = request.args.get('role')
    if not username:
        return jsonify({'code':0,'msg':'请输入用户'})
    if not email:
        return jsonify({'code':0,'msg':'请输入邮箱'})
    if not is_valid_email(email):
        return jsonify({'code':'0', 'msg': '邮箱格式错误'})
    if not role:
        return jsonify({'code':0,'msg':'请选择角色'})
    user = UserModel.query.filter(UserModel.username==username).first()
    if user:
        return jsonify({'code':0,'msg':'用户已存在'})
    user = UserModel.query.filter(UserModel.email==email).first()
    if user:
        return jsonify({'code':0,'msg':'邮箱已存在'})
    else:
        new_password = "Xxx@123456."
        md5_password = md5_encryption(new_password)
        register_time = datetime.utcnow() + timedelta(hours=8)
        user = UserModel(username=username,email=email,password=md5_password,role=role,register_time=register_time)
        VerificationCode = VerificationCodeModel(email=email,code='无',created_time=register_time,expiration_time=register_time)
        db.session.add(user)
        db.session.add(VerificationCode)
        db.session.commit()
        return jsonify({'code':'1', 'msg': '添加用户信息成功'})

@admin_view.route('/admin_user/update_user',methods=['POST'])
def update_user():
    username = request.args.get('username')
    email = request.args.get('email')
    role = request.args.get('role')
    if not username:
        return jsonify({'code':0,'msg':'请输入用户'})
    user = UserModel.query.filter(UserModel.email==email).first()
    Logs = LoginLogModel.query.filter(LoginLogModel.user_id == user.id).all()
    for Log in Logs:
        Log.username = username
    user.username = username
    user.role = role
    db.session.commit()
    return jsonify({'code':'1', 'msg': '修改用户信息成功'})

@admin_view.route('/admin_user/delete_user',methods=['post'])
def delete_user():
    email = request.args.get('email')
    user = UserModel.query.filter(UserModel.email==email).first()
    Logs = LoginLogModel.query.filter(LoginLogModel.user_id == user.id).all()
    for Log in Logs:
        db.session.delete(Log)
    VerificationCode = VerificationCodeModel.query.filter(VerificationCodeModel.email==email).first()
    db.session.delete(user) 
    db.session.delete(VerificationCode) 
    db.session.commit()
    return  jsonify({'code':1,'msg':'删除用户信息成功'})

@admin_view.route('/admin_user/set_password',methods=['post'])
def set_password():
    email = request.args.get('email')
    user = UserModel.query.filter(UserModel.email==email).first()
    user.password = md5_encryption('Xxx@123456.')
    db.session.commit()
    return  jsonify({'code':1,'msg':'密码重置成功'})

@admin_view.route('/admin_user/update_password',methods=['post'])
def update_password():
    username = request.args.get('username')
    new_pwd = request.args.get('new_pwd')
    confirm_pwd = request.args.get('confirm_pwd')
    if not username:
        return jsonify({'code':0,'msg':'该用户不存在'})
    if not new_pwd:
        return jsonify({'code':0,'msg':'请输入新密码'})
    elif not confirm_pwd:
        return jsonify({'code':0,'msg':'请再次输入新密码'})
    elif not check_password(new_pwd):
        return jsonify({'code':'0', 'msg': '新密码格式不正确'})
    else:
        if new_pwd == confirm_pwd:
            user = UserModel.query.filter(UserModel.username==username).first()
            user.password = md5_encryption(new_pwd)
            db.session.commit()
            return  jsonify({'code':1,'msg':'密码修改成功'})
        else:
            return  jsonify({'code':0,'msg':'两次密码不一致'})