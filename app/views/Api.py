import requests
base_url = "http://172.17.0.42:7861"
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
    response = requests.get("http://172.17.0.42:7861/knowledge_base/list_files?knowledge_base_name="+name,headers={"Content-Type":"application/json"})
    json_response = response.json()
    msg = json_response['msg']
    code = json_response['code']
    data = json_response['data']
    count = len(json_response['data'])
    if code == 200:
        msg = '查询 {name} 向量库成功'.format(name=name)
    return code,msg,data,count

def delete_docs(name,file):
    response = requests.post("http://172.17.0.42:7861/knowledge_base/delete_docs",json={
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



# #上传文件到知识库并进行向量化
# #@file_list  上传的文件(单文件，多文件) 文件列表list
# #@name  知识库名称  str
# #@override 覆盖已有文件  boolean
# #@to_vector_store 上传文件后是否进行向量化  boolean
# #@chunk_size  知识库中单段文本最大长度  int
# #@chunk_overlap 相邻文本重合长度  int
# #@zh_title_enhance  是否开启中文标题加强  boolean
# #@docs  自定义的docs，需要转为json字符串  str
# #@not_refresh_vs_cache  暂不保存向量库（用于FAISS）  boolean
# #@
# def upload_docs(file_list,name,override=False,to_vector_store=True,chunk_size=250,chunk_overlap=50,zh_title_enhance=False,docs='',not_refresh_vs_cache=False):
#     response = requests.post("http://172.17.0.42:7861/knowledge_base/upload_docs",files=file_list,data={
#         "knowledge_base_name":name,
#         "override":override,
#         "to_vector_store":to_vector_store,
#         "chunk_size":chunk_size,
#         "chunk_overlap":chunk_overlap,
#         "zh_title_enhance":zh_title_enhance,
#         "docs":docs,
#         "not_refresh_vs_cache":not_refresh_vs_cache
#     })
#     json_response = response.json()
#     print(json_response)

# # upload_docs(file_list={'files':open('test1.txt','r')},name="test")



# # delete_docs('test',["test1.txt"])
    
# def update_info(name,description):
#     response = requests.post("http://172.17.0.42:7861/knowledge_base/update_info",json={
#     "knowledge_base_name": name,
#     "kb_info": description
#     },headers={"Content-Type":"application/json"})
#     json_response = response.json()
#     print(json_response,'')

# # update_info("test","这是一个知识库")


# def chat(question,name):
#     response = requests.post("http://172.17.0.42:7861/chat/knowledge_base_chat", json={
#         "query": question,
#         "knowledge_base_name":name,
#         "top_k": 3,
#         "score_threshold": 1,
#         "history":[],
#         "stream": False,
#         "model_name": "chatglm3-6b",
#         "temperature": 0.7,
#         "max_tokens": 0,
#         "prompt_name": "default"
#         },headers={"Content-Type":"application/json;charset=utf-8"})
#     json_response = response.json()['answer']
#     print(json_response)
    


# # chat("你好","test")


