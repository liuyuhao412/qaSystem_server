from . import admin_view
from flask import request,jsonify
from app.models.user import LoginLogModel

@admin_view.route('/admin_log/get_log',methods=['GET','POST'])
def user_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    
    username = request.args.get('username')
    if not username:
        username = ''

    query = LoginLogModel.query
    if username!='':
        query = query.filter(LoginLogModel.username.like('%{username}%'.format(username=username)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    users = pagination.items
    data = [user.to_json() for user in users]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})