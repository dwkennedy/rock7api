This is a project to accept messages from Rock7, insert them into a 
database, then serve up KML.  Uses FastCGI, SQLAlchemy, and sqlite3

to enter the virtual environment,
```
    source /home/doug/fastapi/bin/activate
```

to start the asynchronous server gateway interface:
```
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

to create the initial blank database,
```
    python3 main.py
```

to reset database, erase the "sql_app.db" file.

### Comprehensive list of data payloads from rock7's test feature:

- One small step for a man one giant leap for mankind

- Hello! This is a test message from RockBLOCK!

- There are 10 types of people who understand binary

### Installation notes
```
pip install fastapi
pip install sqlalchemy
pip install simplekml
pip install uvicorn
```
