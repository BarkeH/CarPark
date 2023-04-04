from pymongo import MongoClient
from bson import json_util
import json
import time
client = MongoClient('localhost',27017)
db = client.CarPark
collection = db.licencePlates

plate = input()

db_insert = { "plate":plate, "timeEntered": time.time(), "isACT":True}

output = collection.insert_one(db_insert)
