# Getting started

## Prerequisites: Python 3

### Virtual environment
- Run "python3 -m venv /path/to/new/virtual/environment" (with you preferred path - fx. ~/.py-env/greenhouse_keeper)
- Run "source */path/to/new/virtual/environment/*bin/activate"

### Setup the app
- Run "python3 -m pip install -r requirements.txt"
- cd to "greenhouse_keeper"
- Run "python3 -m manage makemigrations"
- Run "python3 -m manage migrate"

### Run the app
- Run "python3 -m manage runserver"
- Go to http://127.0.0.1:8000/measurements/
