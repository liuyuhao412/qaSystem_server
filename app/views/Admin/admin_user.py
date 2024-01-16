from . import admin_view,md5_encryption
from flask import request,jsonify
from app.models.user import UserModel,VerificationCodeModel
from datetime import datetime,timedelta
from app import db

@admin_view.route('/admin_user/get_user',methods=['POST'])
def user_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    email = request.args.get('email')
    role = request.args.get('role')
    if not email:
        email = ''
    if not role:
        role = ''
    query = UserModel.query
    if email!='':
        query = query.filter(UserModel.email.like('%{email}%'.format(email=email)))
    if role!='':
        query = query.filter(UserModel.role.like('%{role}%'.format(role=role)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    users = pagination.items
    data = [user.to_json() for user in users]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})


@admin_view.route('/admin_user/add_user',methods=['POST'])
def add_user():
    email = request.args.get('email')
    role = request.args.get('role')
    if not email:
        return jsonify({'code':0,'msg':'请输入邮箱'})
    if not role:
        return jsonify({'code':0,'msg':'请选择角色'})
    user = UserModel.query.filter(UserModel.email==email).first()
    if user:
        return jsonify({'code':0,'msg':'邮箱已存在'})
    else:
        new_password = "Xxx@123456."
        md5_password = md5_encryption(new_password)
        register_time = datetime.utcnow() + timedelta(hours=8)
        user = UserModel(email=email,password=md5_password,role=role,register_time=register_time)
        db.session.add(user)
        db.session.commit()
        return jsonify({'code':'1', 'msg': '添加用户信息成功'})

@admin_view.route('/admin_user/update_user',methods=['POST'])
def update_user():
    email = request.args.get('email')
    role = request.args.get('role')
    if not email:
        return jsonify({'code':0,'msg':'请输入邮箱'})
    user = UserModel.query.filter(UserModel.email==email).first()
    user.role = role
    db.session.commit()
    return jsonify({'code':'1', 'msg': '修改用户信息成功'})

@admin_view.route('/admin_user/delete_user',methods=['post'])
def delete_user():
    email = request.args.get('email')
    user = UserModel.query.filter(UserModel.email==email).first()
    db.session.delete(user) 
    db.session.commit()
    return  jsonify({'code':1,'msg':'删除用户信息成功'})

@admin_view.route('/admin_user/set_password',methods=['post'])
def set_password():
    email = request.args.get('email')
    user = UserModel.query.filter(UserModel.email==email).first()
    user.password = md5_encryption('Xxx@123456.')
    db.session.commit()
    return  jsonify({'code':1,'msg':'密码重置成功'})