# -*- coding: utf-8 -*-
#===============================================================================
# 目的：为其他的模块提供一些通用的工具
# 作者：terry_feng
# 时间：2014.4.23-8.28
#===============================================================================
import threading
import os
import md5


class Tools():
    #线程锁
    mylock = threading.RLock()
    basePath = ''
    logFilePath = ''
    errorlogFilePath = ''
    def __init__(self, basePath):
        Tools.basePath = basePath
        if not os.path.exists(basePath):
            os.makedirs(basePath)

        Tools.logFilePath = os.path.join(basePath, 'log.txt')
        Tools.errorlogFilePath = os.path.join(basePath, 'errorLog.txt')
        print 'tools class'
    @staticmethod
    def getMD5(info):
        key = md5.new(info)
        return key.digest()

    @staticmethod
    def printAndLog(msg, isError = False):
            print msg
            #Tools.mylock.acquire()
            if not isError:
                logFile = open(Tools.logFilePath, 'a+')
                logFile.write(msg)
                logFile.close()
            else:
                errorlogFile = open(Tools.errorlogFilePath, 'a+')
                errorlogFile.write(msg)
                errorlogFile.close()
            #Tools.mylock.release()
    @staticmethod
    def replaceSpecialCharacters(string, replaceCharacter = ''):

        colon = '%c'%58
        forwardSlash = '%c'%47
        backSlash = '%c'%92
        asterisk = '%c'%42
        questionMask = '%c'%63
        doubleQuote = '%c'%34
        greaterThanSign = '%c'%62
        lessThanSign = '%c'%60
        shugang = '%c'%124

        charSet = [colon, forwardSlash, backSlash, asterisk, questionMask, doubleQuote, greaterThanSign, lessThanSign, shugang]
        for i in charSet:
            string = string.replace(i,replaceCharacter)
        return string
    @staticmethod
    def getSotedListFromDic(dic, reverse = False):
        return sorted(dic.items(), key = lambda dic: dic[1][0:6])
if __name__ == '__main__':
#     myConfig = {}
#     myConfig['basePath'] = 'E:\\MySpace\\Crawel\\Alibuybuy'
#     myConfig['logFilePath'] = 'log.txt'
#     myConfig['errorlogFilePath'] = 'errorlog.txt'
#     Tools.setConfig(myConfig)
#     for i in range(100):
#         if i % 2 == 0:
#             msg = str(i) + ' is a even number.\n'
#             Tools.printAndLog(msg, error = False)
#         else:
#             msg = str(i) + ' is a odd number.\n'
#             Tools.printAndLog(msg, error = True)
    print Tools.replaceSpecialCharacters('000009_【WISE Talk-世界在发生什么】李天放：从硅谷到中国，创业者的心态正在改变.html000004_润物细无声：伟大的品牌化于无形.htmlsdfsd/dfs、：了解啊地方:]\[?')
    print Tools.getMD5('lizhibo')
    print str(Tools.getMD5('lizhibo'))
