from . import admin_view
from flask import request, jsonify
from app.views.Api import upload_docs

import platform
if platform.system() == "Windows":
    splash = '\\'
elif platform.system() == "Linux":
    splash = '/'


UPLOAD_PATH = 'app'+ splash + 'uploads' + splash 


@admin_view.route('/admin_model/upload_file',methods=['post'])
def upload_file():
    for key, file in request.files.items():
        file_name = file.filename
        file_path = UPLOAD_PATH + file_name
        file.save(file_path)
    return jsonify({"code":1,"msg":"上传成功","file":file_name})

@admin_view.route('/admin_model/upload_form',methods=['post'])
def upload_form():
    kb_name = request.args.get('kb_name')
    file = request.args.get('file')
    chunk_size_max_length = request.args.get('chunk_size_max_length')
    chunk_overlap_length = request.args.get('chunk_overlap_length')
    zh_title_enhance = request.args.get('zh_title_enhance')
    if kb_name == '':
        return jsonify({'code':0,'msg':'请先选择知识库'})
    file = {'files':open(UPLOAD_PATH + file,'rb') }
    msg = upload_docs(file,kb_name,chunk_size_max_length,chunk_overlap_length,zh_title_enhance)

    return jsonify({'code':1,'msg':msg})