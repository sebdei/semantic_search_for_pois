# Installation

- make sure you installed pip and virtualenv
- cd into folder and create a virtualenv with

```sh
python3 -m venv venv
```

or create the venv as follows if errors occur

```sh
virtualenv venv
```

activate virtualenv with

```sh
source venv/bin/activate
```

install all dependencies

```sh
pip install -r requirements.txt
```

start main.py with

```sh
python3 main.py
```

store current dependencies in requirements.txt

```sh
pip freeze > requirements.txt
```

deactivate virtualenv later with

```sh
deactivate
```
