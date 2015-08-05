import time
from multiprocessing import Process
import multiprocessing

from tools.myThread import downloadThread
from tools.myURLlib import getRawContent
from tools.myFileOperation import *


class GrabPagesManager(object):
    #grab pages and download them from pages
    def __init__(self, pages, category, otherConfig, threadList = []):
        self.grabPages = pages
        self.category = category
        self.countOfProcesses = category.website.countOfProcesses
        self.countOfThreads = category.website.countOfThreads
        self.categoryName = category.name
        self.countOfGrabedPages = 0
        self.timeout = category.website.timeout
        self.otherConfig = otherConfig
        self.path = otherConfig['path']
        self.gradedLogPath = os.path.join(self.path, multiprocessing.current_process().name + ".dat")

        self.logPath = os.path.join(self.path, 'log.txt')

        self.threadList = threadList
        self.lock = threading.Lock()
        self.initFilesAndDicts()

    def initFilesAndDicts(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if not os.path.exists(self.gradedLogPath):
            dumpObjToFile([], self.gradedLogPath)
        else:
            grabPages = loadObjFromFile(self.gradedLogPath)
            if len(grabPages) != 0:
                dic = {}
                temp = []
                for grabPage in grabPages:
                    #if grabPage.grabed:
                    if not dic.has_key(grabPage.url):
                        dic[grabPage.url] = grabPage

                for page in self.grabPages:
                    if not dic.has_key(page.url):
                        temp.append(page)
                for page in temp:
                    grabPages.append(page)
                self.grabPages = grabPages
                self.countOfGrabedPages = len(dic.items())

    def startMiningMuThread(self):
        length = len(self.grabPages)
        step = int(float(length) / self.countOfThreads + 1)

        if length == 0:
            print "There is no pages."
            return

        startTime = time.ctime()
        print 'Start all thread: %s'%time.ctime()
        for i in xrange(0, length, step):
            start = i
            if i + step > length:
                end = length
            else:
                end = i + step
            #print a[start:end]
            thread = downloadThread(self.categoryName + ':' + str(i) + '-' + str(i + step), self.grabPagesFunc, self.grabPages[start:end])
            thread.start()
            self.threadList.append(thread)

        if end < length:
            #print a[i:length]
            thread = downloadThread(self.categoryName + ':' + str(i) + '-' + str(i + step), self.grabPagesFunc, self.grabPages[i:length])
            thread.start()
            self.threadList.append(thread)
        print 'All threads have been started: %s'%time.ctime()
        for thread in self.threadList:
            print "Start this thread:\t" + thread.name + '\tat time: %s'%time.ctime()
            thread.join()
            print "End this thread:\t" + thread.name + '\tat time: %s'%time.ctime()

        print 'All threads have been gone: %s'%time.ctime()

        endTime = time.ctime()

        self.createReport(startTime, endTime)

        pass

    def grabPagesFunc(self, pages):
        print threading.currentThread().name
        for page in pages:
            #print threading.currentThread().name + 'will grab the url: ' + page.url
            self.grabPage(page)
        self.saveGrabedLog()
        print threading.currentThread().name + " has grabed all pages"
        pass

    def startMiningSingleThread(self):
        for page in self.grabPages:
            self.grabPage(page)
        pass

    def startMining(self, isMuProcesses = False, isMuThreads = True):
        if isMuThreads and (not isMuProcesses):
            self.startMiningMuThread()
        elif (not isMuThreads) and (not isMuProcesses):
            self.startMiningSingleThread()
        elif isMuThreads and isMuProcesses:
            self.startMiningMutiProcessesAndMutiThreads()

    def grabPage(self, page):

        if page.grabed:
            #print 'this page has been grabed: ' + page.path
            return

        url = page.url
        msg = threading.currentThread().name + '\n'
        msg += 'start download the url: ' + url + '\n'
        msg += "start time is : %s"%time.ctime() + '\n'

        msg += 'internet: %s.\t'%time.ctime() + '\n'

        page.rawContent, errormsg = getRawContent(url, self.timeout)

        if page.rawContent == None and errormsg != None:
            errormsg += '\tTime is: %s.\t'%time.ctime() + 'The url: %s\t'%url + 'The count of grabed pages: %s\t'%str(self.countOfGrabedPages) + '\n'
            self.printAndLog(errormsg, True)
            return
        #change strategy, because processing page data is cpu intensive.
        #we just save the page raw content and process after a while

        self.lock.acquire()
        self.countOfGrabedPages += 1
        self.lock.release()
        #Tools.mylock.release()

        self.savePage(page)
        page.grabed = True

        if self.countOfGrabedPages % 25 == 0:
            self.saveGrabedLog()

        msg += "end time is : %s"%time.ctime() + '\n'
        msg += 'the number of grabed pages is: ' + str(self.countOfGrabedPages) + '\n\n'
        self.printAndLog(msg)

    def printAndLog(self, msg, isError = False):
        print msg
        self.lock.acquire()
        try:
            if not isError:
                logFile = open(self.logPath, 'a+')
                logFile.write(msg)
                logFile.close()
            else:
                errorlogFile = open(self.logPath, 'a+')
                errorlogFile.write(msg)
                errorlogFile.close()
        except Exception, e:
            print str(e)
            self.lock.release()
        self.lock.release()
        if isError:
            Tools.printAndLog(msg, isError)

    def getPages(self):
        return self.grabPages

    def saveGrabedLog(self):
        print "saveGrabedLog: " + str(self.countOfGrabedPages) + '\t' + self.gradedLogPath
        #Tools.mylock.acquire()
        filePath = os.path.join(self.path, multiprocessing.current_process().name + ".dat")
        self.lock.acquire()
        dumpObjToFile(self.grabPages, filePath)
        self.lock.release()
        #Tools.mylock.release()

    #this functon should be overwriten to realize all kinds of function, such as:
    #1. contract the urls from navigation page and save this page
    #2. save the article page
    def processPage(self, page):
        pass

    def savePage(self, page):
        #000023_fileNameLabel.html
        articleName = Tools.replaceSpecialCharacters(page.fileNameLabel) + '.html'
        page.path = os.path.join(self.path, articleName)
        saveFile = open(page.path, 'w+')
        saveFile.write(page.rawContent)
        saveFile.close()
        #save the memory
        page.rawContent = None


    def grabPagesFuncForMutiProcesses(self, pages):
        #in sub process, all the function and data from main process can be copied to sub process, in other words, sub process has same function and data as main process,
        #but sub process has some more parameters coming from main process, which don't have same address in memory as main process.
        #this line is used for changing the size of self.grabPages in the sub process, because in sub process only part of all self.grabPages should be grabed by a single sub process.
        self.grabPages = pages

        self.startMining()

    def startMiningMutiProcessesAndMutiThreads(self):
        length = len(self.grabPages)

        if length == 0:
            print "There is no pages."
            return

        step = int(float(length) / self.countOfProcesses + 1)
        listOfProcess = []
        startTime = time.ctime()
        print 'start all process: %s'%time.ctime()
        for i in xrange(0, length, step):
            start = i
            if i + step > length:
                end = length
            else:
                end = i + step
            #print a[start:end]
            p = Process(name = 'lesshst-' + str(i + 1), target = self.grabPagesFuncForMutiProcesses, args = (self.grabPages[start:end], ))
            p.start()
            listOfProcess.append(p)

        if end < length:
            #print a[i:length]
            p = Process(name = 'lesshst-' + str(i + 1), target = self.grabPagesFuncForMutiProcesses, args = (self.grabPages[i:length], ))
            p.start()
            listOfProcess.append(p)

        print 'all processes have been started: %s'%time.ctime()
        for process in listOfProcess:
            print "join function: start this process: " + process.name + ' at time: %s'%time.ctime()
            process.join()
            print "join function: end this process: " + process.name + ' at time: %s'%time.ctime()

        self.grabPages = []
        for process in listOfProcess:
            filePath = os.path.join(self.path, process.name + ".dat")
            readfile = open(filePath, "rb")
            ret = pickle.load(readfile)
            readfile.close()
            os.remove(filePath)

            self.grabPages.extend(ret)

        self.saveProcessLog(self.grabPages)

        endTime = time.ctime()
        self.createReport(startTime, endTime)

        print len(self.grabPages)
        print 'all processes have been gone: %s'%time.ctime()

    def createReport(self, startTime, endTime):

        if multiprocessing.current_process().name != 'MainProcess':
            return

        countOfGrabed = 0
        countOfProcessed = 0
        for page in self.grabPages:
            if page.grabed:
                countOfGrabed += 1
            if page.processed:
                countOfProcessed += 1
        countTotal = len(self.grabPages)

        report = ''
        report += '----------------------------------------------------------------------------\r\n'
        #report += "Process's name:\t" + multiprocessing.current_process().name
        report += 'Category:\t' + self.category.name + '\t' + self.path.split('/')[-1:][0] + '\r\n'
        report += 'Total is:\t' + str(countTotal) + '\r\n'
        report += 'Count of grabed: \t' + str(countOfGrabed) + '------------' + str(float(countOfGrabed)/countTotal * 100) + '%' + '\r\n'
        report += 'Count of processed:\t' + str(countOfProcessed) + '------------' + str(float(countOfProcessed)/countTotal * 100) + '%' + '\r\n'
        report += 'Start time is: \t%s'%startTime + '\r\n' + 'End time is: %s'%endTime + '\r\n'
        report += '----------------------------------------------------------------------------\r\n'

        self.printAndLog(report)

        self.category.website.saveReport(report)

    def saveProcessLog(self, pages):
        filePath = os.path.join(self.path, multiprocessing.current_process().name + ".dat")
        savefile = open(filePath, "wb")
        pickle.dump(pages, savefile, True)
        savefile.close()