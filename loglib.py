class Logger:
    def __init__(self, DEBUG=True):
        self.DEBUG = DEBUG

    def log(self, s):
        if self.DEBUG:
            print(str(s))
