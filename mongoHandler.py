from pymongo import MongoClient 

client = MongoClient('mongodb://root:password@localhost:27017/')
db = client.licence
collection = db.licence

def deleteCarByPlate(plate):
    deleteObject = {"plate":plate}
    collection.delete_one(deleteObject)

def getTimeEntered(plate):
    findObject = {"plate":plate}
    car = collection.find_one(findObject)
    return car["plate"]

def getWholeCar(plate):
    findObject = {"plate":plate}
    car = collection.find_one(findObject)
    return car

def getWholeDataBase():
    cars = collection.find()
    return cars

def insertCar(plate, timeEntered, isACT):
    insertObject = {"plate":plate, "timeEntered":timeEntered, "isACT":isACT}
    collection.insert_one(insertObject)

if __name__ == "__main__":
    print(getWholeDataBase())
