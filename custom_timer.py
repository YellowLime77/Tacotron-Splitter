import time

class TimerException(Exception):
    """uh"""

class Timer:
    """A stopwatch down to the 0.000000000001 second, just for you"""

    def __init__(self):
        self.start_time = None
    
    def start(self):
        """ON YOUR MARK... GET SET..."""

        # If this happens, uhohs
        if self.start_time is not None:
            raise TimerException("🤷")
        
        #GO GO GO GO GOOOOO!!!
        self.start_time = time.perf_counter()
    
    def stop(self) -> float:
        """FINISH!"""

        # Uhohs again
        if self.start_time is None:
            raise TimerException("🤷🤷")
        
        # This tells me how bad my pc performs
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        # and shows it to me
        return elapsed_time