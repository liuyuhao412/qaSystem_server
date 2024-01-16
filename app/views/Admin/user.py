from . import admin_view
from flask import request,jsonify
from app.models.user import UserModel

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