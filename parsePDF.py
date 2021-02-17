# %%
import codecs
import re
import PyPDF2
from tika import parser
import textract
import fitz
from py4j.java_gateway import JavaGateway
import os.path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB


#
def loadCmap(path=r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseMap.txt'):
    cmap = dict()
    with open(path, 'r') as f:
        l = f.readline()
        while l:
            res = l.replace('\n', '').split(":", 1)
            cmap.update({res[0]: res[1]})
            l = f.readline()

    return cmap

#
def writeFile(data, path, model=0, joiner='', ender=''):
    output = open(path, 'a', encoding='utf-8')
    if model == 0:
        for strings in data:
            output.writelines(joiner.join(strings))
            output.writelines(ender)
    # full write
    elif model == 1:
        output.writelines(data)

#
def parsePDF_tika(path):
    raw = parser.from_file(path)
    res = raw['content']
    writeFile(res, r'C:\Users\Administrator\Desktop\parseRes_tika.txt', model=1)


#
def parsePDF_PyPDF2(path):
    pdf_file = open(path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for i in range(number_of_pages):
        page = read_pdf.getPage(i)
        page_content = page.extractText()#.encode('ansi')
        print(page_content)
        # print(1)
        # print(page_content)
        writeFile(page_content, r'C:\Users\Administrator\Desktop\parseRes_PyPDF2.txt')
        # print(2)


# 
def parsePDF_pdfMiner(path):
    '''解析PDF文本，并保存到TXT文件中'''
    fp = open(path,'rb')
    #用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    #创建一个PDF文档
    doc = PDFDocument(parser)
    # 连接分析器，与文档对象
    # parser.set_document(doc)
    # doc.set_parser(parser)
 
    # # #提供初始化密码，如果没有密码，就创建一个空的字符串
    # doc._initialize_password()

    #检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr,laparams=laparams)
        #创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr,device)
 
        #循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            #接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if(isinstance(x,LTTextBoxHorizontal)):
                    # with open(r'C:\Users\Administrator\Desktop\parseRes_pdfminer.txt','a') as f:
                    results = x.get_text().replace('\n', '')
                    results += " start pos:(" + str(round(float(x.x0), 3)) + "," + str(round(float(x.y0), 3)) + ")"
                    results += " end pos:(" + str(round(float(x.x1), 3)) + "," + str(round(float(x.y1), 3)) + ")\n"
                    print(results)
                    writeFile(results, r'C:\Users\Administrator\Desktop\parseRes_pdfminer_with_pos.txt')
                        # f.write(results  +"\n")

# dis
def parsePDF_textract(path):
    text = textract.process(path)


#
def parsePDF_fitz(path):
    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            text += page.getText()

    writeFile(text, r'C:\Users\Administrator\Desktop\parseRes_fitz.txt')


# 
def parsePDF_JavaGateway(path):
    gw = JavaGateway()
    result = gw.entry_point.strip(path)

    # result is a dict of {
    #   'success': 'true' or 'false',
    #   'payload': pdf file content if 'success' is 'true'
    #   'error': error message if 'success' is 'false'
    # }

    writeFile(result['payload'], r'C:\Users\Administrator\Desktop\parseRes_fitz.txt')


# 按选定类型将pdf转成对应格式文件
def parsepdf_pdfminer_formal(path, outtype='txt'):
    # debug option
    debug = 0
    # input option
    password = b''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = r'C:\Users\Administrator\Desktop\parseRes_demo.' + outtype
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    encoding = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    laparams.all_texts = True
    laparams.detect_vertical = True
    # for (k, v) in opts:
    #     if k == '-d': debug += 1
    #     elif k == '-P': password = v.encode('ascii')
    #     elif k == '-o': outfile = v
    #     elif k == '-t': outtype = v
    #     elif k == '-O': imagewriter = ImageWriter(v)
    #     elif k == '-c': encoding = v
    #     elif k == '-s': scale = float(v)
    #     elif k == '-R': rotation = int(v)
    #     elif k == '-Y': layoutmode = v
    #     elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
    #     elif k == '-m': maxpages = int(v)
    #     elif k == '-S': stripcontrol = True
    #     elif k == '-C': caching = False
    #     elif k == '-n': laparams = None
    #     elif k == '-A': laparams.all_texts = True
    #     elif k == '-V': laparams.detect_vertical = True
    #     elif k == '-M': laparams.char_margin = float(v)
    #     elif k == '-W': laparams.word_margin = float(v)
    #     elif k == '-L': laparams.line_margin = float(v)
    #     elif k == '-F': laparams.boxes_flow = float(v)
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = open(outfile, 'w', encoding=encoding)
    if outtype == 'txt':
        device = TextConverter(rsrcmgr, outfp, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp)
    # else:
    #     return usage()
    # for fname in args:
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                        maxpages=maxpages, password=password,
                                        caching=caching, check_extractable=True):
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
    device.close()
    outfp.close()
    return


#
def parseCid(path, filetype='txt', cmapPath=''):
    Cmap = loadCmap() if cmapPath == '' else loadCmap(cmapPath)

    pattern = re.compile(r'\(cid:\d+\)')
    num_pattern = re.compile(r'\d+')
    res_lines = []

    with open(path, 'r', encoding='utf-8') as f:
        l = f.readline()
        while l:
            temp_l = l
            # 查询cid
            mt = pattern.findall(l)
            # 解析cid
            for i in mt:
                parse_i = Cmap[num_pattern.findall(i)[0]]
                temp_l = temp_l.replace(i, parse_i)
            res_lines.append(temp_l)
            l = f.readline()
    
    with open(r'C:\Users\Administrator\Desktop\parseRes_parseCid.' + filetype, 'w', encoding='utf-8') as f:
        for i in res_lines:
            f.writelines(i)


path = r'D:\wuziyang\wuziyang\其他项目\PDF解析\四高危机检测-demo.pdf'
path1 = r'D:\wuziyang\wuziyang\其他项目\PDF解析\免疫力相关基因检测10项.pdf'
path2 = r'D:\wuziyang\wuziyang\其他项目\PDF解析\心脑血管用药模板.pdf'
path3 = r'D:\wuziyang\wuziyang\其他项目\PDF解析\儿童安全用药 模板.pdf'
# %%
# parsePDF_tika(path)
# parsePDF_PyPDF2(path)
# parsePDF_fitz(path)
# parsePDF_pdfMiner(path1)

parsepdf_pdfminer_formal(path1, 'xml')
parseCid(r'C:\Users\Administrator\Desktop\parseRes_demo.xml', 'xml')

# %%
# 去除文档中的ASCII控制码
def strip_control_characters(s):
    word = ''
    for i in s:
        if i==codecs.BOM_UTF8:
            continue
        if ord(i)>31 or ord(i) == 10 or ord(i) ==13:
            word += i
    return word

ppath = [r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes_儿童安全用药 模板.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes_免疫力相关基因检测10项.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes_四高危机检测-demo.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes_心脑血管用药模板.xml']
tpath = [r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes__儿童安全用药 模板.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes__免疫力相关基因检测10项.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes__四高危机检测-demo.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes__心脑血管用药模板.xml']
ttpath = [r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes___儿童安全用药 模板.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes___免疫力相关基因检测10项.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes___四高危机检测-demo.xml',
        r'D:\wuziyang\wuziyang\其他项目\PDF解析\parseRes___心脑血管用药模板.xml']

# %%
for p,t in zip(ppath, tpath):
    print(p)
    with open(p, 'r', encoding='utf-8') as fo:
        with open(t, 'w', encoding='utf-8') as fw:
            for line in fo:
                fw.write(strip_control_characters(line))


# %%
for p,t in zip(tpath, ttpath):
    print(p)
    with open(p, encoding='utf-8') as fo:
        data = fo.read()
        if data[:3]==codecs.BOM_UTF8:
            data = data[3:]
            with open(t, 'w', encoding='utf-8') as fw:
                fw.write(data)

# %%
