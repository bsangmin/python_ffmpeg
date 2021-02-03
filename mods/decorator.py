import time

class RunningTime:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        ss = time.time()
        self.func(*args, **kwargs)
        print(self.func.__name__, time.time() - ss)