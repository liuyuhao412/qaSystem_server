from . import user_view
from flask import request,jsonify
from app.models.user import chatHistoryModel

@user_view.route('/get_history',methods=['POST'])
def get_user_history():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    username = request.args.get('username')
    role = request.args.get('role')
    if not role:
        role = ''
    query = chatHistoryModel.query
    print(username)
    query = query.filter(chatHistoryModel.username==username)
    if role!='':
        query = query.filter(chatHistoryModel.role.like('%{role}%'.format(role=role)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    historys = pagination.items
    data = [history.to_json() for history in historys]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})