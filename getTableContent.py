# %%
import parsePDF as pf
import re
import json
import numpy as np


keyWord = ['检测内容', '基因检测结果明细', '用药指导结果']
path = [
    r'C:\Users\Administrator\Desktop\parseRes_parseCid.txt',
    r'C:\Users\Administrator\Desktop\parseRes_pdfminer免疫力相关基因检测10项.txt',
    r'C:\Users\Administrator\Desktop\parseRes_pdfminer心脑血管用药模板.txt',
    r'C:\Users\Administrator\Desktop\parseRes_pdfminer儿童安全用药 模板.txt'
]


#
def getContent1(path):
    record_info = ["姓名 (NAME)", "性别 (GENDER)", "出生年月 (BIRTH DATE)", "编号样本 (SPECIMEN ID)", "报告日期 (DATE OF REPORT)"]
    content_table = '检测内容'
    pagePattern = re.compile('第 \d+ 页')
    print('process ' + path + '...')
    table_res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            line = line.replace('\n', '')
            # 处理报告封面
            if record_info[0] in line:
                temp_dict = dict()

                line = f.readline().replace('\n', '')
                while line == "" or any(k in line for k in record_info[:3]):
                    line = f.readline().replace('\n', '')
                
                if line == "":
                    line = f.readline().replace('\n', '')
                for i in range(3):
                    temp_dict.update({record_info[i]: line})
                    line = f.readline()
                    line = f.readline().replace('\n', '')
                line = f.readline()
                line = f.readline().replace('\n', '')
                temp_dict.update({record_info[3]: line})
                line = f.readline()
                line = f.readline()
                line = f.readline()
                line = f.readline().replace('\n', '')
                temp_dict.update({record_info[4]: line})
                table_res.append(temp_dict)
                line = f.readline()

            # 处理疾病，易感指数表
            elif pagePattern.findall(line):
                line = f.readline()
                if line.replace('\n', '') == "":
                    line = f.readline()
                if "疾病" in line[-4:]:
                    dis_ls = []
                    indx_ls = []
                    line = f.readline()
                    line = f.readline()
                    while not "易感指数" in line:
                        dis_ls.append(line.replace('\n', ''))
                        line = f.readline()
                        line = f.readline()
                    line = f.readline()
                    while line and not pagePattern.findall(line):
                        if line.replace('\n', '') == "":
                            line = f.readline()
                        else:
                            indx_ls.append(line.replace('\n', ''))
                            line = f.readline()
                    
                    temp_ls = []
                    for i,j in zip(dis_ls, indx_ls):
                        temp_ls.append({"疾病": i, "易感指数": j})
                    
                    table_res.append(temp_ls)
                    line = f.readline()

            # 采集表内容
            elif content_table in line:
                temp_res = []
                temp_dict = dict()
                temp_key = ""
                temp_value = []
                line = f.readline()
                # 跳过空行
                while not line.replace('\n', ''):
                    line = f.readline()
                # 到下一页退出循环
                while line and not pagePattern.findall(line):
                    line = line.replace('\n', '').replace(' ', '')
                    # 新列
                    if temp_key == "" and not line == "":
                        temp_key = line
                    # 切换列
                    elif line == "":
                        temp_dict.update({temp_key: temp_value})
                        temp_value = []
                        temp_key = ""
                    # 列值
                    else:
                        temp_value.append(line)

                    line = f.readline()
                
                # 将表数据转为合适的dict格式,方便转json
                colKey = np.array(list(temp_dict.keys()))
                colValue = np.array(list(temp_dict.values()))
                for i in range(len(colValue[0])):
                    row_dict = dict()
                    for j in range(len(colValue)):
                        row_dict.update({colKey[j]: colValue[j][i]})
                    temp_res.append(row_dict)

                # table_res.update({len(table_res): temp_res})
                table_res.append(temp_res)
            
                line = f.readline()
            else:
                line = f.readline()
        
        # json output
        with open(path.split('.')[0] + '_json.txt', 'w') as fw:
            json.dump(table_res, fw, ensure_ascii=False)


#
def getContent2(path):
    key = ["检测项目", "基因名", "基因型", "评估结果"]
    print('process ' + path + '...')
    table_res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            #只有一张表
            if "基因检测结果明细：" in line:
                # 四组数据依次排列，由于数据量不确定，需要先取出再处理
                res = []
                line = f.readline()
                while line.replace('\n', '') == "" or any(k in line for k in key):
                    line = f.readline()
                while line and not line.replace('\n', '') == "2":
                    res.append(line.replace('\n', ''))
                    line = f.readline()
                    line = f.readline()
                rows = int(len(res) / 4)
                temp_ls = []
                for i in range(rows):
                    temp_ls.append({"检测项目": res[i], "基因名": res[i + rows], "基因型": res[i + rows * 2], "评估结果": res[i + rows * 3]})

                table_res.append(temp_ls)

            else:
                line = f.readline()

        # json output
        with open(path.split('.')[0] + '_json.txt', 'w') as fw:
            json.dump(table_res, fw, ensure_ascii=False)


def getContent3(path):
    record_info = ["姓名 (NAME)", "性别 (GENDER)", "出生年月 (BIRTH DATE)", "编号样本 (SPECIMEN ID)", "报告日期 (DATE OF REPORT)"]
    colName = ["中文名", "主要成分", "遗传评估", "服用指导"]
    filterName = ["心脑血管疾病精准用药报告", "t下页续", "s接上页"]
    col3 = ["慢代谢型", "中等代谢型", "正常疗效", "疗效较好", "普通风险", "正常代谢型"]
    col4 = ["正常服用", "减量服用", "加强监测疗效或更换药物", "加强毒副反应监控"]
    print('process ' + path + '...')
    table_res = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            #样本信息
            if "样本信息" == line.replace('\n', ''):
                temp_dict = dict()
                while any(k in line for k in record_info):
                    k = line
                    line = f.readline()
                    if any(k in line for k in record_info):
                        temp_dict.update({k: ""})
                    else:
                        temp_dict.update({k: line})
                        line = f.readline()
                
                table_res.append(temp_dict)

            # 表
            elif "用药指导结果" == line.replace('\n', ''):
                "药物" == line.replace('\n', '')[-2:]



            else:
                line = f.readline()

        # json output
        with open(path.split('.')[0] + '_json.txt', 'w') as fw:
            json.dump(table_res, fw, ensure_ascii=False)


# %%
# getContent1(path[0])
# getContent2(path[1])
getContent3(path[2])

# %%
