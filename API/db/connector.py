import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "mi_app")

client = MongoClient(MONGO_URI)
db_client = client[MONGO_DB]