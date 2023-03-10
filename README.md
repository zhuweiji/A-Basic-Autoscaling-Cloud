A simple implementation of a auto-scaling cloud computing cluster using the python Dask framework

### Conceptual Architecture

There are three parts to the system:
1. A Scheduler which partition works and assigns it to worker nodes
2. Worker Nodes which expose a HTTP endpoint and listen idly, and starts up if the scheduler requests
3. Any task runners which connect to the scheduler to run their python code on the cluster.

```mermaid
flowchart TD
    A[Task Runner] -->|New Computation| C{Scheduler}
    Z[Task Runner] -->|New Computation| C
    C -->|Subtask| D[fa:fa-computer Worker Node]
    C -->|Subtask| E[fa:fa-computer Worker Node]
    C -->|Subtask| F[fa:fa-computer Worker Node]
    C -->|Subtask| G[fa:fa-computer Worker Node]
```

The scheduler begins with zero or more worker nodes already instantiated. 

Uninstantiated worker nodes do not provide their computational power to the cluster. They are standby nodes that can be called on if the cluster needs to scale up. Each uninstantiated worker uses Flask to expose a HTTP endpoint, which the scheduler will ping if it requires the worker to spin up.

```mermaid
flowchart TD
    subgraph WaitingNodes
        B[idle_node]
        C[idle_node]
        D[idle_node]
        E[idle_node]
    end
    
    A{Scheduler} --> WaitingNodes --> WN[Worker Node] --> A
```

### Starting a Cluster

To initialise this program, you will need one or more computers: 
1. One of them will run the scheduler, 
2. The others will run the workers (the machine running the worker can run the scheduler concurrently) 

This will provide you with a computing cluster, which you can send tasks to via the Python SDK for Dask. An example is provided in the run_task.py file

To start, on all machines:
1. clone the repo via `git clone`
2. Install the dependencies for this project via either `pip install -r requirements.txt` or `poetry install`

On a worker machine: 
1. Run poetry run `flask --app worker run` or `poetry run flask --app worker run` 
2. Take note of the ip address and port that the flask server is running on, and add it to the workers.toml file of the machine running the scheduler
e.g. addresses = ["http://127.0.0.1:5000"]

On the scheduler machine: \
1. Run `python3 run scheduler.py` or `poetry run python3 scheduler.py`

The cluster has been created!

On some machine, you can run `python3 run_task.py` or `poetry run python3 run_task.py`
