# %%
# verify user_id_sn
import numpy as np

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
with open(r'C:/Users/Administrator/Desktop/item.log', 'r', encoding='unicode_escape') as f:
    line = f.readline()
    while line:
        splitdata = line.split('[')
        if len(splitdata) >= 2:
            # print(line)
            userId = splitdata[1].split(',')[0].replace('"', '')
            user_id.append(userId)
        line = f.readline()

f.close()
print("data rows:")
print(len(user_id))
print("item ids:")
print(len(set(user_id)))

# %%
