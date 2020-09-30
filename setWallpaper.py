# %%
#coding=utf-8

__author__ = 'Administrator'

import pythoncom
from win32com.shell import shell, shellcon
import json
from time import sleep


def read_path(path, limit=-1):
    result = []
    image_indx = {}
    indx = 0
    for maindir, _, file_name_list in os.walk(path):
        for filename in file_name_list:
            # filter json
            if not filename.split('.')[1] == 'json':
                apath = os.path.join(maindir, filename)
                result.append(apath)
                # deal with image index
                image_indx.update({filename: indx})
                indx += 1
        break
    if limit >= 0:
        ed_idx = min(limit, len(result))
        result = result[:ed_idx]
    
    return result


g_desk = None

def toGBK(s):
    return s.decode('utf-8').encode('gb2312')

def getDeskComObject():
    global g_desk
    if not g_desk:
        g_desk = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, \
                                             None, pythoncom.CLSCTX_INPROC_SERVER, \
                                             shell.IID_IActiveDesktop)
    return g_desk

def setWallPaper(paper):
    desktop = getDeskComObject()
    if desktop:
        desktop.SetWallpaper(paper, 0)
        desktop.ApplyChanges(shellcon.AD_APPLY_ALL)

def addUrlLink(lnk):
    desktop = getDeskComObject()
    desktop.AddUrl(0, lnk, 0, 0)

if __name__ == '__main__':
    path = read_path(r'C:\Users\Administrator\Desktop\test2')
    for p in path:
        sleep(0.1)
        setWallPaper(p)
# %%
