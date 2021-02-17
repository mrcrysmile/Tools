# %%
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import os
import urllib.request as request
import socket
import re
import json
from chardet import detect


# read data from txt and parse row data
def read_txt(path, parse_func):
    all_word = []
    encode = ''
    # with open(path, 'rb') as f:
    #     line = f.read()
    #     print("get encode...")
    #     encode = detect(line)['encoding']
    # print('got encode.')
    with open(path, 'r', encoding='utf-8') as f: #'GB18030'
        line = f.readline()
        while line:
            all_word.append(parse_func(line, f))
            # print(line)
            line = f.readline()

    f.close()
    return all_word


# parse huoqingqing data str
def parse(in_str, f):
    res = []
    t1 = in_str.split(' INFO ')
    res.append(t1[0])

    t2 = t1[1].split(',"userAgent":')
    for i in t2[0].replace('"', '').split('line:756 {')[1].split(","):
        if ":" in i:
            splt_i = i.split(":")
            if len(splt_i) > 1:
                res.append(":".join(splt_i[1:]))
            else:
                res.append(i.split(":")[1])
    t3 = t2[1].split(',"deviceId')
    res.append(t3[0])

    t4 = t3[1].split('modelData":')
    for i in t4[0].replace('"', '').split(","):
        if ":" in i:
            splt_i = i.split(":")
            if len(splt_i) > 1:
                res.append(":".join(splt_i[1:]))
            else:
                res.append(i.split(":")[1])

    t5 = t4[1].split(',"origin')
    res.append(t5[0])
    for i in t5[1].replace('"', '').split('}')[0].split(","):
        if ":" in i:
            splt_i = i.split(":")
            if len(splt_i) > 1:
                res.append(":".join(splt_i[1:]))
            else:
                res.append(i.split(":")[1])

    return res


#
def parseJson(data, f):
    return list(json.loads(data).values())


#
def parse_res_data(data, f):
    return data.split('\t')


# 解析评论数据
def parse_comment(data, f):
    ret = []
    ds = data.split(' INFO ')
    ret.append(ds[0].replace(',', '.'))
    ret.append(ds[1].replace('\n', ''))
    l = f.readline()
    if l:
        ret.append(l.replace('\n', ''))
    return ret


# 解析数字数据文本
def parse_num_data(data, f):
    ret = []
    ds = data.split(' INFO ')
    ret.append(ds[0].replace(',', '.'))
    partt = re.compile('[\d.]*')
    ss = partt.findall(ds[1])
    ss = list(filter(None, ss))
    ret.append(ss[0])
    ret.append(str(int(float(ss[1]) * 10000)))
    ret.append(str(int(float(ss[2]) * 10000)))
    return ret


# write data
def write_txt(string_set, path, title=''):
    output = open(path, 'w', encoding='utf-8')
    if not title == '':
        output.writelines('\t'.join(title))
        output.writelines('\n')
    for strings in string_set:
        output.writelines('\t'.join(strings))
        output.writelines('\n')


#
def process_ori_data():
    headers = ['time', 'unionId', 'userName', 'servletPath', 'methodName', 'dataId', 'sessionId', 'userAgent', \
    'deviceId', 'channel', 'remarks', 'ip', 'modelData', 'origin', 'referer', 'crtTime']
    
    ds = read_txt(r'C:\Users\Administrator\Desktop\data.txt', parse)
    
    # k_set = set()
    # for i in ds:
    #     k_set.add(i[4])

    # print(k_set)

    write_txt(ds, r'C:\Users\Administrator\Desktop\data_split.txt', headers)


# download pics in data
def downloadPics(urls):
    save_path = r'C:\Users\Administrator\Desktop\test2'

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    headers = ('User-Agent', user_agent)
    opener = request.build_opener()
    opener.addheaders = [headers]
    request.install_opener(opener)
    
    # 设定一下无响应时间，防止有的坏图片长时间没办法下载下来
    timeout = 20
    socket.setdefaulttimeout(timeout)
    
    # 通过urllibs的requests获取所有的图片
    count = 1
    bad_url = []
    for url in urls:
        url.rstrip('\n')
        print(url)
        try:
            pic = request.urlretrieve(url, save_path + '/%d.jpg' % count)
            print('pic %d' % count)
            count += 1
        except Exception as e:
            print(Exception, ':', e)
            bad_url.append(url)
        print('\n')
    print('got all photos that can be got')

    # 把没有抓取到的urls保存起来
    with open('bad_url3.data', 'w') as f:
        for i in bad_url:
            f.write(i)
            f.write('\n')
        print('saved bad urls')
        

# statistic data distribution
# download pics for compute similarity
def statData():
    pic_count = 0
    pic_item_count = 0
    video_count = 0
    video_item_count = 0
    base_path = ''
    down_list = []
    pic_pattern = re.compile('fileId:[^,]*', re.I)
    video_pattern = re.compile('videoUrl:[^,]*', re.I)
    video_header = 'https://image.huoqingqing.com/'
    pic_header = 'https://image.huoqingqing.com/'

    s = read_txt(r'C:\Users\Administrator\Desktop\data_split.txt', parse_res_data)
    for i in s:
        if i[4] == '货清清新增发布商品':
            mStr = i[-4].replace('"', '').replace('\\', '')
            # pic
            picMchRes = pic_pattern.findall(mStr)
            pic_count += len(picMchRes)
            if not len(picMchRes) == 0:
                pic_item_count += 1
            for k in picMchRes:
                down_list.append(pic_header + k.replace('fileId:', ''))
            
            # video
            videoMchRes = video_pattern.findall(mStr)
            hasVideo = False
            for k in videoMchRes:
                if not 'null' in k:
                    video_count += 1
                    print(k)
                    hasVideo = True
            if hasVideo:
                video_item_count += 1

    # download pics
    downloadPics(down_list)    

    print('total counts:' + str(pic_count + video_count), ', total counts2:' + str(pic_item_count + video_item_count))
    print('pic counts:' + str(pic_count) + ', rate:' + str(pic_count / (pic_count + video_count)))
    print('video counts:' + str(video_count) + ', rate:' + str(video_count / (pic_count + video_count)))
    print('pic item counts:' + str(pic_item_count) + ', rate:' + str(pic_item_count / (pic_item_count + video_item_count)))
    print('video item counts:' + str(video_item_count) + ', rate:' + str(video_item_count / (pic_item_count + video_item_count)))


# %%
if __name__ == "__main__":
    process_ori_data()
    # statData()


# %%
# read_txt(r'C:\Users\Administrator\Desktop\comment(1).log', parse_comment)
# read_txt(r'C:\Users\Administrator\Desktop\popularity.log', parse_num_data)
# %%
