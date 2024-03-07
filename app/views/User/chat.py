from . import user_view
from flask import request,jsonify
from app.views.Api import chat
from app.models.user import chatHistoryModel,UserModel,LLMConfigModel
from datetime import datetime,timedelta
from app import db


@user_view.route('/chat',methods=['POST'])
def chat():
    question = request.args.get('question')
    username = request.args.get('username')

    '''
    获取模型配置参数
    '''
    config1 = LLMConfigModel.query.filter(LLMConfigModel.key=='top_k').first()
    config2 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_threshold').first()
    config3 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_Temperature').first()
    config4 = LLMConfigModel.query.filter(LLMConfigModel.key=='kb_name').first()
    top_k = config1.value
    score_threshold = config2.value
    score_Temperature = config3.value
    kb_name = config4.value
    user = UserModel.query.filter(UserModel.username==username).first()
    questionModel = chatHistoryModel(message=question,role='user',time=datetime.utcnow() + timedelta(hours=8),user_id=user.id,username = user.username)
    db.session.add(questionModel)
    db.session.commit()
    answer = chat(question=question,name=kb_name,top_k=top_k,score_threshold=score_threshold,temperature=score_Temperature)
    answerModel = chatHistoryModel(message=answer,role='system',time=datetime.utcnow() + timedelta(hours=8),user_id=user.id,username = user.username)
    db.session.add(answerModel)
    db.session.commit()
    return jsonify({'code':'1', 'answer': answer})