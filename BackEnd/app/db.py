from pymongo import MongoClient

DATABASE_NAME="trackerDb"

def get_db_instance():
    client = MongoClient("mongodb://localhost:27017/")
    return client[DATABASE_NAME]