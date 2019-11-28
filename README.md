# Collectors
Collectors are responsible for collecting data accross many different OSINT sources

### Initial setup

> **Note:** this is usefull for EVERY python project you are working on !

* Get the code on your local machine, because it's not in the cloud yet ...
```BASH
git clone git@github.com:opullence/collectors.git ; cd collectors
```

* Create a virtual environment and activate it (The recommanded way is to use python3-venv).
```BASH
python3 -m venv env ; source env/bin/activate
```

* You need to upgrade pip and setuptools (because i'm using `find_namespace_packages` in `setup.py`)

```BASH
pip install pip setuptools --upgrade
```

* Install dependencies and development tools using pip
```BASH
pip install -r requirements.txt
```

* Install git hooks (pre-commit)
```BASH
pre-commit install
```
* Setup the project services and command line tools (if necessary)

```BASH
python setup.py develop
```

### Collectors requirements
### Redis

* install redis using docker (requires docker)

```BASH
docker run -d --rm --name my-redis-container -p 6379:6379 redis
```

* install redis locally (on debian /ubuntu)

```BASH
sudo apt-get install redis-server
sudo systemctl start redis-server
redis-cli info
```

## Use the collectors API

#### Call the python code locally

Open a python shell and run the following commands
```python
>>> from opulence.collectors import app
>>> app.add(1, 2)
>>> app.reload_collectors()
>>> app.list_collectors()
```

#### Call the celery worker

Start a celery worker for the collectors app listening on the `collectors` and `default` queue.

```BASH
celery worker -A opulence.collectors.app --queues=collectors,default -l info
```

In a python shell, run the following commands

```python
>>> from opulence.collectors import app
>>> app.add.delay(1, 2)         # Async
>>> app.add.delay(1, 2).get()   # Sync
```

#### Call the celery worker remotly


```python
>>> from opulence.collectors import app
>>> from opulence.common.celery.utils import sync_call, async_call
>>> a = async_call(app.app, "opulence.collectors.app.add", 10, args=(1, 2)) #Async
>>> a.get()
>>> sync_call(app.app, "opulence.collectors.app.add", 10, args=(1, 2))      #Sync
>>> sync_call(app.app, "collectors:reload_collectors", 10)
>>> sync_call(app.app, "collectors:list_collectors", 10)
```


## Working example with nmap:

```

>>> from opulence.facts import Domain
>>> from opulence.facts import IPv4
>>> from opulence.collectors import app
Loaded: ['dummy collector', 'Hacker target', 'Nmap stealth scan', 'Nmap TCP connect', 'Profiler', 'exampleScriptModule']
>>> domain = Domain(fqdn="facebook.fr")
>>> ip = IPv4(address="216.58.204.99")
>>> res = app.execute_collector_by_name("Nmap TCP connect", ip)
ScriptCollector: launch command ('nmap', '-sT', '-oX', '-', '216.58.204.99')
>>> res.status
{'status': 40, 'code': 'Finished', 'error': None}
>>> res.output
[<opulence.facts.port.Port object at 0x7f21f5213710>, <opulence.facts.port.Port object at 0x7f21f5213828>]

```
