from pymongo import MongoClient
from bson import json_util
import json
client = MongoClient('localhost',27017)
db = client.CarPark
collection = db.licencePlates
cars = collection.find()

for car in cars:
    print(car)


if input("type something to remove an element: "):
    plate = input("licence Plate: ")
    
    deleteObject = {"plate":plate}

    collection.delete_one(deleteObject)

for car in collection.find():
    print(car)


