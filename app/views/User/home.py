from . import user_view
from flask import request,jsonify
from datetime import datetime,timedelta
from app.models.user import LoginLogModel
@user_view.route('/get_time',methods=['POST'])
def get_time():
    username = request.args.get('username')
    print(username)
    last_login_log = LoginLogModel.query.filter_by(username=username).order_by(LoginLogModel.login_time.desc()).first()
    time = last_login_log.login_time
    if time is None:
        time =  datetime.utcnow() + timedelta(hours=8)

    time = "您上次登录,时间是" + time.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({'code':1,'msg':'获取时间成功','time':time})