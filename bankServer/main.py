from flask import Flask, request, jsonify
from pymongo import MongoClient
from ecies import encrypt
import binascii
import encryption
import json

client = MongoClient('mongodb://root:password@localhost:27017/')
databaseBank = client.bank
collectionUsers = databaseBank.users

app = Flask(__name__)

def requestToDecrypt(request):
    encrypted = request.form.to_dict()['encrypted']
    decrypted = encryption.decryptMessage(encrypted)
    dictRequests = json.loads(decrypted)
    
    return dictRequests

@app.route('/')
def index():
    return "<h1>hello world</h1>"

@app.route('/api/public', methods=['GET'])
def public():
    with open('keys/public.txt') as f:
        for line in f:
            return jsonify({"publicKey":''.join(line.split())})

@app.route('/api/payment', methods=['POST'])
def payment():
    dictRequests = requestToDecrypt(request) 

    cardNumber = dictRequests['cardNumber']
    
    user = collectionUsers.find_one({'cardNumber':int(cardNumber)})
    

    if not user:
        return jsonify({'success':False})

    if not (user['cvv'] == int(dictRequests['cvv'])):
        return jsonify({'success':False})

    if not (user['balance'] >= int(dictRequests['price'])):
        return jsonify({'success':false})

    collectionUsers.update_one({
       'cardNumber':int(cardNumber)
        },{
        '$inc':{
                'balance':0-int(dictRequests['price'])
                }
        }, upsert=False)
    


    return ({'success':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
