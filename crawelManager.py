import re
import Queue
import multiprocessing
import threading

class CrawelManager(object):

    def __init__(self, mainURL):
        self.mainURL = mainURL
        self.categories = {}

        self.filterNavigationPages = r''
        self.filterBase = r''
        pass

    def getCategories(self):
        return self.categories

    def startCraweling(self, isMutiProcesses = False, isMutiThreads = True):
        if isMutiThreads and (not isMutiProcesses):
            self.startCrawelingMuThread()
        elif (not isMutiThreads) and (not isMutiProcesses):
            self.startCrawelingSingleThread()
        elif isMutiThreads and isMutiProcesses:
            self.startCrawelingMutiProcessesAndMutiThreads()

    def startCrawelingMuThread(self):
        pass

    def startCrawelingSingleThread(self):
        pass

    def startCrawelingMutiProcessesAndMutiThreads(self):
        pass

s1 = """
http://sports.cnr.cn/news/index_1.html      fsdfsadfsdf
sdf sdfsdfs http://finance.cnr.cn/2014jingji/yw/index_1.html
http://military.cnr.cn/zgjq/index_1.html
http://military.cnr.cn/gjjs/index_1.html    http://military.cnr.cn/gjjs/
http://military.cnr.cn/sdpl/index_1.html
http://military.cnr.cn/ycdj/index_1.html    http://military.cnr.cn/ycdj/
http://military.cnr.cn/zgjq/20150720/t20150720_519260796.html
"""

rCategory = r'http://((?:travel|health|edu|news|sports|tec|auto|military|finance|gongyi|ent|country))\.cnr\.cn/' + \
    '((?:news|2014jingji/yw|zgjq|gjjs|sdpl|ycdj|))/?(?:index_\d+.html|)'
rNavigation = r'http://(?:travel|health|edu|news|sports|tec|auto|military|finance|gongyi|ent|country)\.cnr\.cn/' + \
    '(?:news|2014jingji/yw|zgjq|gjjs|sdpl|ycdj|native|gjxw|comment|theory)/?(?:index_\d+.html|)'

rArticle = r'http://(?:travel|health|edu|news|sports|tec|auto|military|finance|gongyi|ent|country)\.cnr\.cn/' + \
    '(?:news|2014jingji/yw|zgjq|gjjs|sdpl|ycdj)/\d+/t\d+_?\d+.html'

#s1 = rawContent
#print s1

basePath = '/home/lesshst/crawel/cnr'
#categories = {'military/gjjs': ['http://military.cnr.cn/gjjs/index_1.html', 'http://military.cnr.cn/gjjs/']}
categories = {}
rNavigation = r'http://.*?\.cnr\.cn/.*?/(?:index_\d+.html|)'
rNavigation1 = r'http://(.*?)\.cnr\.cn/(.*?)/(?:index_\d+.html|)'

for item in re.findall(rNavigation, s1, re.S):
    for i in re.findall(rNavigation1, item, re.S):
        categoryName = i[0] + '/' + i[1]

        if not categories.has_key(categoryName):
            categories[categoryName] = []
        categories[categoryName].append(item)


for item in categories.items():
    print item[0], item[1]