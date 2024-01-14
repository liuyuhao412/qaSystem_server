# 创建app实例，控制运行
from app import create_app,db
from app.models import user

app = create_app('development')

if __name__ == '__main__':
    app.run()   
