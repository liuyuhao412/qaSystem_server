from . import admin_view
from flask import request,jsonify
from app.models.user import LoginLogModel

@admin_view.route('/admin_log/get_log',methods=['POST'])
def log_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    
    email = request.args.get('email')
    role = request.args.get('role')
    if not email:
        email = ''
    if not role:
        role = ''
    query = LoginLogModel.query
    if email!='':
        query = query.filter(LoginLogModel.email.like('%{email}%'.format(email=email)))
    if role!='':
        query = query.filter(LoginLogModel.role.like('%{role}%'.format(role=role)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    logs = pagination.items
    data = [log.to_json() for log in logs]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})