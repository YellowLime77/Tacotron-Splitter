import time

class TimerException(Exception):
    """"""

class Timer:
    def __init__(self):
        self.start_time = None
    
    def start(self):
        if self.start_time is not None:
            raise TimerException("can't stop a stopped clock")
        
        self.start_time = time.perf_counter()
    
    def stop(self):
        if self.start_time is None:
            raise TimerException("it's still going, are you going to stop it?")
        
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        return elapsed_time