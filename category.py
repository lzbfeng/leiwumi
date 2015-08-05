import os

from page import *
from grabNaviPagesManager import GrabNaviPagesManager
from grabArticlePagesManager import GrabArticlePagesManager
from tools.myTools import Tools


class Category(object):
    def __init__(self, name, naviURLs, keycode, website):
        self.path = os.path.join(website.path, name)
        self.name = name
        self.website = website
        self.naviURLs = naviURLs
        self.keycode = keycode

        self.ProcessNavipagesCodeTemplatePath = os.path.join(self.path, "ProcessNavipagesCodeTemplate.py")
        BSTemplateCode = """
import sys
import os
import re
from BeautifulSoup import BeautifulSoup as BS

if __name__ == "__main__":

    path = sys.argv[1]
    f = open(path, 'r+')
    rawContent = f.read()
    f.close()

    if re.search(r'charset.*?=.*?gb2312', rawContent, re.I):
        rawContent = rawContent.decode('gbk')

    soup = BS(rawContent)

    items = """ + self.keycode + """
    for item in items:
        print item[0] + "$$$" + item[1]
"""
        ReTemplateCode = """
import sys
import re

if __name__ == "__main__":

    path = sys.argv[1]

    f = open(path, 'r+')
    rawContent = f.read()
    f.close()

    if re.search(r'charset.*?=.*?gb2312', rawContent, re.I):
        rawContent = rawContent.decode('gbk')

    pattern = re.compile(""" + self.keycode + """, re.S)

    for item in re.findall(pattern, rawContent):
        print item[0] + "$$$" + item[1]
"""

        if self.keycode.startswith('['):
            self.ProcessNavipagesCodeTemplate = BSTemplateCode
        else:
            self.ProcessNavipagesCodeTemplate = ReTemplateCode

        self.initFilesAndDicts()

    def __reduce__(self):
          return (self.__class__, (self.name, self.naviURLs, self.keycode, self.website))

    def initFilesAndDicts(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        f = open(self.ProcessNavipagesCodeTemplatePath, 'w+')
        f.write(self.ProcessNavipagesCodeTemplate)
        f.close()

    def startGrabNaviPages(self, isMutiProcesses, isMutiThreads):
        #main
        self.navigationPages = self.getNavigationPages()
        self.naviPagesMiningManager = GrabNaviPagesManager(self.navigationPages, self, {"path":os.path.join(self.path, "navigationPages")})

        #start mine navigation pages and get article pages that should be grabed
        self.naviPagesMiningManager.startMining(isMutiProcesses, isMutiThreads)

    def startProcessNavigation(self, isMutiProcesses = True):
        self.naviPagesMiningManager.startProcessingNaviPages(isMutiProcesses)

    def startGrabArticlePages(self, isMutiProcesses, isMutiThreads):
        self.articlePages = self.naviPagesMiningManager.getPages()
        self.articlePagesMiningManager = GrabArticlePagesManager(self.articlePages, self, {"path":os.path.join(self.path, "articlePages")})
        self.articlePagesMiningManager.startMining(isMutiProcesses, isMutiThreads)

    def getNavigationPages(self):
        naviPages = []
        for url in self.naviURLs:
            try:
                naviPages.append(NavigationPage(url, self, [], '', '', '', False, False))
            except Exception, e:
                Tools.printAndLog("Category.getNavigationPages has an error is: " + str(e), isError = True)

        return naviPages

