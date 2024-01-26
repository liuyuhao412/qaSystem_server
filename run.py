# 创建app实例，控制运行
from app import create_app,db
from app.models import user
from flask import request
from flask_cors import CORS


app = create_app('development')
CORS(app)



if __name__ == '__main__':
    app.run()   
