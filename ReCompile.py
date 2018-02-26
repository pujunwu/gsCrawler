#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re  # 导入正则表达式的库

'''
正则表达式截取符合规则的字符串
返回字符串数组
'''


def reCompile(reg, str):
    pattern = re.compile(reg)
    match = re.findall(pattern, str)
    return match


# 从诗人列表获取诗人对应的介绍详情页链接http://www.
def reAuthorUrls(str):
    authorUrls = reCompile(
        r'<textarea\sstyle="[^\"]*"\scols="1"\srows="1"\sid="txtareAuthor[0-9]*">[^\"]*http(.*?)</textarea>', str)
    authors = []
    if authorUrls:
        for i in range(len(authorUrls)):
            url = authorUrls[i]
            p = url.find('author_')
            p1 = url.find('.aspx')
            en = {}
            if p != -1 and p1 != -1:
                en['id'] = url[p + 7:p1]
                en['url'] = 'http' + url
            else:
                en.url = 'http' + url
            authors.append(en)
    return authors


# 获取诗人图片链接 http://www.
def reAuthorImage(str):
    p = str.find('<div class="divimg">', 0)
    p1 = str.find('" width="105" height="150" alt="', p)
    if p != -1 and p1 != -1:
        image = str[p + 21:p1]
        p = image.find('"')
        if p != -1:
            image = image[p + 1:]
            return image
    return ''


# 获取诗人名称 李白
def reAuthorName(str):
    authorName = reCompile(
        r'<h1\sstyle="font-size:20px;\sline-height:22px;\sheight:22px;\smargin-bottom:10px;">(.*?)</h1>', str)
    if authorName:
        return authorName[0]
    return ''


# 获取诗人介绍 简单说明
def reAuthorExplain(str, name):
    # <h2 style="margin-bottom:10px;font-weight:bold; font-size:16px;">
    explain = reCompile(
        r'<h1\sstyle="font-size:20px;\sline-height:22px;\sheight:22px;\smargin-bottom:10px;">[^\"]*<p\sstyle="\smargin:0px;">(.*?)</p>',
        str)
    if explain:
        ex = explain[0]
        a = ex.find(name, 0)
        b = ex.find(name + '，', 0)
        if a == -1 or a > 1:
            ex = name + '：' + ex
        elif b == 0:
            ex = ex.replace(name + '，', name + '：')
        else:
            ex = ex.replace(name, name + '：')
        return ex
    return ''


# 获取诗人介绍[{'title':'纪念建筑','context':'对应说明'}, {'title': '后世纪念'},'context':'对应说明'}]
def reAuthorExplainDetailed(str):
    p = 0
    p1 = 0
    detailed = []
    while p > -1 and p1 > -1:
        p = str.find('<div class="contyishang">', p)
        p1 = str.find('</div>', p + 25)
        if p == -1 or p1 == -1:
            continue
        content = str[p + 25:p1]
        p = content.find('<h2 style="font-weight:bold; font-size:16px; margin-bottom:10px;">', 0)
        p2 = content.find('</h2>', p + 66)
        title = content[p + 66:p2]
        p3 = content.find('<a title="收起" href="javascript:fanyiClose', p2 + 5)
        if p3 > -1:
            content = content[p2 + 5:p3]
        else:
            content = content[p2 + 5:]
        content = content.replace('\n', '')
        p = p1
        detailed.append({'title': title, 'content': content})
    return detailed

    # p = 0
    # detailed = []
    # iden1 = '<h2 style="font-weight:bold; font-size:16px; margin-bottom:10px;">'
    # leng1 = len(iden1)
    # iden2 = '<a title="收起" href="javascript:fanyiClose'
    # leng2 = len(iden2)
    # while p != -1:
    #     p = str.find(iden1, p)
    #     if p != -1:
    #         p1 = str.find('</h2>', p)
    #         title = str[p + leng1:p1]
    #         p = str.find(iden2, p1)
    #         if p1 == -1 or p == -1:
    #             context = ''
    #             p = -1
    #         else:
    #             context = str[p1 + 5:p]
    #             p = p + leng2
    #         detailed.append({'title': title, 'context': context + '</p>'})
    # return detailed


# 获取赞的数量
def reAuthorFabulou(html):
    # <img src="/img/good.png" / alt="赞" width="14" height="14"/><span>&nbsp;4917</span></a></div>
    p = html.find('<img src="/img/good.png" / alt="赞" width="14" height="14"/><span>&nbsp;', 0)
    p1 = html.find('</span></a></div>', p + 71)
    if p != -1 and p1 != -1:
        return html[p + 71:p1]
    else:
        return '-1'


# 诗人写的诗的链接
def reAuthorPoetryUrl(str):
    p = str.find('<div class="title" style=" text-align:center; height:40px; line-height:40px;">', 0)
    p1 = str.find('</div>', p)
    if p == -1:
        return ''
    a = str[p + 76:p1]
    p = a.find('/authors')
    p1 = a.find('.aspx">', p)
    if p == -1:
        return ''
    a = a[p:p1 + 5]
    return a


# 获取诗文信息
def reAuthorPoetrys(html):
    iden1 = '<div class="sons">'
    leng1 = len(iden1)
    iden2 = '<div style=" width:1px; height:1px; overflow:hidden;">'
    p = 0
    poetryHtmls = []
    p4 = html.find('<div class="pages">', p)
    while p != -1:
        p = html.find(iden1, p)
        p1 = html.find(iden2, p)
        if p1 > p4 or p1 == -1:
            p1 = p4
        if p != -1 and p1 != -1:
            context = html[p + leng1:p1]
            p2 = context.find('OnShangxi(')
            p3 = context.find(')"', p2)
            if p2 != -1:
                id = context[p2 + 10:p3]
                poetryHtmls.append({'content': context, 'id': id})
            p = p1
    return poetryHtmls


# 获取佚名诗文信息
def reNamelessAuthorPoetrys(html):
    # <a\sstyle="font-size:18px;\sline-height:22px;\sheight:22px;\s"\shref="[^\"]*"\starget="_blank">
    # explain = reCompile(r'target="_blank"><b>(.*?)<div\sclass="tool">',html)
    p = 0
    poetryHtmls = []
    while p != -1:
        p = html.find('<a style="font-size:18px; line-height:22px; height:22px; " href="/view_', p)
        p1 = html.find('</a>\n</div>\n</div>', p)
        if p != -1:
            context = html[p + 71:p1 + 4]
            p2 = context.find('.aspx')
            if p2 != -1:
                id = context[0:p2]
                poetryHtmls.append({'content': context, 'id': id})
        p = p1
    return poetryHtmls


# # 获取诗文信息
# def reAuthorPoetryInfo(html, name, yiwen, zhushi, shangxi):
#     p = html.find('<div class="contson"', 0)
#     p = html.find('">', p)
#     p2 = html.find('</div>', p)
#     if p == -1:
#         return {}
#     shiwen = html[p + 2:p2]
#     # tags = html[html.find('<div class="tag">', p2) + 17:]
#     tagContexts = reCompile(r'<a href="[/type.aspx?p=][^\"]*">(.*?)</a>', html)
#     p = html.find('target="_blank"><b>', 0)
#     p2 = html.find('</b></a></p>', p)
#     title = html[p + 19:p2]
#     # 点赞
#     fabulou = reAuthorFabulou(html)
#     # 类型
#     if not tagContexts:
#         tagContexts = []
#     else:
#         tagContexts.remove(name)
#     # 译文
#     if yiwen:
#         yiwens = reCompile(r'<span style="color:#993300;">(.*?)</span>', yiwen)
#         yiwenStr = ''
#         if yiwens:
#             for i in yiwens:
#                 yiwenStr += '<p>' + i + '</p>'
#     else:
#         yiwenStr = ''
#     # 注释
#     if zhushi:
#         zhushis = reCompile(r'<span style="color:#006600;">(.*?)</span>', zhushi)
#         zhushiStr = ''
#         if zhushis:
#             for i in zhushis:
#                 zhushiStr += '<p>' + i + '</p>'
#     else:
#         zhushiStr = ''
#     # 赏析
#     if shangxi:
#         shangxis = reCompile(r'<p>(.*?)</p>', shangxi)
#         shangxieStr = ''
#         if shangxis:
#             for i in shangxis:
#                 shangxieStr += '<p>' + i + '</p>'
#         zhiliaoStr = shangxi[shangxi.find('<p style=" color:#919090;margin:0px; font-size:12px;line-height:160%;">'):]
#         zi = zhiliaoStr.find('<a style')
#         if zi:
#             zhiliaoStr = zhiliaoStr[0:zi]
#     else:
#         shangxieStr = ''
#         zhiliaoStr = ''
#
#     sg = {'title': title, 'author': name, 'context': shiwen, "types": tagContexts, 'yiwen': yiwenStr,
#           'zhushi': zhushiStr, 'shangxi': shangxieStr, 'zhiliao': zhiliaoStr, 'fabulou': fabulou}
#     # print('诗文：'+shiwen)
#     # print('类型：')
#     # print(tagContexts)
#     # print('译文：'+yiwenStr)
#     # print('注释：'+zhushiStr)
#     # print('赏析：'+shangxieStr)
#     # print('参考资料：' + zhiliaoStr)
#     return sg

# 获取诗文信息
def reAuthorPoetryInfo(html, name, yiwen, zhushi, shangxi):
    p = html.find('<div class="contson"', 0)
    p = html.find('">', p)
    p2 = html.find('</div>', p)
    if p == -1:
        return {}
    shiwen = html[p + 2:p2]
    # 正文去掉注解
    p = 0
    while p != -1:
        p = shiwen.find('(', p)
        if p == -1:
            p = shiwen.find('（', p)
        if p == -1:
            continue
        p1 = shiwen.find(')', p)
        if p1 == -1:
            p1 = shiwen.find('）', p)
        shiwen = shiwen[0:p] + shiwen[p1 + 1:]
        p = p1 + 1
    # tags = html[html.find('<div class="tag">', p2) + 17:]
    tagContexts = reCompile(r'<a href="[/type.aspx?p=][^\"]*">(.*?)</a>', html)
    p = html.find('href="/view_', 0)
    p2 = html.find('.aspx"', p)
    id = html[p + 12:p2]
    p = html.find('target="_blank"><b>', p2)
    p2 = html.find('</b></a></p>', p)
    title = html[p + 19:p2]
    # 点赞
    fabulou = reAuthorFabulou(html)
    # 类型
    if not tagContexts:
        tagContexts = []
    else:
        tagContexts.remove(name)
    # 去掉\n换行
    shiwen = shiwen.replace('\n', '')

    sg = {'title': title, 'author': name, 'content': shiwen, "types": tagContexts, 'yiwen': yiwen,
          'zhushi': zhushi, 'shangxi': shangxi, 'fabulou': fabulou, 'poetryId': id}
    # print('诗文：'+shiwen)
    # print('类型：')
    # print(tagContexts)
    # print('译文：'+yiwenStr)
    # print('注释：'+zhushiStr)
    # print('赏析：'+shangxieStr)
    # print('参考资料：' + zhiliaoStr)
    return sg


# 获取佚名诗文信息
def reNamelessAuthorPoetryInfo(html, name, yiwen, zhushi, shangxi):
    p = html.find('<div class="contson"', 0)
    p = html.find('">', p)
    p2 = html.find('</div>', p)
    if p == -1:
        return {}
    shiwen = html[p + 2:p2]
    # 正文去掉注解
    p = 0
    while p != -1:
        p = shiwen.find('(', p)
        if p == -1:
            p = shiwen.find('（', p)
        if p == -1:
            continue
        p1 = shiwen.find(')', p)
        if p1 == -1:
            p1 = shiwen.find('）', p)
        shiwen = shiwen[0:p] + shiwen[p1 + 1:]
        p = p1 + 1
    # tags = html[html.find('<div class="tag">', p2) + 17:]
    tagContexts = reCompile(r'<a href="[/type.aspx?p=][^\"]*">(.*?)</a>', html)
    p = html.find('href="/view_', 0)
    p2 = html.find('.aspx"', p)
    id = html[p + 12:p2]
    p = html.find('target="_blank"><b>', p2)
    p2 = html.find('</b></a></p>', p)
    title = html[p + 19:p2]
    # 点赞
    fabulou = reAuthorFabulou(html)
    # 类型
    if not tagContexts:
        tagContexts = []
    else:
        try:
            tagContexts.remove('<span style="color:#B00815;line-height:100%;">佚名</span>')
        except:
            print('报错')
    # 去掉\n换行
    shiwen = shiwen.replace('\n', '')

    sg = {'title': title, 'author': name, 'content': shiwen, "types": tagContexts, 'yiwen': yiwen,
          'zhushi': zhushi, 'shangxi': shangxi, 'fabulou': fabulou, 'poetryId': id}
    # print('诗文：'+shiwen)
    # print('类型：')
    # print(tagContexts)
    # print('译文：'+yiwenStr)
    # print('注释：'+zhushiStr)
    # print('赏析：'+shangxieStr)
    # print('参考资料：' + zhiliaoStr)
    return sg


def reAuthorPoetryNexUrl(html):
    # <a style="width:60px;" href="Default.aspx?p=311&c=">下一页</a>
    urls = reCompile(r'<a\sstyle="width:60px;"\shref="/(.*?)">下一页</a>', html)
    if urls:
        return urls[0]
    return ''


def reAuthorNexUrl(html):
    p = html.find('<div class="pages">', 0)
    p1 = html.find('</div>', p)
    if p == -1 or p1 == -1:
        return ''
    context = html[p + 19:p1]
    p = context.find('<a href="Default.aspx?p=', 0)
    if p == -1:
        return ''
    p = context.find('<a style="width:60px;" href="', p + 7)
    p1 = context.find('">下一页</a>', p)
    if p == -1 or p1 == -1:
        return ''
    return context[p + 29:p1]


def reNextUrlPag(httpUrl):
    authorUrls = reCompile(r'\?p=(.*?)&c=', httpUrl)
    if authorUrls:
        return authorUrls[0]
    return ''


# def reZSYWSX(html):
#     p = html.find('<p>', 0)
#     p1 = html.find('<div class="hr">', p)
#     # 判断是否只有赏析
#     if html.find('<div class="hr">', 0) < 10:
#         # 赏析
#         p = html.find('<div class="hr"></div>', 0)
#         p1 = html.find('<p style=" color:#919090;margin:0px; font-size:12px;line-height:160%;">', p)
#         sx = html[p + 22:p1]
#         return {'zw': '', 'yw': '', 'zs': '', 'sx': sx}
#     content = html[p:p1]
#     # 获取正文、注释、译文
#     contents = reCompile(r'<p>(.*?)</p>', content)
#     # 赏析
#     p = html.find('<div class="hr"></div>', p1 - 16)
#     p1 = html.find('<p style=" color:#919090;margin:0px; font-size:12px;line-height:160%;">', p)
#     sx = html[p + 22:p1]
#     # 解析正文、注释、译文
#     zw = ''
#     yw = ''
#     zs = ''
#     length = len(contents)
#     for i in range(0, length):
#         item = contents[i]
#         a = item.find('<br />')
#         # 正文
#         zw += item[0:a]
#         # 正文去掉正文以外的内容
#         p = zw.find('(')
#         if p != -1:
#             zw = zw[0:p]
#         # 译文
#         b = item.find('<span style="color:#993300;">', a)
#         if b != -1:
#             c = item.find('<', b + 30)
#             yw += item[b + 29:c]
#         else:
#             yw += 'N'
#         # 注释
#         b = item.find('<span style="color:#3333ff;">', a)
#         if b != -1:
#             c = item.find('<', b + 30)
#             zs += item[b + 29:c]
#         else:
#             zs += 'N'
#         # 添加分隔符
#         if i < length - 1:
#             zw += '<br />'
#             yw += '#'
#             zs += '#'
#     # 正文去掉\n
#     zw = zw.replace('\n', '')
#     # instanceContent =
#     # print('正文:' + zw)
#     # print('译文:' + yw)
#     # print('注释:' + zs)
#     # print('赏析:' + sx)
#     return {'zw': zw, 'yw': yw, 'zs': zs, 'sx': sx}

def reZSYWSX(zs, yw, sx):
    zsContent = ''
    ywContent = ''
    sxContent = ''
    p = 0
    count = 0
    # 注释
    while p > -1 and zs:
        p = zs.find('<br />', p)
        if p == -1:
            continue
        p1 = zs.find('<span style="color:#3333ff;">', p)
        if p1 != -1:
            p2 = zs.find('</span>', p1)
            zs2 = zs[p1 + 29:p2]
        else:
            p2 = zs.find('</p>', p)
            if p2 != -1:
                zs2 = zs[p + 6:p2]
            else:
                zs2 = zs[p + 6:]
        if not zs2:
            zs2 = 'N'
        if count > 0:
            zsContent += '#'
        zsContent += zs2
        count += 1
        if p2 != -1:
            p = p2
        else:
            p = p1
    # 译文
    p = 0
    count = 0
    while p > -1 and yw:
        p = yw.find('<span style="color:#993300;">', p)
        if p == -1:
            continue
        p1 = yw.find('</span>', p + 29)
        p2 = yw.find('<br />', p + 29)
        if p2 != -1 and p1 > p2:
            p1 = p2
        yw2 = yw[p + 29:p1]
        if count > 0:
            ywContent += '#'
        ywContent += yw2
        count += 1
        p = p1 + 6
    # 赏析
    if sx:
        p = sx.find('<div class="hr"></div>', 0)
        p1 = sx.find('<p style=" color:#919090;margin:0px; font-size:12px;line-height:160%;">', p + 22)
        if p != -1 and p1 != -1:
            sxContent = sx[p + 22:p1]
    ywContent = ywContent.replace('\n', '')
    zsContent = zsContent.replace('\n', '')
    sxContent = sxContent.replace('\n', '')
    # print('译文:' + ywContent)
    # print('注释:' + zsContent)
    # print('赏析:' + sxContent)
    return {'zs': zsContent, 'yw': ywContent, 'sx': sxContent}
    # ***********************************名句截取******************************************


def reMJ(html):
    # <a style="width:60px;" href="Default.aspx?p=311&c=">下一页</a>
    # mjs = reCompile(r'<div\sclass="[^\"]*"\sstyle="\smargin-top:12px;border-bottom:1px\sdashed #DAD9D1;\spadding-bottom:7px;">(.*?)"></div>', html)
    mjs = []  # reCompile(r'<div\s+[^>]*class="cont"[^>]*>(.*?)</div>', html)
    p = 0
    while p != -1:
        p = html.find('<div class="cont" style=" margin-top:12px;', p)
        p = html.find('<a style', p)
        p1 = html.find('</div>', p)
        if p != -1 and p1 != -1:
            mjs.append(html[p:p1])
            p = p1 + 6
        else:
            p = -1;

    if mjs:
        mjr = []
        for i in range(len(mjs)):
            item = mjs[i]
            a = item.find('href="/view_', 0)
            p = item.find('.aspx">', a)
            id = item[a + 12:p]
            p = item.find('.aspx">', 0)
            p1 = item.find('</a>', 0)
            content = item[p + 7:p1]
            p = item.find('.aspx">', p1)
            p1 = item.find('</a>', p)
            at = item[p + 7:p1]
            ats = at.split('《')
            mjr.append({'content':content, 'author': ats[0], 'title': ats[1].replace('》', ''), 'poetryId': id})
        return mjr
    return []
