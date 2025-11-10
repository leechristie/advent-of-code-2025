import time
import sys

__PRINT = print

__all__ = ['print']

# wrapper for print to default to STDERR
def print(*args, sep=' ', end='\n', file=sys.stderr):
    time.sleep(0.005)
    __PRINT(*args, sep=sep, end=end, file=file, flush=True)
    time.sleep(0.005)
