from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["blog_platform"]

users = db["users"]
posts = db["posts"]
comments = db["comments"]