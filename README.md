# Treehouse-Python-Techdegree-Project-12: "Social Team Builder"

# Description

A Django app allowing users to (1) create profiles listing their skills and work experience,
(2) post work projects and associated positions that need filling, and (3) apply for open positions
on other projects.

# Python

Version 3.6.4

# Installing

- Download files.
- In the project directory install virtual environment: `python -m venv env`
- Activate virtual environment: in Windows `env\scripts\activate` or Posix `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

# Database setup

- Run `python manage.py makemigrations`
- Then run `python manage.py migrate`
- Load initial data: `python manage.py loaddata initial_data.json`

# Running

- Start server: `python manage.py runserver 0.0.0.0:8000`
