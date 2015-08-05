from tools.myURLlib import getRawContent
from webSite import *
class BFCrawel(object):

    def __init__(self, webSite):
        self.path = webSite.path
        self.countOfProcesses = webSite.countOfProcesses
        self.countOfThreads = webSite.countOfThreads


    def __reduce__(self):
        return (self.__class__, (self.countOfProcesses,self.countOfThreads, ))

    def startCrawel(self):
        pass
