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
    response = requests.post("http://172.17.0.42:7861/knowledge_base/delete_knowledge_base",json=name,headers={"Content-Type":"application/json"})
    json_response = response.json()
    print(json_response)
    msg = json_response['msg']
    code = json_response['code']
    return code,msg

