
class Config(object):

    def __init__(self, websiteConfigPath):
        configFile = open(websiteConfigPath, 'r')
        self.config = {}

        for line in configFile.readlines():
            items = line.strip().split("-=-")
            self.config[items[0].strip()] = items[1].strip()
        pass

    def __int__(self):
        pass

    def getConfig(self):
        return self.config