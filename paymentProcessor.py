import requests
import json
from ecies import encrypt, decrypt
import binascii
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def rfidGetCardDetails():
    reader = SimpleMFRC522()
    data = {"success": False}
    try:
        
        id, text = reader.read()
        splitted = text.split(',')
        print(text)
        print(splitted)
        print(len(splitted))
        data = {"success": True, 
                "cardNumber":splitted[0],
                "cvv":splitted[1],
                "expiryMonth":splitted[2],
                "expiryYear":splitted[3]}
    finally:
        GPIO.cleanup()
    return data

def getPublicKey():
    response = requests.get('http://0.0.0.0:5000/api/public')
    
    responseDict = json.loads(response.text)
    rawKey = responseDict['publicKey']
    
    pk_hex = binascii.unhexlify(rawKey)
    return pk_hex

def dictToEncrypt(publicKey, rawData):
    strData = json.dumps(rawData)

    encryptedData = encrypt(publicKey, strData.encode('utf8'))
    return binascii.hexlify(encryptedData)

def sendPayment(price):
    publicKey = getPublicKey()

    data = rfidGetCardDetails()
    if data["success"] == False:
        return {"success":False}
    
    data["success"] = None
    data["price"] = price

    encryped = dictToEncrypt(publicKey, data)
    
    response = requests.post("http://0.0.0.0:5000/api/payment", data={"encrypted":encryped})
    print(response.text)
    return {"success":True, "response":response.text}

if __name__ == '__main__':
    publicKey = getPublicKey()
    sendPayment(5)

    #encrypted = dictToEncrypt(publicKey, data)
    #response = requests.post("http://0.0.0.0:5000/api/payment", data={"encrypted":encrypted})
    #print(response.text)
