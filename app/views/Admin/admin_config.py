from . import admin_view
from flask import request,jsonify
from app.models.user import LLMConfigModel
from app import db

@admin_view.route('/admin_model/get_config',methods=['POST'])
def get_config():
    config1 = LLMConfigModel.query.filter(LLMConfigModel.key=='top_k').first()
    config2 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_threshold').first()
    config3 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_Temperature').first()
    config4 = LLMConfigModel.query.filter(LLMConfigModel.key=='kb_name').first()
    top_k = int(config1.value)
    score_threshold =  float(config2.value)
    score_Temperature =  float(config3.value)
    kb_name =  config4.value
    data = {'top_k':top_k,'score_threshold':score_threshold,'score_Temperature':score_Temperature,'kb_name':kb_name}
    db.session.commit()
    return jsonify({'code':1,'msg':'成功','data':data})


@admin_view.route('/admin_model/save_config',methods=['POST'])
def save_config():
    top_k = request.args.get('top_k', type=int)
    score_threshold =  request.args.get('default_score_threshold', type=float)
    score_Temperature = request.args.get('default_score_Temperature', type=float)
    kb_name = request.args.get('kb_name')
    config1 = LLMConfigModel.query.filter(LLMConfigModel.key=='top_k').first()
    config2 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_threshold').first()
    config3 = LLMConfigModel.query.filter(LLMConfigModel.key=='score_Temperature').first()
    config4 = LLMConfigModel.query.filter(LLMConfigModel.key=='kb_name').first()
    config1.value = top_k
    config2.value = score_threshold
    config3.value = score_Temperature
    config4.value = kb_name
    
    db.session.commit()
    return jsonify({'code':1,'msg':'成功'})