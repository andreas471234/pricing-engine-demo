# Pricing Engine

## Overview

This is django web app that is used to calculate price of

### Install Python 3.11.5 and other dependencies

- <https://www.python.org/downloads/release/python-3115/>
- Install the python package
  - `macOS 64-bit universal2 installer`
- Create python virtual environtment
  - `virtualenv --python=python3.11 venv`
- Go inside the virtual environtment
  - `source venv/bin/activate`
- Run following command in project directory

    ```bash
      pip3 install -r requirements.txt
    ```

### Setting up database

- Install using dmg
  - <https://dev.mysql.com/downloads/mysql/>
- Run following command in mysql
  - `CREATE DATABASE pricingapp`
- Run the command on project directory

    ```bash
      python3 manage.py makemigrations
      python3 manage.py migrate
    ```

### Running the server

- Run following command in project directory
  - `python3 manage.py runserver`

### API Docs

- link for the API Docs
  - <https://documenter.getpostman.com/view/32451372/2s9YsT68DW>
