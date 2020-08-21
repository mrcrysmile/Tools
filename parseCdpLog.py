# %%
import numpy as np
import datetime as dt
import re


# read data from cdp log and parse data
def read_txt(path):
    keyWord = ['接收到任务推送', '任务开始', '加工开始', '任务结束']
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        last_time = -1
        cache_line = ''
        while line:
            # 字符串包含任意关键词，则记录时间，并打印与上一次的时间差
            if '[INFO]' in line:
                cache_line = line
                line = f.readline()
                if any(k in line for k in keyWord):
                        time_parttern = re.compile('\d{4}-[^,]*')
                        cur_time = time_parttern.findall(cache_line)[0]
                        if last_time == -1:
                            last_time = cur_time
                        else:
                            t1 = dt.datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
                            t2 = dt.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
                            print(line + str((t1 - t2).seconds))
                            last_time = cur_time
            line = f.readline()

    f.close()
    return


if __name__ == "__main__":
    read_txt(r'C:\Users\Administrator\Desktop\6739.log')
