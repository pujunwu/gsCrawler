#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re  # 导入正则表达式的库
import os  # 文件处理
import json  # json处理

import OpenUrl  # 网络请求
import ReCompile  # html截取


def downloadType():
    out = open('F:/type.txt', "r", encoding='UTF-8')
    str = out.read()
    print()
    pattern = re.compile(r'<a\shref="[^\"]*">(.*?)</a>')
    match = re.findall(pattern, str)

    types = json.dumps(match, ensure_ascii=False, indent=None)

    writeText('F:/type_json.txt', types)

    return match


# 输出文字
def writeText(path, data):
    if data and len(data):
        out = open(path, "a+", encoding='UTF-8')
        if out:
            out.write(data)
            out.close()
            return path
        else:
            return ''


# 输出文字
def writeTextMjs(path, mjs):
    out = open(path, "a+", encoding='UTF-8')
    if not out:
        return False
    for i in range(len(mjs)):
        mj = json.dumps(mjs[i], ensure_ascii=False, indent=None)
        out.write(mj+',\n')
    out.close()
    return True

# 输出文字
def writeText2(path, data):
    out = open(path, "a+", encoding='UTF-8')
    if out:
        out.write(data)
        out.close()
        return True
    else:
        return False


#下载名句
def downloadMj():
    rootUrl = 'http://so.gushiwen.org/mingju/'
    nexUrl = 'Default.aspx?p=1&c=&t='
    savePath = os.getcwd() + '/mj/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    savePath = savePath + 'mj.txt'
    print('开始拉取')
    writeText2(savePath,'[\n')
    count = 0
    while nexUrl:
        count +=1
        print('第'+str(count)+'次拉取')
        print(rootUrl + nexUrl)
        html = OpenUrl.url_open(rootUrl + nexUrl)
        try:
            # 获取下一页数据
            html = html.decode('UTF-8')
        except UnicodeEncodeError as e:
            print(e)
            html = ''
        if not html:
            nexUrl = ''
            continue
        nexUrl = ReCompile.reAuthorNexUrl(html)
        mjs = ReCompile.reMJ(html)
        writeTextMjs(savePath, mjs)
    #完成符号
    writeText2(savePath, ']')
    print('拉取完成')


if __name__ == '__main__':
    # downloadType()
    # testGs()
    # threadTest()
    downloadMj()
