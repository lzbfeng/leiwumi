import threading


class downloadThread(threading.Thread):
    def __init__(self, name, func, region):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name
        self.region = region
    def run(self):
        self.func(self.region)