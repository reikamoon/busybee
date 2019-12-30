from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/busybee')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
busybee = db.busybee
shopping = db.busybee.shopping

app = Flask(__name__)

@app.route('/')
def home():
    #Home
    return render_template('home.html')

@app.route('/today')
def todo():
    #Show To Do List
    return render_template('today.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
