from pymongo import MongoClient
from bson import json_util
import json
client = MongoClient('localhost',27017)
db = client.CarPark
collection = db.licencePlates
cars = collection.find()

car_list = []
for car in cars:
    car_list.append(car)

car_list = json.dumps(car_list, default=json_util.default)


print(car_list)
