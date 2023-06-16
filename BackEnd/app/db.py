from flask import g
from pymongo import MongoClient

DATABASE_NAME="trackerDb"

# def get_db_instance():
#     client = MongoClient("mongodb://localhost:27017/")
#     return client["trackerDb"]
def get_db():
    if 'db' not in g:
        g.db = MongoClient("mongodb://localhost:27017/").trackerDb
    return g.db

def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()