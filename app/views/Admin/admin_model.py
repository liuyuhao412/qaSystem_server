from . import admin_view,to_json,paginate
from app.views.Api import get_kb_list,create_knowledge,delete_knowledge,get_list_files,delete_docs
from flask import request,jsonify


@admin_view.route('/admin_model/get_kb_list',methods=['POST'])
def kb_list():
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    data_list,count = get_kb_list()
    data_list = to_json(data_list)
    data_list = paginate(data_list,page,limit)
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data_list})


@admin_view.route('/admin_model/add_kb',methods=['POST'])
def add_kb():
    name = request.args.get('kb_name', type=str)
    if name  == None:
        return jsonify({'code':'0', 'msg': '请先输入知识库名'})
    else:
        code,msg = create_knowledge(name)
        return jsonify({'code':code,'msg':msg})
    

@admin_view.route('/admin_model/delete_kb',methods=['POST'])
def del_kb():
    name = request.args.get('kb_name', type=str)
    code,msg = delete_knowledge(name)
    return jsonify({'code':code,'msg':msg})


@admin_view.route('/admin_model/select_kb_list',methods=['POST'])
def select_kb_list():
    data_list,count = get_kb_list()
    data_list = to_json(data_list)
    return jsonify({'code':1,'msg':'请求成功','count':count,'data':data_list})


@admin_view.route('/admin_model/get_file_list',methods=['POST'])
def get_file_list():
    name = request.args.get('kb_name', type=str)
    page = request.args.get('page', type=int)
    limit =  request.args.get('limit', type=int)
    if name  == None:
        return jsonify({'code':'0', 'msg': '请先选择知识库'})
    else:
        code,msg,data_list,count = get_list_files(name)

        data_list = to_json(data_list)
        data_list = paginate(data_list,page,limit)
        
        return jsonify({'code':code,'msg':msg,'count':count,'data':data_list})
    

@admin_view.route('/admin_model/delete_doc',methods=['POST'])
def del_doc():
    kb_name = request.args.get('kb_name', type=str)
    filename = request.args.get('filename', type=str)
    code,msg = delete_docs(kb_name,filename)
    return jsonify({'code':code,'msg':msg})