import string
from multiprocessing import Process
import multiprocessing
from BeautifulSoup import BeautifulSoup as BS          # HTML
from grabPagesManager import *

class GrabArticlePagesManager(GrabPagesManager):
    """
    This class is used to grab the urls from navigation pages, and the pages is what we finally grab.
    """
    def __init__(self, naviPages, category, otherConfig):
        if naviPages == None:
            print "There is no pages. naviPages is None."
        else:
            if len(naviPages) == 0:
                print "There is no pages."
        self.naviPages = naviPages
        self.articlePages = self.getArticlePages()

        GrabPagesManager.__init__(self, self.articlePages, category, otherConfig)

        pass

    def getArticlePages(self):
        articlePages = []
        for naviPage in self.naviPages:
            articlePages.extend(naviPage.articlePages)
        return articlePages

