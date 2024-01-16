from . import admin_view
from flask import request,jsonify
from app.models.user import VerificationCodeModel

@admin_view.route('/admin_code/get_code',methods=['GET','POST'])
def code_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    
    username = request.args.get('username')
    if not username:
        username = ''
    query = VerificationCodeModel.query
    if username!='':
        query = query.filter(VerificationCodeModel.email.like('%{username}%'.format(email=username)))
    count = query.count() # 符合条件的记录总数
    pagination = query.paginate(page,per_page=limit,error_out=False)
    codes = pagination.items
    data = [code.to_json() for code in codes]
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data})