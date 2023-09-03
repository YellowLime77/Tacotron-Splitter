import time

class TimerException(Exception):
    """uh"""

class Timer:
    """Actually a stopwatch, not a timer"""

    def __init__(self):
        self.start_time = None
    
    def start(self):
        """On your mark... get set..."""

        # If this happens, uhohs
        if self.start_time is not None:
            raise TimerException("🤷")
        
        # Go!
        self.start_time = time.perf_counter()
    
    def stop(self) -> float:
        """Stop!"""

        # Uhohs again
        if self.start_time is None:
            raise TimerException("🤷")
        
        # Stops the timer
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        # and shows it to the user
        return elapsed_time