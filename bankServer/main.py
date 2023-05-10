from flask import Flask
from flask import request
from pymongo import MongoClient

client = MongoClient('mongodb://root:password@localhost:27017/')

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>test</h1>"


