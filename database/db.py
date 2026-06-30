import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where()
)

db = client["blog_platform"]

users = db["users"]
posts = db["posts"]
comments = db["comments"]