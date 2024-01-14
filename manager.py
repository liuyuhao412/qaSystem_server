# 创建app实例，控制运行
from app import create_app,db
from flask_script import Manager
from app.models import user


app = create_app('development')
manager = Manager(app=app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()


if __name__ == '__main__':
    manager.run()

