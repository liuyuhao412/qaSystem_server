import requests
import json
base_url = "http://172.17.0.110:7861"
top_k = 3
score_threshold = 1.0
temperature = 0.7

'''
获取知识库列表
'''
def get_kb_list():
    response = requests.get(base_url + "/knowledge_base/list_knowledge_bases",headers={"Content-Type":"application/json"})
    json_response = response.json()
    return json_response['data'],len(json_response['data'])
'''
创建知识库
@name 知识库的名称  str
'''
def create_knowledge(name):
    response = requests.post(base_url + "/knowledge_base/create_knowledge_base", json={
        "knowledge_base_name":name,
        "vector_store_type": "faiss",
        "embed_model": "m3e-base"
    },headers={"Content-Type":"application/json"})
    json_response = response.json()
    msg = json_response['msg']
    code = json_response['code']
    return code,msg
'''
删除知识库
@name  知识库的名称  str
'''
def delete_knowledge(name):
    response = requests.post(base_url+"/knowledge_base/delete_knowledge_base",json=name,headers={"Content-Type":"application/json"})
    json_response = response.json()
    print(json_response)
    msg = json_response['msg']
    code = json_response['code']
    return code,msg
'''
获取知识库里的文件列表
@name  知识库的名称  str
'''
def get_list_files(name):
    response = requests.get(base_url + "/knowledge_base/list_files?knowledge_base_name="+name,headers={"Content-Type":"application/json"})
    json_response = response.json()
    msg = json_response['msg']
    code = json_response['code']
    data = json_response['data']
    count = len(json_response['data'])
    if code == 200:
        msg = '查询 {name} 向量库成功'.format(name=name)
    return code,msg,data,count
'''
获取知识库里的文件列表
@name  知识库的名称  str
@file  文件名称  str
'''
def delete_docs(name,file):
    response = requests.post(base_url + "/knowledge_base/delete_docs",json={
    "knowledge_base_name": name,
    "file_names": [file],
    "delete_content": False,
    "not_refresh_vs_cache": False
    },headers={"Content-Type":"application/json"})
    json_response = response.json()
    msg = json_response['msg']
    code = json_response['code']
    if code == 200:
        msg = '删除 {name} 向量库中的 {file} 成功'.format(name=name,file=file)
    return code,msg
'''
上传文件到知识库并进行向量化
@file_list  上传的文件(单文件，多文件) 文件列表list
@name  知识库名称  str
@chunk_size  知识库中单段文本最大长度  int
@chunk_overlap 相邻文本重合长度  int
@zh_title_enhance  是否开启中文标题加强  boolean
'''
def upload_docs(file_list,name,chunk_size=250,chunk_overlap=50,zh_title_enhance=False):
    response = requests.post(base_url + "/knowledge_base/upload_docs",files=file_list,data={
        "knowledge_base_name":name,
        "override":False,
        "to_vector_store":True,
        "chunk_size":chunk_size,
        "chunk_overlap":chunk_overlap,
        "zh_title_enhance":zh_title_enhance,
        "docs":'',
        "not_refresh_vs_cache":False
    })
    json_response = response.json()
    msg = json_response['msg']
    return msg
'''
知识库问答
@question  问题 str
@name  知识库名称  str
@top_k 匹配知识条数 int
@score_threshold   知识匹配分数阈值 float
@temperature  float
@history    []list
'''
def chat(question,name='Olympics',top_k=top_k,score_threshold=score_threshold,temperature=temperature,history=[]):
    response = requests.post( base_url + "/chat/knowledge_base_chat", json={
        "query": question,
        "knowledge_base_name":name,
        "top_k": top_k,
        "score_threshold": score_threshold,
        "history":history,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": temperature,
        "max_tokens": 0,
        "prompt_name": "default"
        },headers={"Content-Type":"application/json;charset=utf-8"})
    json_response = response.text.split("data: ")[1]
    json_response = json.loads(json_response)
    answer = json_response['answer']
    return answer

'''
聊天
@question  问题 str
@temperature  float
@history    []list
'''
def GPT(question,temperature=temperature,history=[]):
    response = requests.post( base_url + "/chat/chat", json={
        "query": question,
        "conversation_id": "",
        "history_len": -1,
        "score_threshold": score_threshold,
        "history":history,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": temperature,
        "max_tokens": 0,
        "prompt_name": "default"
        },headers={"Content-Type":"application/json;charset=utf-8"})
    print(response.text)
    json_response = response.text.split("data: ")[1]
    json_response = json.loads(json_response)
    answer = json_response['text']
    return answer

 