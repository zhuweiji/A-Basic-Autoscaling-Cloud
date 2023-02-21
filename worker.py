from flask import Flask, request

app = Flask(__name__)


import logging
import subprocess
from pathlib import Path

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

def run_process(args: str):
    try:
        subprocess.run(args.split())
    except KeyboardInterrupt:
        log.info('Keyboard Interrupt: Terminating Program')
    except Exception:
        log.exception(args)
        
        


@app.route("/")
def hello_world():
    scheduler_address = request.args.get('address')
    log.info(f'registered request to start worker at remote scheduler {scheduler_address}')
    run_process(f'dask worker {scheduler_address}')
    return {'message': "Server started!"} , 201