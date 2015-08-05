

class Page(object):

    def __init__(self, url, category, path = '', rawContent = '', fileNameLabel = '', grabed = False, processed = False):
        self.path = path
        self.url = url
        self.category = category
        self.rawContent = rawContent
        self.fileNameLabel = fileNameLabel
        self.grabed = grabed
        self.processed = processed

    def __reduce__(self):
          return (self.__class__, (self.url, self.category, self.path, self.rawContent, self.fileNameLabel, self.grabed, self.processed))

class NavigationPage(Page):

    def __init__(self, url, category, articlePages = [], path = '', rawContent = '', fileNameLabel = '', grabed = False, processed = False):
        Page.__init__(self, url, category, path, rawContent, fileNameLabel, grabed, processed)
        self.fileNameLabel = url
        self.articlePages = articlePages
        pass

    def __reduce__(self):
          return (self.__class__, (self.url, self.category, self.articlePages, self.path, self.rawContent, self.fileNameLabel, self.grabed, self.processed))


class ArticlePage(Page):

    def __init__(self, url, title, category, path = '', rawContent = '', fileNameLabel = '', grabed = False, processed = False):
        Page.__init__(self, url, category, path, rawContent, fileNameLabel, grabed, processed)
        self.title = title
        self.content = ''
        self.fileNameLabel = self.title

    def __reduce__(self):
          return (self.__class__, (self.url, self.title, self.category, self.path, self.rawContent, self.fileNameLabel, self.grabed, self.processed))