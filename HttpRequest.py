# %%
# -*- coding:utf-8 -*-
import requests
import urllib
import time
import jpype
import json
import numpy as np
import ParseJson as pj
import os


# 每批次发送的数据条数
batchSize = 50


#
def write_txt(data, path):
    output = open(path, 'w', encoding='utf-8')
    for strings in data:
        output.writelines(''.join(strings))
        output.writelines('\n')


# trans list[list[]] data 2 json
def data2json(data, key):
    str_json = ''
    for lst in data:
        list_json = dict(zip(key, lst))
        str_json += json.dumps(list_json, indent=2, ensure_ascii=False)
    return str_json


# post data to cdp
def httpPost(apiKey, signature, data, timestamp, url='http://reception.idata.zhiziyun.com/dataReceive', headers={"Content-Type": "application/json;charset=utf-8"}):
    param = {'apiKey': apiKey, 'signature': str(signature), 'data': data, 'timestamp': timestamp}
    # print(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    js_data = json.dumps(param, ensure_ascii=False).encode('utf-8')
    response = requests.post(url, data=js_data, headers=headers)
    # print(response.status_code)
    if '200' not in response.text:
        print('one piece of data send failed...')
        print(response.text)
        write_txt([signature, response.text, data], r'C:\Users\Administrator\Desktop\bad_data.txt')


#
def data2cdp(apiKey, encryptKey, path, func=pj.parseJson):
    # 获取jar包
    jarpath = os.path.join(os.path.abspath("."), r"D:\wuziyang\wuziyang\projects\pypros\Tools\HMACSHA1.jar")    
    
    # 获取jvm.dll 的文件路径
    jvmPath = jpype.getDefaultJVMPath()  
   
    # # 开启jvm
    jpype.startJVM(jvmPath,"-ea", "-Djava.class.path=%s" % (jarpath)) 
    
    # 加载java类（参数是java的长类名）
    javaClass = jpype.JClass("pkg.HMACSHA1")    
    
    # 实例化java对象
    javaInstance = javaClass()
    
    print('start post...')
    # post data
    # read ori data
    data = pj.read_txt(path, func)
    batch = np.ceil(len(data) / batchSize)
    st_idx = 0
    ed_idx = 0
    post_num = 0
    for _ in range(int(batch)):
        print('now post ' + str(post_num))
        # get signature
        ed_idx = min(50, len(data))
        post_num += ed_idx
        assert(ed_idx > st_idx)
        cur_batch_data = data[st_idx: ed_idx]
        data = data[ed_idx:]
        timestamp = str(int(round(time.time() * 1000)))
        data_json = json.dumps(cur_batch_data, ensure_ascii=False)
        # 计算signature
        signature = javaClass.HmacSHA1Hex(data_json + timestamp, encryptKey)
        # st_idx = ed_idx

        # post data to cdp
        httpPost(apiKey, signature, data_json, timestamp)
    
    # 关闭jvm
    jpype.shutdownJVM()


# %%
if __name__ == "__main__":
    # pj.read_txt(r'C:\Users\Administrator\Desktop\popularity.log', pj.parse_num_data)
    # pj.read_txt(r'C:\Users\Administrator\Desktop\comment.log', pj.parse_comment)
    data2cdp('1574bddb75c78a6fd2251d61e2993b5146201319', 'c8306ae139ac98f432932286151dc0ec55580eca', r'D:\wuziyang\wuziyang\货清清\货清清数据\data_split.txt', pj.parse_res_data)

# %%
import requests
import json
import time
headers={"Content-Type": "application/json;charset=utf-8"}
url='http://rec.idata.zhiziyun.com/rec'
apiKey = 'i am an apikey'
user_id = 15346948
item_id = 16873
scenario = 'zfwe'
context_info = {'se0': 124}
count = -50000
with_score = 'afc'
param = {}#'apiKey': apiKey,
        #'user_id': str(user_id), 
        # 'item_id': str(item_id), 
        # 'scenario': scenario, 
        # 'context_info': context_info, 
        # 'count': str(count)}
        # 'with_score': with_score}
# print(json.dumps(data, ensure_ascii=False).encode('utf-8'))
js_data = json.dumps(param, ensure_ascii=False).encode('utf-8')
st = time.time()
for i in range(0, 10):
    response = requests.post(url, data=js_data, headers=headers)
print('rec time: ' + str((time.time() - st) / 10))
# print(response.status_code)
s = json.loads(response.text)
a = s['count']
b = s['rec_list']
c = s['rec_id']
print("count: " + str(a))
print('rec_list len: ' + str(len(b)))
print('rec_list example: ' + str(b[0]))
print('rec_id: ' + str(c))


# %%
