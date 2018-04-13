# Closure table using Asyncio + PostgreSQL

Backend provides a simple API for managing tree-based comments.

## Deploy (Ubuntu 16.04 LTS)

1. **Clone repo**

    ```bash
    sudo apt update
    sudo apt install git
    git clone https://github.com/vyacheslav-bezborodov/closure-table
    cd closure-table/
    ```

2. **Set up Python**

    ```bash
    sudo apt update
    sudo apt install python3-pip
    sudo -H pip3 install pipenv
    pipenv install --dev
    pipenv shell
    ```

3. **Set up PostgreSQL**

    ```bash
    sudo apt update
    sudo apt install postgresql
    
    # create user and db
    sudo su postgres
    createuser —pwprompt closureuser    # and type closurepass
    createdb —owner=closureuser closuredb
    exit
    
    # apply migrations
    python apps/auth/db/manage.py version_control
    python apps/auth/db/manage.py upgrade
    python apps/comments/db/manage.py version_control
    python apps/comments/db/manage.py upgrade
    ```

## Run server

Activate the shell and run the script.

```bash
pipenv shell
python runserver.py
```

Then open <http://localhost:8080/api/doc> in your favourite browser.

Use **admin/admin** as a superuser email and password to sign in. 
