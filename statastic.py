# %%
import numpy as np
import chardet

ss = dict()
with open(r'C:\Users\Administrator\Desktop\1937.log', 'r', encoding='UTF-8') as f:
    line = f.readline()
    while line:
        ls = line.replace('"', '').replace(']', '').split('[')[1].split(',')
        if ls[0] in ss:
            if ls[1] != ss[ls[0]]:
                if ls[1] > '2020-11-00':
                    print(ls)
        ss.update({ls[0]: ls[1]})
        line = f.readline()


# %%
# 重复recid专用
import numpy as np
import chardet

v1set = dict()
v2set = dict()

c = 0
with open(r'C:\Users\Administrator\Desktop\1729.log', 'r', encoding='UTF-8') as f:
    line = f.readline()
    while line:
        lss = line.split(',')[0].split('[')[1].replace('"', '')
        ls = lss.split("_")
        c += 1
        if ls[2] == '3':
            if lss in v1set:
                v1set[lss] += 1
            else:
                v1set.update({lss: 1})
        elif ls[2] == '5':
            if lss in v2set:
                v2set[lss] += 1
            else:
                v2set.update({lss: 1})
        else:
            print("error: not 3 and 5")
        line = f.readline()

v1_dup = 0
v1_all = 0
v2_dup = 0
v2_all = 0
for k,v in v1set.items():
    v1_all += v
    if v != 1:
        v1_dup += v
for k,v in v2set.items():
    v2_all += v
    if v != 1:
        v2_dup += v

print("all %d" %c)

print("v1 all %d" % v1_all)
print("v1 recid %d" % len(v1set))
print("v1 dup rate %f" % (v1_dup / v1_all))

print("v2 all %d" % v2_all)
print("v2 recid %d" % len(v2set))
print("v2 dup rate %f" % (v2_dup / v2_all))

# %%

# %%
