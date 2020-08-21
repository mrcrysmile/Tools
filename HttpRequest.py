# %%
# -*- coding:utf-8 -*-
import requests
import urllib
import time
import jpype
import json
import numpy as np
import ParseJson as pj


# 每批次发送的数据条数
batchSize = 50


# trans list[list[]] data 2 json
def data2json(data, key):
    str_json = ''
    for lst in data:
        list_json = dict(zip(key, lst))
        str_json += json.dumps(list_json, indent=2, ensure_ascii=False)
    return str_json


# post data to cdp
def httpPost(apiKey, signature, data, timestamp):
    param = {'apiKey': apiKey, 'signature': str(signature), 'data': data, 'timestamp': timestamp}
    # print(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    headers = {"Content-Type": "application/json;charset=utf-8"}
    js_data = json.dumps(param, ensure_ascii=False).encode('utf-8')
    response = requests.post("http://reception.idata.zhiziyun.com/dataReceive", \
        data=js_data, headers=headers)
    # print(response.status_code)
    if '200' not in response.text:
        print('one piece of data send failed...')
        pj.write_txt([signature, data], r'C:\Users\Administrator\Desktop\bad_data.txt')


#
def data2cdp(path, apiKey, encryptKey):    
    # 获取jar包
    jarpath = os.path.join(os.path.abspath("."), r"D:\wuziyang\wuziyang\projects\pypros\Tools\HMACSHA1.jar")    
    
    # 获取jvm.dll 的文件路径
    jvmPath = jpype.getDefaultJVMPath()  
   
    # 开启jvm
    jpype.startJVM(jvmPath,"-ea", "-Djava.class.path=%s" % (jarpath)) 
    
    # 加载java类（参数是java的长类名）
    javaClass = jpype.JClass("pkg.HMACSHA1")    
    
    # 实例化java对象
    javaInstance = javaClass()
    
    # post data
    # read ori data
    data = pj.read_txt(path, pj.parseJson)
    batch = np.ceil(len(data) / batchSize)
    st_idx = 0
    ed_idx = 0
    for _ in range(int(batch)):
        # get signature
        ed_idx = min(ed_idx + batchSize, len(data))
        assert(ed_idx > st_idx)
        cur_batch_data = data[st_idx: ed_idx]
        timestamp = str(int(round(time.time() * 1000)))
        data_json = json.dumps(cur_batch_data, ensure_ascii=False)
        # print(data_json)
        # 调用java方法，由于写的是静态方法，直接使用类名就可以调用方法
        # 计算signature
        signature = javaClass.HmacSHA1Hex(data_json + timestamp, encryptKey)
        st_idx = ed_idx

        # post data to cdp
        httpPost(apiKey, signature, data_json, timestamp)
    
    # 关闭jvm
    jpype.shutdownJVM()


# %%
if __name__ == "__main__":
    data2cdp(r'C:\Users\Administrator\Desktop\用戶信息.txt', '0716d9708d321ffb6a00818614779e779925365c', '934385f53d1bd0c1b8493e44d0dfd4c8e88a04bb')

# %%
path = r'C:\Users\Administrator\Desktop\新建文本文档.txt'
all_word = ''
with open(path, 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        all_word += line
        line = f.readline()
f.close()

s = json.loads(all_word)
print(s)
# %%
