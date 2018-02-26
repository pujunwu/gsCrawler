#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json  # json处理
import os
import threading  # 多线程

import time
import OpenUrl  # 自定义网页获取库
import ReCompile  # 自定义截取字符串库
import WriteText  # 自定义文件输出库
import FileUtils  # 自定义文件处理

# 网页根路径
rootUrl = 'http://so.gushiwen.org/'
GSCOUNTDD = 0


# 获取诗文的注释、译文、赏析
def defPoetryZSYWSX(id):
    url = rootUrl + 'shiwen2017/ajaxshiwencont.aspx?id=' + id + '&value='
    yiwen = OpenUrl.url_open(url + 'yi')
    # 获取译文
    try:
        yiwen = yiwen.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    # 获取注释
    zhushi = OpenUrl.url_open(url + 'zhu')
    try:
        zhushi = zhushi.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    # 获取赏析
    shangxi = OpenUrl.url_open(url + 'shang')
    try:
        shangxi = shangxi.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    yiwen = isError(yiwen)
    zhushi = isError(zhushi)
    shangxi = isError(shangxi)
    # 诗歌信息
    # print('yiwen:' + yiwen)
    # print('zhushi:' + zhushi)
    # print('shangxi:' + shangxi)
    return ReCompile.reZSYWSX(zhushi, yiwen, shangxi)


# 获取诗人page_url链接下的所有首诗的信息
def funAuthorPoetry(html, authorName, authorpoetrys, filePath, is_print):
    poetrys = ReCompile.reAuthorPoetrys(html)
    if not authorpoetrys:
        authorpoetrys = []
    if not poetrys:
        return authorpoetrys
    for i in poetrys:
        # url = rootUrl + 'shiwen2017/ajaxshiwencont.aspx?id=' + i["id"] + '&value=yizhushang'
        # text = OpenUrl.url_open(url)
        # # 获取译文
        # try:
        #     text = text.decode('utf-8')
        # except UnicodeEncodeError as e:
        #     print(e)
        #     continue
        # text = isError(text)
        # if text:
        #     contexts = ReCompile.reZSYWSX(text)
        # else:
        #     contexts = {}
        contexts = defPoetryZSYWSX(i["id"])
        if contexts:
            # 诗歌信息
            poetryInfo = ReCompile.reAuthorPoetryInfo(i["content"], authorName, contexts['yw'],
                                                      contexts['zs'], contexts['sx'])
        else:
            # 诗歌信息
            poetryInfo = ReCompile.reAuthorPoetryInfo(i["content"], authorName, '', '', '')

        # 输出诗歌
        WriteText.writePoetry(poetryInfo, filePath, authorName)

        if is_print:
            print(authorName + '的诗：')
            print(poetryInfo)
        authorpoetrys.append(authorName)
    return authorpoetrys


def isError(str):
    if str:
        p = str.find('网页发生错误', 0)
        if p != -1 or len(str) < 5:
            return ''
    return str


# 获取诗人信息包括对应的诗
def funAuthorInfos(page_url, authorId, savePath, is_print, startPage='1'):
    print('\n' + page_url + '\n')
    try:
        html = OpenUrl.url_open(page_url).decode('utf-8')
    except UnicodeEncodeError:
        return False
    # print(html)
    p = html.find('该文章不存在或已被删除')
    if p != -1:
        return False
    # 头像
    head = ReCompile.reAuthorImage(html)
    # 名称
    name = ReCompile.reAuthorName(html)
    # 介绍
    introduce = ReCompile.reAuthorExplain(html, name)
    # 详细介绍
    explain = ReCompile.reAuthorExplainDetailed(html)
    # 点赞
    fabulou = ReCompile.reAuthorFabulou(html)
    # 诗人对应的诗的链接  http://so.gushiwen.org/authors/authorsw_3067A1.aspx
    poetryNexUrl = 'authors/authorsw_' + str(authorId) + 'A' + str(
        startPage) + '.aspx'  # ReCompile.reAuthorPoetryUrl(html)
    # 诗人的诗保存的路径
    filePath = authorId + '_' + name + '.txt'
    # 诗人信息
    author = {'authorId': authorId, 'name': name, 'head': head, 'introduce': introduce, 'explain': explain,
              'poetrys': filePath, 'fabulou': fabulou}
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    # 保存诗人信息
    savePathName = writeAuthor(author, savePath)
    mutex.release()  # 释放锁
    global GSCOUNTDD
    GSCOUNTDD += 1
    print('第' + str(GSCOUNTDD) + '个诗人')
    if savePathName:
        WriteText.writeCatalog({'author': author['name'], 'fileName': savePathName, 'fabulou': fabulou}, savePath)
    # return True
    if is_print:
        print(author)
    print('诗人：' + name)
    # 诗歌输出路径
    filePath = savePath + '/poetrys/' + filePath
    # 保存诗歌开头格式
    WriteText.writePoetryJson('[\n{}', filePath, name)
    # 诗人写的所有诗
    authorpoetrys = []
    # 循环获取诗
    while poetryNexUrl:
        if is_print:
            print('\n' + '当前链接下所有的诗的信息：')
            print(rootUrl + poetryNexUrl)
        # http://so.gushiwen.org/authors/authorsw_247A1.aspx
        try:
            # 获取下一页数据
            html = OpenUrl.url_open(rootUrl + poetryNexUrl).decode('UTF-8', 'ignore')
        except UnicodeEncodeError as e:
            print(e)
            poetryNexUrl = ''
            continue
        # 获取诗人写的诗信息
        authorpoetrys = funAuthorPoetry(html, name, authorpoetrys, filePath, is_print)
        # 获取下一页链接 返回链接格式authors/authorsw_247A1.aspx
        poetryNexUrl = ReCompile.reAuthorPoetryNexUrl(html)
    # 保存诗歌结束格式
    WriteText.writePoetryJson(']', filePath, name)
    return True


# 输出诗人信息 诗人介绍，诗人写的诗，诗人的头像等信息
def writeAuthor(author, rootPath):
    if not rootPath:
        rootPath = os.getcwd()
    imageUrl = author['head']
    # if not imageUrl:
    #     imageName = ''
    # else:
    #     # 保存头像
    #     imageName = WriteText.saveImgs(rootPath + '/authorhead/', imageUrl, OpenUrl.url_open(imageUrl))
    # 将头像路径保存在信息中
    headUrls = imageUrl.split('/')
    author['head'] = headUrls[len(headUrls) - 1]
    # 对象转json
    jsonAuthor = json.dumps(author, ensure_ascii=False, indent=None)
    # 保存文件名称
    fileName = author['authorId'] + '_' + author['name'] + '.txt'
    # 保存信息成功返回文件名称
    if WriteText.writeTextFile(rootPath + '/authors/' + fileName, jsonAuthor + '\n', author['name']):
        return fileName
    return ''


authorPathsff = []


# 获取诗人的详细介绍以及诗
def funAuthors(html, rootSave, is_print, threadCount, authorPaths, startPage='1'):
    authorUrls = ReCompile.reAuthorUrls(html)
    # 检查是否拉取成功
    if authorPaths:
        global GSCOUNTDD
        authors = []
        for item in authorUrls:
            authorPathsff.append(item)
            GSCOUNTDD += 1
            print('第' + str(GSCOUNTDD) + '个诗人')
            if FileUtils.getFileName(authorPaths, item['id']):
                authors.append(item)
        if authors:
            for item in authors:
                authorUrls.remove(item)
    print(authorUrls)
    if not authorUrls:
        return True

    print('请求人数：' + str(len(authorUrls)))
    if authorUrls:
        i = 0
        length = len(authorUrls)
        if threadCount > length:
            threadCount = length
        while i < length:
            threads = []
            # 循环创建线程
            for j in range(threadCount):
                if i >= length:
                    break
                item = authorUrls[i]
                threads.append(threading.Thread(target=funAuthorInfos,
                                                args=(item['url'], item['id'], rootSave, is_print, startPage)))
                i += 1
            threadStart = []
            # 执行线程
            for t in threads:
                t.setDaemon(True)
                t.start()
                threadStart.append(t)
            for ts in threadStart:
                ts.join()  # 等待线程执行完成

                # for i in authorUrls:
                #     if not i['url']:
                #         continue
                #     funAuthorInfos(i['url'], i['id'], rootSave, is_print,startPage)
    else:
        print('获取诗人id和链接失败')


def downloadAuthor():
    # int(get_page(url))#最大值316
    # 诗人简绍
    # http://so.gushiwen.org/authors/Default.aspx?p=316&c=
    # 诗人详细介绍
    # http://so.gushiwen.org/author_3152.aspx
    # 诗人的诗文
    # http://so.gushiwen.org/authors/authorsw_247A1.aspx
    # 诗文
    # http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id = 21744&value=cont
    # 译文 正文和译文用<br />分隔遇到 <p style=" color:#919090;margin:0px; font-size:12px;line-height:160%;">参考资料：</p> 就完成
    # http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=22550&value=yi
    # 注释 规则同译文
    # http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=22550&value=zhu
    # 赏析正文和赏析内容用div分隔
    # http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=22550&value=shang
    # 诗文赏析  翻译 注释 赏析
    # http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=7722&value=yizhushang
    # 诗文详细介绍
    # http://so.gushiwen.org/view_7722.aspx
    print('开始获取')
    count = 0
    url = rootUrl + 'authors/'
    authorNextUrl = 'Default.aspx?p=1&c='
    savePath = os.getcwd() + '/ancientpoetry'
    WriteText.writeCatalogJson('[\n{}', savePath)
    while authorNextUrl:
        print('\n' + url + authorNextUrl + '\n')
        html = OpenUrl.url_open(url + authorNextUrl)
        count += 1
        try:
            # 获取当page_url链接下的数据
            html = html.decode('utf-8')
        except UnicodeEncodeError as e:
            print(e)
            continue
        except AttributeError as e:
            print(e)
        if not html:
            authorNextUrl = ''
        else:
            pag = ReCompile.reNextUrlPag(authorNextUrl)
            WriteText.writeLog(savePath, '当前第' + str(count) + '次循环请求：')
            WriteText.writeLog(savePath, '访问网站第' + pag + '页数据如下：')
            WriteText.writeLog(savePath, '访问链接：' + url + authorNextUrl)
            # 获取当前页的所有诗人信息及写的诗信息
            # funAuthors(html, savePath, False, 5, '1')
            # 获取下一页链接
            authorNextUrl = ReCompile.reAuthorNexUrl(html)
            print('访问网站第' + pag + '页数据如下：')
            print('当前第' + str(count) + '次循环请求。')
    # 输出目录结束符号
    WriteText.writeCatalogJson(']', savePath)
    print('拉取完成,一共拉取：' + str(count) + '页')


# 拉取诗人信息和诗
def downloadAuthorAndPoetry(savePath, is_print, authorPaths, startPag='1', threadPag=2, authorCount=2):
    print('开始获取')
    count = 0
    url = rootUrl + 'authors/'
    authorNextUrl = 'Default.aspx?p=' + startPag + '&c='
    while authorNextUrl:
        htmls = []
        for i in range(threadPag):
            htmls.append(getAuthorAndNextUrlHtml(url + authorNextUrl))
            # 获取下一页链接
            authorNextUrl = htmls[len(htmls) - 1]['nexUrl']
            if not authorNextUrl:
                break
        # 启动线程
        threads = []
        for i in htmls:
            count += 1
            print('请求链接:')
            print(i['currentUrl'])
            # 打印日志
            WriteText.writeLog(savePath, '当前第' + str(count) + '次循环请求：')
            WriteText.writeLog(savePath, '访问网站第' + ReCompile.reNextUrlPag(i['currentUrl']) + '页数据如下：')
            WriteText.writeLog(savePath, '访问链接：' + i['currentUrl'] + '\n')
            # 获取当前页的所有诗人信息及写的诗信息
            threads.append(threading.Thread(target=funAuthors,
                                            args=(i['html'], savePath, is_print, authorCount, authorPaths, '1')))

        threadsStart = []
        # 启动线程
        for t in threads:
            t.setDaemon(True)
            t.start()
            threadsStart.append(t)
        # 等待线程执行完成
        for ts in threadsStart:
            ts.join()
    print('拉取完成,一共拉取：' + str(count) + '页')


# 获取佚名诗人page_url链接下的所有首诗的信息
def funNamelessAuthorPoetry(html, authorName, authorpoetrys, filePath, is_print):
    poetrys = ReCompile.reAuthorPoetrys(html)
    if not authorpoetrys:
        authorpoetrys = []
    if not poetrys:
        return authorpoetrys
    for i in poetrys:
        # http://so.gushiwen.org/view_131.aspx
        # url = rootUrl + 'shiwen2017/ajaxshiwencont.aspx?id=' + i["id"] + '&value=yizhushang'
        # text = OpenUrl.url_open(url)
        # # 获取译文
        # try:
        #     text = text.decode('utf-8')
        # except UnicodeEncodeError as e:
        #     print(e)
        #     continue
        # text = isError(text)
        # if text:
        #     contexts = ReCompile.reZSYWSX(text)
        # else:
        #     contexts = {}
        contexts = defPoetryZSYWSX(i["id"])
        if is_print:
            print(contexts)
        if contexts:
            # 诗歌信息
            poetryInfo = ReCompile.reNamelessAuthorPoetryInfo(i["content"], authorName, contexts['yw'],
                                                              contexts['zs'], contexts['sx'])
        else:
            # 诗歌信息
            poetryInfo = ReCompile.reNamelessAuthorPoetryInfo(i["content"], authorName, '', '', '')
        # 输出诗歌
        WriteText.writePoetry(poetryInfo, filePath, authorName)
        if is_print:
            print(authorName + '的诗：')
            print(poetryInfo)
        authorpoetrys.append(authorName)
    return authorpoetrys


# 拉取遗漏诗人和诗信息
def funMissingAuthorPoetry(missings, savePath, is_print):
    if not missings:
        return False
    for mis in missings:
        authorId = mis.split('_')[0]
        funAuthorInfos(rootUrl + 'author_' + str(authorId) + '.aspx', authorId, savePath, is_print)
    return True


# 拉取佚名诗人的诗
def funNamelessAuthorInfos(savePath, is_print, startPage='1'):
    authorId = '3157'
    name = '佚名'
    fabulou = '500'
    # 佚名诗人的诗  http://so.gushiwen.org/search.aspx?type=author&page=3&value=%E4%BD%9A%E5%90%8D
    poetryNexUrl = 'search.aspx?type=author&page=' + str(startPage) + '&value=%E4%BD%9A%E5%90%8D'
    # 诗人的诗保存的路径
    filePath = authorId + '_' + name + '.txt'
    # 诗人信息
    author = {'authorId': authorId, 'name': name, 'head': '', 'introduce': '', 'explain': '',
              'poetrys': filePath, 'fabulou': fabulou}
    # 保存诗人信息
    savePathName = writeAuthor(author, savePath)
    if savePathName:
        WriteText.writeCatalog({'author': author['name'], 'fileName': savePathName, 'fabulou': fabulou}, savePath)
    if is_print:
        print(author)
    print('诗人：' + name)
    # 诗歌输出路径
    filePath = savePath + '/poetrys/' + filePath
    # 保存诗歌开头格式
    WriteText.writePoetryJson('[\n{}', filePath, name)
    # 诗人写的所有诗
    authorpoetrys = []
    count = 0
    # 循环获取诗
    while poetryNexUrl:
        if is_print:
            print('\n' + '当前链接下所有的诗的信息：')
            print(rootUrl + poetryNexUrl)
        # http://so.gushiwen.org/authors/authorsw_247A1.aspx
        try:
            # 获取下一页数据
            html = OpenUrl.url_open(rootUrl + poetryNexUrl).decode('UTF-8', 'ignore')
        except UnicodeEncodeError as e:
            print(e)
            poetryNexUrl = ''
            continue
        # 获取诗人写的诗信息
        authorpoetrys = funNamelessAuthorPoetry(html, name, authorpoetrys, filePath, is_print)
        # 获取下一页链接 返回链接格式authors/authorsw_247A1.aspx
        poetryNexUrl = ReCompile.reAuthorPoetryNexUrl(html)
        count += 1
        print('佚名诗词第' + str(count) + '页，拉取完成')
    # 保存诗歌结束格式
    WriteText.writePoetryJson(']', filePath, name)
    return True


# 获取网页信息和下一页链接
def getAuthorAndNextUrlHtml(pagUrl):
    html = OpenUrl.url_open(pagUrl)
    try:
        # 获取下一页数据
        html = html.decode('UTF-8')
    except UnicodeEncodeError as e:
        print(e)
        html = ''
    if html:
        poetryNexUrl = ReCompile.reAuthorNexUrl(html)
        return {'html': html, 'nexUrl': poetryNexUrl, 'currentUrl': pagUrl}
    else:
        return {'html': '', 'nexUrl': '', 'currentUrl': pagUrl}


def testGs():
    poetryNexUrl = 'authors/authorsw_2733A1.aspx'
    filePath = os.getcwd() + '/authors' + '/poetrys/2733_武汉臣.txt'
    while poetryNexUrl:
        try:
            # 获取下一页数据
            html = OpenUrl.url_open(rootUrl + poetryNexUrl).decode('UTF-8', 'ignore')
        except UnicodeEncodeError as e:
            print(e)
            poetryNexUrl = ''
            continue
        # 获取诗人写的诗信息
        funAuthorPoetry(html, '武汉臣', [], filePath, False)
        # 获取下一页链接 返回链接格式authors/authorsw_247A1.aspx
        poetryNexUrl = ReCompile.reAuthorPoetryNexUrl(html)
        # #测试文件输出
        # WriteText.writeAuthorText(os.getcwd()+'/wod/text.txt','输出的内容')


def testzsywsx():
    # 72486
    url = rootUrl + 'shiwen2017/ajaxshiwencont.aspx?id=72486&value='
    yiwen = OpenUrl.url_open(url + 'yi')
    # 获取译文
    try:
        yiwen = yiwen.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    # 获取注释
    zhushi = OpenUrl.url_open(url + 'zhu')
    try:
        zhushi = zhushi.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    # 获取赏析
    shangxi = OpenUrl.url_open(url + 'shang')
    try:
        shangxi = shangxi.decode('utf-8')
    except UnicodeEncodeError as e:
        print(e)
    except AttributeError as e:
        print(e)
    yiwen = isError(yiwen)
    zhushi = isError(zhushi)
    shangxi = isError(shangxi)
    # 诗歌信息
    print('yiwen:' + yiwen)
    print('zhushi:' + zhushi)
    print('shangxi:' + shangxi)


def textContent():
    html = OpenUrl.url_open('http://so.gushiwen.org/search.aspx?type=author&page=2&value=%E4%BD%9A%E5%90%8D')
    try:
        # 获取下一页数据
        html = html.decode('UTF-8')
    except UnicodeEncodeError as e:
        print(e)
        html = ''
    if html:
        context = ReCompile.reAuthorPoetrys(html)
        # contexts = ReCompile.reAuthorPoetryInfo(context[1]['content'], '佚名', '', '', '')
        contexts = ReCompile.reNamelessAuthorPoetryInfo(context[9]['content'], '佚名', '', '', '')

        jsonAuthor = json.dumps(context, ensure_ascii=False, indent=None)
        print(jsonAuthor)
        jsonAuthor = json.dumps(contexts, ensure_ascii=False, indent=None)
        print(jsonAuthor)


# #  7722
# url = 'http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=72486&value=yizhushang'
# try:
#     # 获取下一页数据
#     html = OpenUrl.url_open(url).decode('UTF-8', 'ignore')
# except UnicodeEncodeError as e:
#     html = ''
#     print(e)
# if html:
#     jsonAuthor = json.dumps(ReCompile.reZSYWSX(html), ensure_ascii=False, indent=None)
#     print(jsonAuthor)


def textHtmlContent():
    url = 'http://so.gushiwen.org/author_604.aspx'
    try:
        # 获取下一页数据
        html = OpenUrl.url_open(url).decode('UTF-8', 'ignore')
    except UnicodeEncodeError as e:
        html = ''
        print(e)
    if html:
        # jsonAuthor = json.dumps(ReCompile.reAuthorExplainDetailed(html), ensure_ascii=False, indent=None)
        jsonAuthor = ReCompile.reAuthorExplain(html, '皮日休')
        print(jsonAuthor)


if __name__ == '__main__':
    # startTimer = time.time()
    dirs = os.path.dirname(os.getcwd())
    savePath = dirs + '/ancientpoetry'
    # # 目录开始
    # WriteText.writeCatalogJson('[\n{}', savePath)
    # authorPaths = FileUtils.eachFile(savePath + '/authors')
    # # 拉取诗人和诗
    # downloadAuthorAndPoetry(savePath, False, authorPaths, '1', 1, 5)
    # jsonStrs = json.dumps(authorPathsff, ensure_ascii=False, indent=None)
    # # 写入文件
    # WriteText.writeDirs(savePath + "/", jsonStrs)
    # # 拉取佚名诗
    # # funNamelessAuthorInfos(savePath, False, '1')
    # # 输出目录结束符号
    # WriteText.writeCatalogJson(']', savePath)
    # c = time.time() - startTimer
    # print('执行时长：')
    # print(c)

    # 获取遗漏诗人信息
    fileNames = FileUtils.eachFile('F:\\python\\ancientpoetry2\\authors')
    contents = FileUtils.eachFile1('C:\\Users\\adminstrators\\Desktop\\古诗\古诗\\ancientpoetry\\authors')
    difference = list(set(contents).difference(set(fileNames)))
    funMissingAuthorPoetry(difference, savePath, False)

    # downloadAuthor()

    # testGs()
    # testzsywsx()

    # textHtmlContent()
    # defPoetryZSYWSX('7722')
    # textContent()
