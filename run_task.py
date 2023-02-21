import logging
from typing import Callable, Iterable

import dask.array as da
import dask.bag as db
import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client, Scheduler, Worker

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def long_running_function():
    i = 0
    for i in range(10**8):
        i += 1
    return i


if __name__ == "__main__":
    SCHEDULER_ADDRESS = 'tcp://192.168.1.140:51650'
    try:
        client = Client(SCHEDULER_ADDRESS)
        log.info('connected')
        
        big_data = [i for i in range(10**2)]
        log.info('data intialized')
        
        futures = [client.submit(long_running_function) for i in range(5)]
        
        
        log.info(futures)
        results = client.gather(futures)
        log.info(results)
        
    except KeyboardInterrupt:
        log.info('SIGKILL')
