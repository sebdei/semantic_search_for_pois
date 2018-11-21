Installation
------------

- make sure you installed pip and virtualenv
- cd into folder and create a virtualenv with

```
$ python3 -m venv venv
```

activate virtualenv with

```
$ source venv/bin/activate
```

install all dependencies
```
(venv)$ pip install -r requirements.txt
```
start main.py with
```
$ python3 main.py
```

store current dependencies in requirements.txt
```
pip freeze > requirements.txt
```

deactivate virtualenv later with

```
$ deactivate
```
