from subprocess import *
from grabPagesManager import *
from page import *

class GrabNaviPagesManager(GrabPagesManager):
    """
    This class is used to grab the urls from navigation pages, and the pages are what we finally grab.
    """
    def __init__(self, navigationPages, category, otherConfig):
        GrabPagesManager.__init__(self, navigationPages, category, otherConfig)

    # def processPage(self, navigationPage):
    #
    #     #get urls from naviPage
    #     self.grabArticlePagesFromPage(navigationPage)
    #
    #     #save the memory
    #     navigationPage.rawContent = None

    def processNaviPages(self, pages):

        #this line is for saving the memory that sub process has occupied, because original all self.grabPages is not used in this sub process
        self.grabPages = None

        for page in pages:
            if not page.grabed:
                continue
            try:
                if not page.processed:
                    self.processNaviPage(page)
                    page.processed = True
                else:
                    print "page.articlePages", page.articlePages[0].title, page.articlePages[0].url, page.articlePages[0].grabed
                    pass
            except Exception, e:
                print "processNaviPages function error: " + str(e)

        self.saveProcessLog(pages)
        print multiprocessing.current_process().name + ". time is %s"%time.ctime()

    def processNaviPage(self, page):
        print multiprocessing.current_process().name + "-" + self.category.name + '\tprocess navigation page: ' + page.path
        # with open(page.path, "r") as f:
        #         page.rawContent = f.read()
        #         self.grabArticlePagesFromPage(page)

        self.grabArticlePagesFromPage(page)

    def processNaviPagesMutiProcesses(self):
        length = len(self.grabPages)

        if length == 0:
            print "processNaviPagesMutiProcesses.\tThere is no pages in %s"%self.category.name
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
            p = Process(name = 'lesshst-' + str(i + 1), target = self.processNaviPages, args = (self.grabPages[start:end],))
            p.start()
            listOfProcess.append(p)

        if end < length:
            #print a[i:length]
            p = Process(name = 'lesshst-' + str(i + 1), target = self.processNaviPages, args = (self.grabPages[i:length], ))
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
        # for page in grabPages:
        #     print page.url, page.grabed, page.processed

        self.saveProcessLog(self.grabPages)

        endTime = time.ctime()

        self.createReport(startTime, endTime)
        print len(self.grabPages)
        print 'all processes have been gone: %s'%time.ctime()

    def processNaviPagesSingleProcess(self):
        pass

    def startProcessingNaviPages(self, mutiProcess = True):
        if mutiProcess:
            self.processNaviPagesMutiProcesses()
        else:
            self.processNaviPagesSingleProcess()

    def grabArticlePagesFromPage(self, navigationPage):
        #content = navigationPage.rawContent
        #soup = BS(content)
        urlsAndTitles = self.getURLsAndTitles(navigationPage)
        for item in urlsAndTitles:
            url = item[0]
            title = item[1]
            print title + "\t" + url
            navigationPage.articlePages.append(ArticlePage(url, title, navigationPage.category))

    def handleURL(self, url):
        if "http" not in url:
            s1 = self.category.website.url
            s2 = url
            url = s1 + s2
            if s1.endswith('/') and s2.startswith('/'):
                url = s1[:len(s1) - 1] + s2

        return url

    def getURLsAndTitles(self, page):
        cmd = ["python", self.category.ProcessNavipagesCodeTemplatePath, page.path]
        pipe = Popen(cmd, stdin = PIPE, stdout = PIPE)

        ret = []
        for line in pipe.stdout.readlines():
            url, title = line.strip().split('$$$')
            url = self.handleURL(url)
            ret.append((url, title))

        return ret

    #overwrite this function to realize all kinds of customing grab ways
    # def getURLsAndTitles(self, soup):
    #     hrefInfo = self.category.hrefInfo
    #     [div, key, value] = hrefInfo.split('::')
    #     return [(i.a['href'], i.a.text) for i in soup.findAll(div, attrs={key: value})]
