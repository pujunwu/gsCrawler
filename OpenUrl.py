#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib.request
import socket

import WriteText  # 输出日志

# 如果网络请求失败，尝试重连次数
retryCount = 3


def url_open(url, count=0):
    try:
        socket.setdefaulttimeout(30)
        req = urllib.request.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        response = urllib.request.urlopen(url)
        html = response.read()
        return html
    except:
        if not url:
            print("HTTPError:Url为空，" + str(count))
            return ''
        count += 1
        if count <= retryCount:
            print('第' + str(count) + '次尝试重连')
            print(url)
            html1 = url_open(url, count)
            if html1:
                print('第' + str(count) + '次尝试重连，连接成功')
            else:
                print('第' + str(count) + '次尝试重连，连接失败')
            return html1
        else:
            print("HTTPError:" + url)
            WriteText.writeErrorLog('F:/python/gushiwen_web/ancientpoetry/', '当前第' + str(count) + '次请求失败：')
            WriteText.writeErrorLog('F:/python/gushiwen_web/ancientpoetry/', url + '\n')
            return ''
