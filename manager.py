# 创建app实例，控制运行
from app import create_app,db
from flask_script import Manager
from app.models import user
from app.models.user import LLMConfigModel


app = create_app('development')
manager = Manager(app=app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()

@manager.command
def init_LLMConfig():
    LLMConfig1 = LLMConfigModel(key='top_k',value='3')
    LLMConfig2 = LLMConfigModel(key='score_threshold',value='1.0')
    LLMConfig3 = LLMConfigModel(key='score_Temperature',value='0.7')
    LLMConfig4 = LLMConfigModel(key='kb_name',value='Olympics')
    db.session.add(LLMConfig1)
    db.session.add(LLMConfig2)
    db.session.add(LLMConfig3)
    db.session.add(LLMConfig4)
    db.session.commit()

if __name__ == '__main__':
    manager.run()

