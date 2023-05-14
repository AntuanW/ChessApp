from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv('.env')

username: str = os.getenv("MONGO_USERNAME")
password: str = os.getenv("MONGO_PASSWORD")

class MongoConnection:
    def __init__(self):
        self.db = None
        self.users = None
        self.client = None
        self.uri = f"mongodb+srv://{username}:{password}@cluster0.rsuv7ei.mongodb.net/?retryWrites=true&w=majority"

    def initMongoConnection(self):
        self.client = MongoClient(self.uri)
        self.db = self.client["chess-application"]
        self.users = self.db["users"]
