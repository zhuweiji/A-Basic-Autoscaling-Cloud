A simple implementation of a auto-scaling cloud computing cluster using the python Dask framework

There are three parts to the system:
1. A scheduler which partition works and assigns it to worker nodes
2. Worker Nodes which expose a HTTP endpoint and listen idly, and starts up if the scheduler requests
3. A task runner which connects to the scheduler to run programs.


To initialise this program, you will need one or more computers
One of them will run the scheduler
The others will run the workers (the machine running the worker can run the scheduler concurrently)

This will provide you with a computing cluster, which you can send tasks to via the Python SDK for Dask. An example is provided in the run_task.py file

To start, on all machines:
1. clone the repo via `git clone`
2. Install the dependencies for this project via either `pip install -r requirements.txt` or `poetry install`

On a worker machine:
3. Run poetry run `flask --app worker run` or `poetry run flask --app worker run`
4. Take note of the IP address and Port that the flask server is running on, and add it to the workers.toml file of the machine running the scheduler

On the scheduler machine:
5. Run `python3 run scheduler.py` or `poetry run python3 scheduler.py`

The cluster has been created!

On some machine, you can run `python3 run_task.py` or `poetry run python3
 run_task.py`