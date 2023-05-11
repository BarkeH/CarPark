from flask import Flask, request, jsonify
from pymongo import MongoClient
from ecies import encrypt
import binascii

client = MongoClient('mongodb://root:password@localhost:27017/')
databaseBank = client.bank
collectionUsers = databaseBank.users

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>hello world</h1>"

@app.route('/api/public', methods=['GET'])
def public():
    with open('keys/public.txt') as f:
        for line in f:
            return jsonify({"public":"this is a public key"})

    #return jsonify({"publickey":str(pk_hex)})
@app.route('/api/payment', methods=['POST'])
def payment():
    #TODO encryption
    dictRequests = request.form.to_dict()
    cardNumber = dictRequests['cardNumber']
    
    user = collectionUsers.find_one({'cardNumber':int(cardNumber)})
    

    if not user:
        return jsonify({'success':'no user'})

    if not (user['cvv'] == int(request.form['cvv'])):
        return jsonify({'success':'cvv incorrect'})

    if not (user['balance'] >= int(request.form['price'])):
        return jsonify({'success':'balance no good'})

    collectionUsers.update_one({
       'cardNumber':int(cardNumber)
        },{
        '$inc':{
                'balance':0-int(request.form['price'])
                }
        }, upsert=False)
    


    return ({'success':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
