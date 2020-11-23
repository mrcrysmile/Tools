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
    data2cdp('472b07b9fcf2c2451e8781e944bf5f77cd8457c8', '934385f53d1bd0c1b8493e44d0dfd4c8e88a04bb', r'D:\wuziyang\wuziyang\货清清\货清清数据\testData.txt', pj.parse_res_data)

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
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei']
plt.figure(figsize=(24, 8))
plt.xlabel('rating范围(1e-5)')
plt.ylabel('rating数量占比(%)')
values = [15999, 120335172, 139685423, 58133, 11580, 3556, 3415, 1206, 4250]
values = [15623, 118882363, 139793853, 978010, 238079, 86760, 42663, 58166, 11026, 3452, 3137, 1223, 3175]
values = [45.68,
17.65,
4.10,
2.69,
2.01,
1.62,
1.36,
1.19,
1.06,
0.93,
0.84,
5.48,
3.04,
12.36
]

bins = [-1, -0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 3]
ranges = ["(-1, -0.05)", "(-0.05, 0)", "(0, 0.05)", "(0.05, 0.1)", 
"(0.1, 0.15)", "(0.15, 0.2)", "(0.2，0.4)", "(0.4, 0.6)", "(0.6, 3)"]
ranges = ["(-1, -0.05)", "(-0.05, 0)", "(0, 0.01)", "(0.01, 0.02)", "(0.02, 0.03)", 
"(0.03, 0.04)", "(0.04, 0.05)", "(0.05, 0.1)", "(0.1, 0.15)",
 "(0.15, 0.2)", "(0.2，0.4)", "(0.4, 0.6)", "(0.6, 3)"]
ranges = ["小于0", "(0, 1)", "(1, 2)", "(2, 3)", 
"(3, 4)", "(4, 5)", "(5, 6)", "(6, 7)",
 "(7, 8)", "(8，9)", "(9, 10)", "(10, 20)", "(20, 30)", "大于30"]



rects = plt.bar(ranges, values)
for rect in rects:
  height = rect.get_height()
  plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % height)

# plt.savefig('C:\Users\Administrator\Desktop\hist.jpg')
plt.show()

# %%
