
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

import httpx
import tomli
from dask.distributed import Scheduler, Worker

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


worker_config_file = Path(__file__).parent/'workers.toml'
worker_config = tomli.loads(worker_config_file.read_text())


@dataclass
class WorkerNode:
    address:str
    started:bool=False
    
    async def start(self, scheduler_address:str):
        log.info(f'starting new worker at address {self.address}')
        async with httpx.AsyncClient() as client:
            r = await client.get(self.address, params={'address':scheduler_address})
            created = r.status_code == 201
            
            self.started = created
            if not created:
                log.warning('unexpected response when trying to start worker')
                log.warning(r.json())
            
            return created
    

possible_workers: List[WorkerNode] = [WorkerNode(address=i) for i in worker_config['addresses']]


async def start_worker(scheduler_address:str):
    available_workers = [i for i in possible_workers if not i.started]
    if not available_workers:
        log.info('Tried to start new worker but none were available')
    await available_workers.pop().start(scheduler_address)
    
async def monitor_scheduler(s:Scheduler, interval_seconds:int=2):
    while True:
        if s.adaptive_target() > len(s.workers):
            result = await start_worker(s.address)
            
        
        await asyncio.sleep(interval_seconds)


async def main():
    log.info(f'started program with uninitialised workers {possible_workers}')
    
    s = Scheduler(port=51650)        # scheduler created, but not yet running
    s = await s                      # the scheduler is running
    asyncio.Task(monitor_scheduler(s)) # create a task to monitor the scheduler and run some custom functions if required
        
    await s.finished()     # wait until the scheduler closes


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()