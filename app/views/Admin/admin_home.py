from . import admin_view
from flask import request,jsonify
from app.models.user import UserModel,LoginLogModel
from sqlalchemy import func
from app import db

@admin_view.route('/admin_home/get_user_count',methods=['GET'])
def get_user_count():
    query = UserModel.query.filter(UserModel.role=='user')
    count = query.count() 
    return jsonify({'code':1,'msg':'请求成功','count':count})


@admin_view.route('/admin_home/get_register_list',methods=['GET'])
def get_register_list():
    all_months = list(range(1, 13))
    #extract从时间中提取月份
    user_counts_by_month = (
    db.session.query(
        func.extract('month', UserModel.register_time).label('month'),
        func.count().label('user_count')
    )
    .filter(UserModel.role == 'user')
    .group_by(func.extract('month', UserModel.register_time))
    .all()
    )
    user_counts_dict = dict(user_counts_by_month)
    user_list = [(month-1, user_counts_dict.get(month, 0)) for month in all_months]
    return jsonify({'code':1,'msg':'请求成功','user_list':user_list})   

@admin_view.route('/admin_home/get_user_log',methods=['GET'])
def get_user_log():
    query = LoginLogModel.query.filter(LoginLogModel.role=='user')
    count = query.count() 
    return jsonify({'code':1,'msg':'请求成功','count':count})


@admin_view.route('/admin_home/get_login_list',methods=['GET'])
def get_login_list():
    all_months = list(range(1, 13))
    #extract从时间中提取月份
    login_counts_by_month = (
    db.session.query(
        func.extract('month', LoginLogModel.login_time).label('month'),
        func.count().label('log_count')
    )
    .filter(LoginLogModel.role == 'user')
    .group_by(func.extract('month', LoginLogModel.login_time))
    .all()
    )
    login_counts_dict = dict(login_counts_by_month)
    login_counts_list = [(month-1, login_counts_dict.get(month, 0)) for month in all_months]
    return jsonify({'code':1,'msg':'请求成功','user_list':login_counts_list})   