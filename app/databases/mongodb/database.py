from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DBNAME}?authSource={MONGO_DBNAME}"
mongo_client = MongoClient(uri)


mongo_database = mongo_client[MONGO_DBNAME]
