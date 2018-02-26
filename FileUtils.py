#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os  # 文件处理
import json  # json处理


def eachFile(filepath):
    fileNames = []
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        fileNames.append(allDir)
    return fileNames

def eachFile1(filepath):
    fileNames = []
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        fileNames.append(allDir)
    return fileNames

# 读取文件内容并打印
def readFile(filename):
    contents = []
    fopen = open(filename, 'r', encoding='UTF-8')  # r 代表read
    for eachLine in fopen:
        contents.append(eachLine)
    fopen.close()
    return contents


# 读取文件内容并打印
def readDirFile(filename):
    contents = ''
    fopen = open(filename, 'r', encoding='UTF-8')  # r 代表read
    for eachLine in fopen:
        contents += eachLine
    fopen.close()
    return contents


def getFileName(fileNames, id):
    if not fileNames or not id:
        return False
    for fileName in fileNames:
        if id == fileName.split('_')[0]:
            return True
    return False


if __name__ == '__main__':
    # downloadType()
    # testGs()
    # threadTest()
    fileNames = eachFile('F:\\python\\ancientpoetry2\\authors')
    # contents = readFile('F:/python/1_catalog.txt')
    contents = eachFile1('C:\\Users\\adminstrators\\Desktop\\古诗\古诗\\ancientpoetry\\authors')
    difference = list(set(contents).difference(set(fileNames)))
    print(difference)
    print(len(difference))


    # classContents = json.loads(contents)
    #
    # fileNames1 = []
    # for item in fileNames:
    #     fileNames1.append(int(item.split('_')[0]))
    #
    # classContents1 = []
    # for item in classContents:
    #     classContents1.append(int(item['id']))


    # items = []
    # item2 = ''
    # for item in classContents1:
    #     item2 = ''
    #     for item1 in fileNames1:
    #         if item == item1:
    #             item2 = item
    #             break
    #     if not item2:
    #         items.append(item)
    # print(items)
    # print([l for l in classContents1 if l in fileNames1])
    # set1 = set(classContents1)
    # set2 = set(fileNames1)
    # print (set1 != set2)

    # fileNames1 = set(fileNames1)
    # fileNames1 = [1,2,3,4,5,6,7]
    # classContents1 = [6,7,8,9]
    # difference = list(set(fileNames1).difference(set(classContents1)))
    # print(difference)
    # print([v for v in classContents1 if classContents1 not in fileNames1])

    # print (list(set(fileNames1).difference(set(classContents1))))  # b中有而a中没有的
    # dd = list(set(classContents1).intersection(set(fileNames1)))
    # print(len(dd))  # 交集

