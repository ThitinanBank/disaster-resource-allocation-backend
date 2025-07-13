from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import AsyncMongoClient
import redis

load_dotenv(override=True)
uri = os.getenv("MONGODB_URI")
redis_host = os.getenv("REDIS_HOST")
redis_password = os.getenv("REDIS_PASSWORD")

# mongodb conection
client = AsyncMongoClient(uri, server_api=ServerApi('1'))
db = client["disaster_resource_allocation"]

# redis conection
# r = redis.Redis(host='localhost', port=6379, db=0)
r = redis.StrictRedis(host=redis_host,password=redis_password , port=6380, ssl=True)