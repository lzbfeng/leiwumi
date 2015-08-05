import os
import re
import time
import threading
import Queue
import pickle

from tools.myURLlib import getRawContent
from tools.myTools import Tools


class downloadThread(threading.Thread):
    def __init__(self, name, func, q):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name
        self.q = q
    def run(self):
        self.func(self.q)


class Crawel(object):

    def __init__(self, webSite):
        self.lock = threading.RLock()

        self.webSite = webSite

        self.baseURL = webSite.url
        self.rBase = webSite.rBase
        self.rNavigation = webSite.rNavigation
        self.rCategory =    webSite.rCategory
        self.urlsPath = os.path.join(webSite.path, 'allNavigationPagesURLs.txt')
        self.countOfThreads = webSite.countOfThreads

        #self.navigationComingFromParent = webSite.navigationComingFromParent
        self.crawelObjectsPath = os.path.join(self.webSite.path, 'crawelObjects.dat')

        if not os.path.exists(self.crawelObjectsPath):
            self.queue = Queue.Queue()
            self.queue.put(self.baseURL)
            self.navigations = {}
            self.categories = {}
            self.articles = {}
            self.allURLs = {}
            self.errorURLs = {}
        else:
            [self.queue, self.navigations, self.categories, self.articles, \
             self.allURLs, self.errorURLs] = self.loadCrawelObjects()

        self.countOfErrorTry = 10               #if error comes from Internet, then try again.
        self.sleepingTimesForGetJob = 5         #if queue is empty, then tray again after a sleep
        self.countOfTryingGetJob = 10
    
        pass

    def getURLsFromRawContent(self, rawContent, r1, parentURL):
        ret = []
        for item in re.findall(r"""href=["'](.*?)["']""", rawContent, re.S):
            item = item.strip()
            item = self.handleURL(item.strip(), parentURL, True)

            if item.startswith('h'):
                if re.findall(r1, item):
                    if not self.allURLs.has_key(item):
                        ret.append(item)
                        self.allURLs[item] = True

        return ret

    def downloadFunc(self, queue):
        selfKilling = False
        countOfWaitingForQueue = 0
        while not selfKilling:
            while not queue.empty():
                countOfWaitingForQueue = 0
                url = self.queue.get()
                print threading.currentThread().name + '\tdownload the url: %s'%url
                rawContent, errormsg = getRawContent(url)

                if rawContent == None and errormsg != None:
                    if not self.errorURLs.has_key(url):
                        self.errorURLs[url] = 1
                    else:
                        self.errorURLs[url] += 1
                    if self.errorURLs[url] <= self.countOfErrorTry:
                        self.queue.put(url)

                    print errormsg
                    continue
                #print rawContent
                urls = self.getURLsFromRawContent(rawContent, self.rBase, url)
                for url in urls:
                    if re.findall(self.rNavigation, url, re.S):
                        if not self.navigations.has_key(url):
                            self.navigations[url] = True
                            print url
                            queue.put(url)

                if len(self.navigations) % 20 == 0:
                    self.saveURLsAndLog()
                print "Queue's size is: \t%s"%str(self.queue.qsize()) + '\t' + \
                        "Navigations 's size is: \t%s"%str(len(self.navigations))
            countOfWaitingForQueue += 1
            print threading.currentThread().name + ' sleep ' + str(self.sleepingTimesForGetJob) + ' seconds for ' + str(countOfWaitingForQueue) + ' time.'
            time.sleep(self.sleepingTimesForGetJob)
            if countOfWaitingForQueue == self.countOfTryingGetJob:
                self.saveURLsAndLog()
                selfKilling = True

    def start(self):
        threadsList = []
        for i in xrange(self.countOfThreads):
            t = downloadThread("thread: " + str(i), func = self.downloadFunc, q = self.queue)
            t.start()
            threadsList.append(t)
        for t in threadsList:
            t.join()
        self.saveURLsAndLog()
        report = ""
        self.webSite.saveReport(report)

    def saveURLsAndLog(self):
        f = open(self.urlsPath, 'w+')
        for url in self.navigations.items():
            f.write(url[0] + '\n')
        f.close()
        #self.saveCrawelObjects()

        #self.webSite.dumpObjToFile(self, self.webSite.crawelLogPath)

    def getURLs(self):
        urls = []
        f = open(self.urlsPath, 'r+')
        for line in f.readlines():
            urls.append(line.strip())
        f.close()
        return urls

    def getNewURL(self, fatherURL, url):
        urlNew = ''
        items = fatherURL.split('/')
        count = len(items)
        index = 1
        for i in items:
            if index < count:
                urlNew += i + '/'
                index += 1
        if urlNew.endswith('/') and url.startswith('/'):
            urlNew = urlNew[:len(urlNew) - 1] + url
        elif urlNew.endswith('/') or url.startswith('/'):
            urlNew = urlNew + url
        else:
            urlNew = urlNew + '/' + url
        return urlNew

    def handleURL(self, url, parentURL, isParent = False):
        if "javascript" not in url and "http" not in url:
            if not isParent:
                s1 = self.baseURL
                s2 = url
                url = s1 + s2
                if s1.endswith('/') and s2.startswith('/'):
                    url = s1[:len(s1) - 1] + s2
            else:
                url = self.getNewURL(parentURL, url)

        return url

    def getCategoryOfURL(self, url):
        categoryName = None
        for item in re.findall(self.rCategory, url, re.S):
            if type(item) == list:
                categoryName = item[0] + '/' + item[1]
            elif type(item) == str:
                categoryName = item
            elif type(item) == tuple:
                if item[1] == '':
                    categoryName = item[0]
                else:
                    categoryName = item[0] + '/' + item[1]
        return categoryName

    def getCategoriesInfo(self):
        for url in self.getURLs():
            categoryName = self.getCategoryOfURL(url)
            if categoryName:
                if not self.categories.has_key(categoryName):
                    self.categories[categoryName] = []
                self.categories[categoryName].append(url)

        for item in self.categories.items():
            print item[0], len(item[1])

        return self.categories.items()

    def saveCrawelObjects(self):
        self.lock.acquire()
        toSave = [self.queue, self.navigations, self.categories, self.articles, self.allURLs, self.errorURLs]
        self.dumpObjToFile(toSave, self.crawelObjectsPath)
        self.lock.release()

    def loadCrawelObjects(self):
        objects = self.loadObjFromFile(self.crawelObjectsPath)
        return objects

    def dumpObjToFile(self, obj, filePath):
        try:
            savefile = open(filePath, "wb")
            pickle.dump(obj, savefile, True)
            savefile.close()
        except Exception, e:
            msg = u'An error occered when use dumpObjToFile function, and the error is ' + str(e) + '\n'
            Tools.printAndLog(msg, isError = True)

    def loadObjFromFile(self, filePath):
        try:
            readfile = open(filePath, "rb")
            ret = pickle.load(readfile)
            readfile.close()
            return ret
        except Exception, e:
            msg = 'An error occered when use loadObjFromFile function, and the error is ' + str(e) + '\n' + filePath
            Tools.printAndLog(msg, isError = True)
            return None



# if __name__ == "__main__":
#     webSite = WebSite("/home/lesshst/BFCrawel/nbweekly.ini")
#     crawel = Crawel(webSite)
#     crawel.start()
#     crawel.getCategoriesInfo()