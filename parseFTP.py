# %%
import numpy as np
import time
import json


# 
def parse(path):
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line:
            temp_str = line
            line = f.readline()
            temp_str += line
            # 处理json
            temp_arr = []
            temp_str = temp_str.replace('\n', '')
            t = temp_str.split('\"{\"')
            temp_arr += t[0].split(',')
            for i in range(1, len(t)):
                tt = t[i].split('\"}\"')
                temp_arr.append(tt[0])
                temp_arr += tt[1].split(',')

            res.append(temp_arr)

            line = f.readline()
        f.close()
    return res


# 0:是否支持交易,1:unionId,2:货品分类,3:货品档次,4:发布时间,5:平台担保交易
# 6:货品编号,7:货品状态
# 8:归属的客户编号
# 9:信息描述
# 10:照片/视频
# 11:是否推荐
# 12:最近更新时间 
def parse1(path):
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line:
            temp_str = line.replace('\n', '')
            line = f.readline()
            while line[0:2] != '0,' and line:
                temp_str += " " + line.replace('\n', '')
                line = f.readline()

            res.append(temp_str.split(','))

        f.close()
    return res


# 读有id货品
def get_product():
    res = []
    with open(r'C:\Users\Administrator\Desktop\1.txt', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            temp_str = line.replace('\n', '')
            line = f.readline()
            while line[0:2] != '0,' and line:
                temp_str += " " + line.replace('\n', '')
                line = f.readline()

            t = temp_str.split(',')
            if t[1] != '':
                res.append(t)

        f.close()

    with open(r'C:\Users\Administrator\Desktop\带unionId数据', 'w', encoding='utf-8') as f:
        for v in res:
            f.write(';'.join(v))
            f.write('\n')
        f.close()


def seperate_product():
    # s = parse1(r'C:\Users\Administrator\Desktop\tet')
    s = parse1(r'C:\Users\Administrator\Desktop\货品数据')
    print("read ok...")
    # with open(r'C:\Users\Administrator\Desktop\货品数据_整理', 'w', encoding='utf-8') as f:
    #     for i in s:
    #         f.write(';'.join(i))
    #         f.write('\n')
    #     f.close()

    product_id_set = set()
    single_product_id_data = dict()
    earliest_time = time.strptime('2020-9-23 00:00:00','%Y-%m-%d %H:%M:%S')
    latest_time = time.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
    # 按货品id过滤数据
    for row in s:
        product_id = row[6]
        user_id = row[8]
        info = row[9]
        link = ','.join(row[10: -2])
        up_time = row[-1]
        if up_time != '':
            # 同id保留最新数据
            if product_id in product_id_set:
                p_data = single_product_id_data[product_id]
                old_time = time.strptime(p_data[4].split('.')[0],'%Y-%m-%d %H:%M:%S')
                cur_time = time.strptime(up_time.split('.')[0],'%Y-%m-%d %H:%M:%S')
                # if cur_time > latest_time:
                #     latest_time = cur_time
                # elif cur_time < earliest_time:
                #     earliest_time = cur_time

                if old_time < cur_time:
                    single_product_id_data.update({product_id: [product_id, user_id, info, link, up_time]})
            else:
                single_product_id_data.update({product_id: [product_id, user_id, info, link, up_time]})

    # with open(r'C:\Users\Administrator\Desktop\productid去重数据', 'w', encoding='utf-8') as f:
    #     for k,v in single_product_id_data.items():
    #         f.write(';'.join(v))
    #         f.write('\n')
    #     f.close()

    print("去重productid后货品数：" + str(len(single_product_id_data)))

    # 记录描述
    info_set = set()
    # 记录重复数据,以描述为key
    info_dict = dict()
    for _, row in single_product_id_data.items():
        product_id = row[0]
        user_id = row[1]
        info = row[2]
        link = row[3]
        up_time = row[4]

        if info in info_set:
            t = info_dict[info]
            # old_time = time.strptime(t[4].split('.')[0],'%Y-%m-%d %H:%M:%S')
            # cur_time = time.strptime(up_time.split('.')[0],'%Y-%m-%d %H:%M:%S')
            # if old_time < cur_time:
            #     info_dict.update({info: [product_id, user_id, info, link, up_time]})
            # t.append('product_id:' + str(product_id) \
            #     + ';'  + 'user_id:' + str(user_id) + ';' + 'link:' + str(link) + ';' + \
            #         'update time:' + str(up_time))
            t.append([product_id, user_id, info, link, up_time])
            info_dict.update({info: t})
        else:
            info_set.add(info)
            info_dict.update({info: [[product_id, user_id, info, link, up_time]]})
            # info_dict.update({info: [('product_id:' + str(product_id) \
            #      + ';'  + 'user_id:' + str(user_id) + ';' + 'link:' + str(link) + ';' + \
            #           'update time:' + str(up_time))]})

    # with open(r'C:\Users\Administrator\Desktop\描述去重数据', 'w', encoding='utf-8') as f:
    #     for k,v in info_dict.items():
    #         f.write(k + ';' + ';'.join(v))
    #         f.write('\n')
    #     f.close()    
    # with open(r'C:\Users\Administrator\Desktop\描述重复数据', 'w', encoding='utf-8') as f:
    #     for k,v in info_dict.items():
    #         if len(v) > 1:
    #             f.write(str(len(v)) + ';' + k + ';' + ';'.join(v))
    #             f.write('\n')
    #         if len(v) > 100:
    #             print('big key:' + k + ', len:' + str(len(v)))
    #     f.close()    
    print("描述去重后货品数：" + str(len(info_dict)))

    dis_link_count = 0
    dis_link_data = []
    same_link_same_info_count = 0
    for k,v in info_dict.items():
        if len(v) > 1:
            link_set = set()
            for vv in v:
                link = vv[3].split(',')

                if len(link_set) >= 1:
                    flag = False
                    for lks in link_set:
                        link_ls = lks.split(',')
                        if len(link_ls) == len(link):
                            for l in link_ls:
                                if l in link:
                                    pass
                                else:
                                    break
                            flag = True
                            break
                        else:
                            continue
                    if flag:
                        same_link_same_info_count += 1
                    else:
                        dis_link_count += 1
                        link_set.add(vv[3])
                        dis_link_data.append(vv)
                else:
                    dis_link_count += 1
                    link_set.add(vv[3])
                    dis_link_data.append(vv)
        else:
            dis_link_count += 1
            dis_link_data.append(v[0])


    print("链接去重数据量：" + str(dis_link_count))
    print("描述相同，链接相同数据量：" + str(same_link_same_info_count))
    # with open(r'C:\Users\Administrator\Desktop\链接去重数据', 'w', encoding='utf-8') as f:
    #     for v in dis_link_data:
    #         f.write(';'.join(v))
    #         f.write('\n')
    #     f.close()

    dis_link_count2 = 0
    dis_link_data2 = []
    same_link_data = dict()
    for v in dis_link_data:
        link_set = set()
        link = v[3].split(',')

        if len(link_set) >= 1:
            flag = False
            cut_key = ''
            for lks in link_set:
                cur_key = lks
                link_ls = lks.split(',')
                if len(link_ls) == len(link):
                    for l in link_ls:
                        if l in link:
                            pass
                        else:
                            break
                    flag = True
                    break
                else:
                    continue
            if flag:
                t = same_link_data[cur_key]
                t.append(';'.join(v))
                same_link_data.update({cur_key: t})
            else:
                dis_link_count2 += 1
                link_set.add(v[3])
                dis_link_data2.append(v)
                same_link_data.update({v[3]: [';'.join(v)]})
        else:
            dis_link_count2 += 1
            link_set.add(v[3])
            dis_link_data2.append(v)

    print("全商品链接去重数据量：" + str(dis_link_count2))
    with open(r'C:\Users\Administrator\Desktop\同链接不同描述数据', 'w', encoding='utf-8') as f:
        for k,v in same_link_data.items():
            if len(v) > 1:
                f.write('#'.join(v))
                f.write('\n')
        f.close()    

    with open(r'C:\Users\Administrator\Desktop\全商品链接去重数据', 'w', encoding='utf-8') as f:
        for v in dis_link_data2:
            f.write(';'.join(v))
            f.write('\n')
        f.close()    

    res = []
    with open(r'C:\Users\Administrator\Desktop\全商品链接去重数据', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            temp_ls = line.replace('\n', '').split(';')
            res.append(temp_ls)
            line = f.readline()

        f.close()
    print('read ok')

    # 记录描述
    info_set = set()
    # 记录重复数据,以描述为key
    info_dict = dict()
    for row in res:
        product_id = row[0]
        user_id = row[1]
        info = row[2]
        link = row[3]
        up_time = row[4]

        if info in info_set:
            t = info_dict[info]
            t.append(';'.join([product_id, user_id, info, link, up_time]))
            info_dict.update({info: t})
        else:
            info_set.add(info)
            info_dict.update({info: [';'.join([product_id, user_id, info, link, up_time])]})

    with open(r'C:\Users\Administrator\Desktop\链接不同描述不同数据', 'w', encoding='utf-8') as f:
        for k,v in info_dict.items():
            if len(v) == 1:
                f.write(str(len(v)) + ';' + k + ';' + '#'.join(v))
                f.write('\n')
        f.close()
    with open(r'C:\Users\Administrator\Desktop\描述重复数据', 'w', encoding='utf-8') as f:
        for k,v in info_dict.items():
            if len(v) > 1:
                f.write(str(len(v)) + ';' + k + ';' + '#'.join(v))
                f.write('\n')
        f.close()
    print("描述去重后货品数：" + str(len(info_dict)))

#
def get_user():
    res = []
    with open(r'C:\Users\Administrator\Desktop\user.txt', 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line:
            temp_str = line.replace('\n', '')
            t = temp_str.split(',')
            if t[7] != '':
                res.append(t)
            line = f.readline()

        f.close()

    with open(r'C:\Users\Administrator\Desktop\有id用户', 'w', encoding='utf-8') as f:
        for v in res:
            f.write(';'.join(v))
            f.write('\n')
        f.close()

# 
def get_user_op_log():
    res = []
    # app_res = []
    # wechat_res = []
    # miniapp_res = []
    # bhgj_res = []
    # h5_res = []
    search_good_res = []
    search_shop_res = []
    search_detail_res = []

    methodDict = dict()
    ipSet = set()
    unionIdSet = set()
    channelDict = dict()
    dataSet = set()
    earliest_time = time.strptime('2020-9-23 00:00:00','%Y-%m-%d %H:%M:%S')
    latest_time = time.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')

    with open(r'C:\Users\Administrator\Desktop\user_op_log.txt', 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line:
            temp_str = line.replace('\n', '')
            # 处理json
            t = []
            temp_str = temp_str.replace('\n', '')
            temp_arr = temp_str.split('{')
            t += temp_arr[0].split(',')
            for i in range(1, len(temp_arr)):
                tt = temp_arr[i].split('}')
                t.append(tt[0])
                if len(tt) > 1:
                    t += tt[1].split(',')
            # methodName,
            # ip,
            # unionId,
            # channel,
            # servletPath,
            # crtTime,
            # userAgent,
            # dataId,
            # origin,
            # sessionId,
            # remarks,
            # referer,
            # userId,
            # modelData,
            # deviceId,
            # userName
            methodName = t[0]
            ip = t[1]
            unionId = t[2]
            channel = t[3]
            crtTime = t[5]
            dataId = t[7]

            # # methodName num
            # if methodName in methodDict:
            #     methodDict.update({methodName: methodDict[methodName] + 1})
            # else:
            #     methodDict.update({methodName: 1})

            # # ip, unionId, dataId
            # ipSet.add(ip)
            # unionIdSet.add(unionId)
            # dataSet.add(dataId)

            # # channel
            # if channel in channelDict:
            #     channelDict.update({channel: channelDict[channel] + 1})
            # else:
            #     channelDict.update({channel: 1})

            # # 更新时间
            # cur_time = time.strptime(crtTime.split('.')[0],'%Y-%m-%d %H:%M:%S')
            # if cur_time > latest_time:
            #     latest_time = cur_time
            # elif cur_time < earliest_time:
            #     earliest_time = cur_time

            # if channel == 'app':
            #     app_res.append(t)
            # elif channel == 'wechat':
            #     wechat_res.append(t)
            # elif channel == 'miniapp':
            #     miniapp_res.append(t)
            # elif channel == 'bhgj':
            #     bhgj_res.append(t)
            # elif channel == 'h5':
            #     h5_res.append(t)
            # else:
            #     print("error data:" + str(t))

            # if methodName == '货清清找货、商品列表':
            #     search_good_res.append(t)
            # elif methodName == '货清清找人、店铺列表':
            #     search_shop_res.append(t)
            if methodName == '浏览好货详情查询':
                search_detail_res.append(t)

            # res.append(t)
            line = f.readline()
        f.close()

    # # 输出结果
    # print("活跃用户数：" + str(len(unionIdSet)))
    # print("ip 数：" + str(len(ipSet)))
    # print("操作货品数：" + str(len(dataSet)))
    # print("各操作类型数：" + str(methodDict))
    # print("各渠道操作数：" + str(channelDict))
    # print("总操作数：" + str(len(res)))
    # print("最早操作时间：" + str(time.strptime(earliest_time,'%Y-%m-%d %H:%M:%S')))
    # print("最晚操作时间：" + str(time.strptime(latest_time,'%Y-%m-%d %H:%M:%S')))

    # for d in app_res:
    #     methodName = d[0]
    #     # methodName num
    #     if methodName in methodDict:
    #         methodDict.update({methodName: methodDict[methodName] + 1})
    #     else:
    #         methodDict.update({methodName: 1})
    # print("app渠道各操作类型数：" + str(methodDict))
    # methodDict = dict()

    # for d in wechat_res:
    #     methodName = d[0]
    #     # methodName num
    #     if methodName in methodDict:
    #         methodDict.update({methodName: methodDict[methodName] + 1})
    #     else:
    #         methodDict.update({methodName: 1})
    # print("wechat渠道各操作类型数：" + str(methodDict))
    # methodDict = dict()

    # for d in miniapp_res:
    #     methodName = d[0]
    #     # methodName num
    #     if methodName in methodDict:
    #         methodDict.update({methodName: methodDict[methodName] + 1})
    #     else:
    #         methodDict.update({methodName: 1})
    # print("miniapp渠道各操作类型数：" + str(methodDict))
    # methodDict = dict()

    # for d in bhgj_res:
    #     methodName = d[0]
    #     # methodName num
    #     if methodName in methodDict:
    #         methodDict.update({methodName: methodDict[methodName] + 1})
    #     else:
    #         methodDict.update({methodName: 1})
    # print("bhgj渠道各操作类型数：" + str(methodDict))
    # methodDict = dict()

    # for d in h5_res:
    #     methodName = d[0]
    #     # methodName num
    #     if methodName in methodDict:
    #         methodDict.update({methodName: methodDict[methodName] + 1})
    #     else:
    #         methodDict.update({methodName: 1})
    # print("h5渠道各操作类型数：" + str(methodDict))
    # methodDict = dict()

    # with open(r'C:\Users\Administrator\Desktop\找店操作日志', 'w', encoding='utf-8') as f:
    #     for v in search_shop_res:
    #             f.write('#'.join(v))
    #             f.write('\n')
    #     f.close()

    # with open(r'C:\Users\Administrator\Desktop\找货操作日志', 'w', encoding='utf-8') as f:
    #     for v in search_good_res:
    #             f.write('#'.join(v))
    #             f.write('\n')
    #     f.close()

    # topn = 0
    # print('*' * 10)
    # print("search good:")
    # modelDataDict = dict()
    # search_dict = dict()
    # user_set = set()
    # for d in search_shop_res:
    #     unionId = d[2]
    #     user_set.add(unionId)
    #     modelData = json.loads('{' + d[15] + '}')
    #     sc_str = ''
    #     if 'searchStr' in modelData:
    #         sc_str = modelData['searchStr']
    #     else:
    #         print("dity data:" + str(modelData))
    #     if sc_str != '':
    #         if sc_str in search_dict:
    #             search_dict.update({sc_str: search_dict[sc_str] + 1})
    #         else:
    #             search_dict.update({sc_str: 1})
    #     # if modelData in modelDataDict:
    #     #     modelDataDict.update({modelData: modelDataDict[modelData] + 1})
    #     # else:
    #     #     modelDataDict.update({modelData: 1})
    # # sort_res = sorted(modelDataDict, key=modelDataDict.get, reverse=True)
    # sort_res = sorted(search_dict, key=search_dict.get, reverse=True)
    # for s in sort_res:
    #     topn += 1
    #     if topn > 30:
    #         break
    #     print("key:" + s + "; num:" + str(search_dict[s]))
    # print('good res len:' + str(len(search_dict)))
    # print('dict len:' + str(len(search_dict)))

    # print('user num:' + str(len(user_set)))
    # for s in sort_res:
    #     topn += 1
    #     if topn > 30:
    #         break
    #     print("key:" + s + "; num:" + str(modelDataDict[s]))
    # print('good res len:' + str(len(search_good_res)))
    # print('dict len:' + str(len(modelDataDict)))
    
    # topn = 0
    # print('*' * 10)
    # print("search shop:")
    # modelDataDict = dict()
    # for d in search_shop_res:
    #     modelData = d[15]
    #     if modelData in modelDataDict:
    #         modelDataDict.update({modelData: modelDataDict[modelData] + 1})
    #     else:
    #         modelDataDict.update({modelData: 1})
    # sort_res = sorted(modelDataDict, key=modelDataDict.get, reverse=True)
    # for s in sort_res:
    #     topn += 1
    #     if topn > 30:
    #         break
    #     print("key:" + s + "; num:" + str(modelDataDict[s]))
    # print('shop res len:' + str(len(search_shop_res)))
    # print('dict len:' + str(len(modelDataDict)))
    
    with open(r'C:\Users\Administrator\Desktop\浏览好货详情.txt', 'w', encoding='utf-8') as f:
        for v in search_detail_res:
            f.write(';'.join(v))
            f.write('\n')
        f.close()

    return res

# %%
if __name__ == "__main__":
    get_user_op_log()
        

# %%
def parse2(path):
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line:
            temp_str = line.replace('\n', '')
            line = f.readline()
            while line[0:2] != '0,' and line:
                temp_str += " " + line.replace('\n', '')
                line = f.readline()

            qq = temp_str.split(',,')
            if len(qq) > 1:
                q = qq[1] [1:]
                res.append(q.split(','))
            else:
                qqq = temp_str.split(',')[4: 10]
                res.append(qqq)

        f.close()
    return res
s = parse2(r'C:\Users\Administrator\Desktop\product_dis_info.txt')
print("read ok...")

union_id_set = set()
stat_dict = dict()

for row in s:
    if len(row) > 4:
        r = row[3]
        stat = r  
        if len(r) > 2:
            print("wrong data: " + str(row))
            continue
        if stat in stat_dict:
            stat_dict.update({stat: stat_dict[stat] + 1})
        else:
            stat_dict.update({stat: 1})
    else:
        print("wrong data: " + str(row))


    # if up_time != '' and stat == '5':
    #     # 同id保留最新数据
    #     if unionId in union_id_set:
    #         pass
    #     else:
    #         union_id_set.add(unionId)

# with open(r'C:\Users\Administrator\Desktop\productid去重数据', 'w', encoding='utf-8') as f:
#     for k,v in single_product_id_data.items():
#         f.write(';'.join(v))
#         f.write('\n')
#     f.close()

print("各状态货品数：" + str(stat_dict))

# print("去重productid后货品数：" + str(len(union_id_set)))
# %%
