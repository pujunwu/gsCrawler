# coding=utf-8 ##以utf-8编码储存中文字符
# -*- coding: UTF-8 -*-
# !/usr/bin/python

import os  # 文件处理
import json  # json处理
import threading  # 多线程


# r：只读（缺省。如果文件不存在，则抛出错误）
# w：只写（如果文件不存在，则自动创建文件）
# a：附加到文件末尾
# r+：读写
# 如果需要以二进制方式打开文件，需要在mode后面加上字符”b”，比如”rb””wb”等

# python读取文件内容f.read(size)
# 参数size表示读取的数量，可以省略。如果省略size参数，则表示读取文件所有内容
# f.readline()读取文件一行的内容 f.readlines()读取所有的行到数组里面[line1,line2,…lineN]

# 输出文字
def writeTextFile(path, text, author):
    if not path:
        return False
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    dirs = os.path.dirname(path)  # 获取当前路径的目录
    if not os.path.exists(dirs):  # 目录不存在就创建
        os.makedirs(dirs)
    out = open(path, "a+", encoding='UTF-8')
    if out:
        r = outText(out, text)
        out.close()
        if not r:
            filename = path.split('/')[-1]  # 文件名称
            d = writeTextEncodingFile(author, dirs, filename, text, 'BG2312')
            mutex.release()  # 释放锁
            return d
        else:
            mutex.release()  # 释放锁
            return True
    else:
        mutex.release()  # 释放锁
        return False


# 输出文字
def writeTextEncodingFile(author, dir, fileName, text, encoding):
    names = fileName.split('.')
    path = dir + "/" + names[0] + '_1.' + names[1]
    out = open(path, "a+", encoding=encoding)
    if out:
        r = outText(out, text)
        out.close()
        if not r:
            print(author)
            print(text)
            return False
        else:
            return True
    else:
        return False


# 输出文字
def outText(out, data, check=''):
    try:
        if not check:
            out.write(data)
        else:
            out.write(str(data.encode(check, 'ignore').encode("UTF-8")))
        return True
    except UnicodeEncodeError as e:
        print(data)
        return False
    except AttributeError as e:
        return True


# 输出文字
def writeText(path, data):
    if not path:
        path = os.getcwd() + "/sr.txt"
    # 判断目录是否存在，如果不存在就创建
    dirExists(path)
    if data and len(data):
        # out = open(path, "a+", encoding='UTF-8')
        out = open(path, "a+")
        if out:
            r = outText(out, data)
            if not r:
                r = outText(out, data, "GBK")
            out.close()
            return path
        else:
            return ''


# 输出目录
def writeCatalog(catalog, rootPath):
    jsonCatalog = json.dumps(catalog, ensure_ascii=False, indent=None)
    writeCatalogJson(',' + jsonCatalog, rootPath)


# 输出目录Json
def writeCatalogJson(catalogJson, rootPath):
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    writeText(rootPath + '/1_catalog.txt', catalogJson + '\n')
    mutex.release()  # 释放锁


# 输出诗歌
def writePoetry(poetry, path, authorName):
    jsonPoetry = json.dumps(poetry, ensure_ascii=False, indent=None)
    writePoetryJson(',' + jsonPoetry, path, authorName)


# 输出诗歌
def writePoetryJson(poetryJson, path, authorName):
    writeTextFile(path, poetryJson + '\n', authorName)


# 输出保存日志
def writeLog(rootSave, log):
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    writeText(rootSave + '/1_log.txt', log + '\n')
    mutex.release()  # 释放锁


# 输出保存日志
def writeErrorLog(rootSave, log):
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    writeText(rootSave + '1_error_log.txt', log + '\n')
    mutex.release()  # 释放锁

# 输出保存日志
def writeDirs(rootSave, log):
    mutex = threading.Lock()  # 创建锁
    mutex.acquire()  # 使用锁
    writeText(rootSave + '1_dir_log.txt', log + '\n')
    mutex.release()  # 释放锁

# 输出图片 输出成功返回图片名称，反之返回''
def saveImgs(folder, img_addrs, imageFile):
    # 如果文件为空不输出
    if not imageFile:
        return ''
    # 判断目录是否存在，如果不存在就创建
    dirExists(folder)
    filename = img_addrs.split('/')[-1]
    imagef = open(folder + filename, 'wb')
    if imagef:
        try:
            imagef.write(imageFile)
        except:
            print("img_addrs:" + img_addrs)
        finally:
            imagef.close()
        return filename
    else:
        return ''


# 判断目录是否存在，如果不存在就创建
def dirExists(path):
    dirs = os.path.dirname(path)  # 获取当前路径的目录
    if not os.path.exists(dirs):
        os.makedirs(dirs)
