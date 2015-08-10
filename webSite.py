import shutil
import multiprocessing
import time

from category import *
from config import *
from tools.myTools import *
from crawel import Crawel


class WebSite(object):

    def __init__(self, websiteConfigPath):

        self.websiteConfigPath = websiteConfigPath
        config = Config(websiteConfigPath)
        self.config = config.getConfig()

        self.name = self.config["name"]
        self.url = self.config['url']
        self.path = os.path.join(self.config["basePath"], self.name)
        self.countOfProcesses = int(self.config["countOfProcesses"])
        self.countOfThreads = int(self.config["countOfThreads"])
        self.timeout = int(self.config["timeout"])
        self.reverse = self.config["reverse"]
        self.rBase = self.config["rBase"]
        self.rNavigation = self.config["rNavigation"]
        self.rCategory = self.config["rCategory"]
        self.keyCode = self.config["keyCode"]

        Tools(self.path)

        if self.config["isMutiProcesses"].lower() == "true":
            self.isMutiProcesses = True
        else:
            self.isMutiProcesses = False

        if self.config["isMutiThreads"].lower() == "true":
            self.isMutiThreads = True
        else:
            self.isMutiThreads = False

        self.initFilesAndDicts()

        self.crawel = Crawel(self)


    def __reduce__(self):
          return (self.__class__, (self.websiteConfigPath, ))

    def initFilesAndDicts(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        shutil.copyfile(self.websiteConfigPath, os.path.join(self.path, os.path.split(self.websiteConfigPath)[1]))


    def startGrab(self):
        report = multiprocessing.current_process().name + '\tProcesses: ' + str(self.countOfProcesses) + '\tThreads: ' + str(self.countOfThreads) + '\tTimeout: ' + str(self.timeout) + '\r\n'
        self.saveReport(report)

        #zero: start grabing navigation urls from the Internet
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nStart Grabing Navigation Urls.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)
        self.crawel.start()
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nEnd Grabing Navigation Urls.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)


        #first: start grabing navigation pages from the Internet
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nStart Grabing Navigation Pages.\t Time is %s.\r\n"%time.ctime()

        self.categoriesInfo = self.crawel.getCategoriesInfo()
        categories = []
        report = "Category Report"
        report += "\r\nCategory\t\t\tCount of Navigation Urls"
        for categoryInfo in self.categoriesInfo:
            #categoryInfo = (society, ("http://www.xinli001.com/society/p$$$/", "1-209", "[(i['href'], i['title']) for i in soup.findAll("a", attrs = {"class": "pic"})]"))
            categoryName = categoryInfo[0]
            naviURLs = categoryInfo[1]
            category = Category(categoryName, naviURLs, self.keyCode, self)
            categories.append(category)
            report += "\r\n" + categoryName + "\t\t\t" + str(len(naviURLs))

        self.saveReport(report)
        for category in categories:
            category.startGrabNaviPages(self.isMutiProcesses, self.isMutiThreads)
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nEnd Grabing Navigation Pages.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)


        #second: process navigation pages to get all including urls and get article pages
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nStart Processing Navigation Pages.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)
        for category in categories:
            category.startProcessNavigation()
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nEnd Processing Navigation Pages.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)


        #third: start grabing article pages from the Internet
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nStart Grabing Article Pages.\t Time is %s.\r\n"%time.ctime()
        self.saveReport(report)
        for category in categories:
            category.startGrabArticlePages(self.isMutiProcesses, self.isMutiThreads)
        report = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        report += "\r\nEnd Grabing Article Pages.\t Time is %s.\r\n\r\n\r\n"%time.ctime()
        self.saveReport(report)
        pass

    def saveReport(self, report):
        reportFile = open(os.path.join(self.path, 'report.txt'), 'a+')
        reportFile.write(report)
        reportFile.close()

    def showReport(self):
        reportFile = open(os.path.join(self.path, 'report.txt'), 'r')
        for line in reportFile.readlines():
            print line
        reportFile.close()

if __name__ == "__main__":

    webSite = WebSite("/home/lesshst/BFCrawel/nbweekly.ini")
    webSite.startGrab()
    webSite.showReport()