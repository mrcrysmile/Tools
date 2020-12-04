# %%
# verify user_id_sn
import numpy as np
from numpy.core.defchararray import array, upper
from numpy.lib.function_base import _update_dim_sizes

user_id = []
with open(r'C:\Users\Administrator\Desktop\user.log', 'r', encoding='unicode_escape') as f:
    line = f.readline()
    while line:
        # print(line)
        userId = line.split('[')[1].split(',')[0].replace('"', '')
        user_id.append(userId)
        line = f.readline()

f.close()
print("data rows:")
print(len(user_id))
print("user ids:")
print(len(set(user_id)))
# %%
# verify item_id_sn
import numpy as np

user_id = []
with open(r'C:\Users\Administrator\Desktop\item1.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        userId = l.split('[')[1].split(',')[0].replace('"', '')
        user_id.append(userId)
with open(r'C:\Users\Administrator\Desktop\item2.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        userId = l.split('[')[1].split(',')[0].replace('"', '')
        user_id.append(userId)
with open(r'C:\Users\Administrator\Desktop\item3.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        userId = l.split('[')[1].split(',')[0].replace('"', '')
        user_id.append(userId)
with open(r'C:\Users\Administrator\Desktop\item4.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        userId = l.split('[')[1].split(',')[0].replace('"', '')
        user_id.append(userId)

f.close()
print("data rows:")
print(len(user_id))
print("item ids:")
print(len(set(user_id)))

# %%
# verify 有效item实时更新
import numpy as np

user_id = dict()
with open(r'C:\Users\Administrator\Desktop\item1.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        row = l.split('\t[')[1].split('","')
        userId = row[0].replace('"', '')
        if userId in user_id:
            user_id[userId] = row[-5]
        else:
            user_id.update({userId: row[-5]})
with open(r'C:\Users\Administrator\Desktop\item2.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        row = l.split('\t[')[1].split('","')
        userId = row[0].replace('"', '')
        if userId in user_id:
            user_id[userId] = row[-5]
        else:
            user_id.update({userId: row[-5]})
with open(r'C:\Users\Administrator\Desktop\item3.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        row = l.split('\t[')[1].split('","')
        userId = row[0].replace('"', '')
        if userId in user_id:
            user_id[userId] = row[-5]
        else:
            user_id.update({userId: row[-5]})
with open(r'C:\Users\Administrator\Desktop\item4.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        row = l.split('\t[')[1].split('","')
        userId = row[0].replace('"', '')
        if userId in user_id:
            user_id[userId] = row[-5]
        else:
            user_id.update({userId: row[-5]})

filtItem = [k for k,v in user_id.items() if v == '5']
output = open(r'C:\Users\Administrator\Desktop\ava_item.txt', 'w', encoding='utf-8')
for string in filtItem:
    output.writelines(string)
    output.writelines('\n')

# %%
import time
s = set()
b = set()
x = dict()
with open(r'C:\Users\Administrator\Desktop\session.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        q = l.replace('\n', '').split('\t')
        t = time.mktime(time.strptime(q[-1].replace('\t', '').split('.')[0], "%Y-%m-%d %H:%M:%S"))
        if q[2] in x:
            if x[q[2]][0] > t:
                x[q[2]][0] = t
            if x[q[2]][1] < t:
                x[q[2]][1] = t
        else:
            x.update({q[2]: [t, t]})

y = dict()
for i in range(12):
    y.update({i: 0})

for _, v in x.items():
    d = int((v[1] - v[0]) / 86400)
    y[d] += 1

for k,v in y.items():
    print(str(k) + ',' + str(v))

import matplotlib.pyplot as plt
name = list(y.keys())
print(name)
# value = list(map(lambda x: x / 7, list(range_dict.values())))
value = list(y.values())
print(value)
plt.bar(range(len(value)), value,tick_label=name)
plt.show()

# %%
uid_user = list()
uid_oper = list()
with open(r'C:\Users\Administrator\Desktop\1631-uid.txt', 'r', encoding='unicode_escape') as f:
    lines = f.readlines()
    for l in lines:
        q = l.replace('\n', '')
        uid_user.append(q)
with open(r'C:\Users\Administrator\Desktop\1630-total-uid.txt', 'r', encoding='unicode_escape') as f:
    lines = f.readlines()
    for l in lines:
        q = l.replace('\n', '')
        if q not in uid_user:
            uid_oper.append(q)

user_uni = list()
for u in uid_user:
    if u not in uid_oper:
        user_uni.append(u)

print('user uni:' + str(len(user_uni)))
output = open(r'C:\Users\Administrator\Desktop\user-uni.txt', 'w', encoding='utf-8')
for v in user_uni:
    output.writelines(v)
    output.writelines('\n')
print('oper uni:' + str(len(uid_oper)))
output = open(r'C:\Users\Administrator\Desktop\oper-uni.txt', 'w', encoding='utf-8')
for v in uid_oper:
    output.writelines(v)
    output.writelines('\n')

# %%

import re
import numpy as np
parttern = r"\d*-\d*-\d* \d*:\d*:\d*"
range_dict = dict()
for i in range(24):
    range_dict.update({i:0})
with open(r'C:\Users\Administrator\Desktop\30.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        q = l.replace('\n', '')
        s = re.findall(parttern, q)
        ran = int(s[0].split(' ')[1].split(':')[0])
        range_dict[ran] += 1

import matplotlib.pyplot as plt
print(28)
name = list(range_dict.keys())
print(name)
# value = list(map(lambda x: x / 7, list(range_dict.values())))
value = list(range_dict.values())
print(value)
plt.bar(range(len(value)), value,tick_label=name)
plt.show()

# %%
import numpy as np
import matplotlib.pyplot as plt
q = dict()
with open(r'C:\Users\Administrator\Desktop\1729.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        u = l.split('[')[1].replace('"', '').split(',')[3]
        if u in q:
            q[u] += 1
        else:
            q.update({u: 1})

v = list(q.values())
print("user num:" + str(len(list(q.keys()))))
print("max:" + str(max(v)))
print("min:" + str(min(v)))
print("aver:" + str(sum(v) / len(list(q.keys()))))
# h, b = np.histogram(np.array(v))
# plt.hist(v, bins=[1,5,10,20,30,40,50,100,400])
plt.rcParams['font.sans-serif']=['SimHei'] 
z = np.array([  "[1,5)",   "[5,10)",  "[10,20)",  "[20,30)",  "[30,40)",  "[40,50)",  "[50,100)", "大于100"])
f = np.array([403., 122., 105.,  44.,  21.,  12.,  17.,  18.])
plt.bar(z, f)
plt.show()
# %%
import matplotlib.pyplot as plt
basep = r'E:\货清清data\als'
q = np.array([])
for i in range(1, 11):
    p = basep + i + '.log'
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            u = l.split(',')
            q.append(u)

w = np.sort(q)
c = len(w)
p = int(c / 100)
x = []
for i in range(100):
    pc = p * i
    x.append(w[pc])
y = range(100)
plt.scatter
plt.tick_params(axis='both',labelsize=14)

# %%
import numpy as np
w = np.array([12,523,4,23])
q = np.arange(10)
q
# %%
