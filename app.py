from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/busybee')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
bees = db.bees
lists = db.lists
products = db.products

app = Flask(__name__)

@app.route('/')
def home():
    #Home
    return render_template('home.html')

@app.route('/today')
def todo():
    #Show To Do List
    return render_template('todolistalt.html')

@app.route('/mylists')
def view_lists():
    #Show my shopping lists from db.lists
    return render_template('list_view.html', lists=lists)

@app.route('/mylists/new')
def new_list():
    #Create a New List
    return render_template('Anew_shoppinglist.html', lists={}, title='New List')

@app.route('/mylists', methods=['POST'])
def submit_list():
    #Submit a new list to the db.lists.
    new_list = {
    'name': request.form.get('name'),
    'products': #Insert a product from the database into list?
    }
    lists_id = lists.insert_one(new_list).inserted_id
    return redirect(url_for('view_lists', lists_id=lists_id))

@app.route('/edit/<list_id>', methods = ['POST'])
def edit_list():
    #edit my shopping list
    my_list = lists.find_one({'_id':ObjectId(list_id)})
    return render_template('Aedit_shoppinglist.html', lists=my_list)

@app.route('/edit/<list_id>', methods=['POST'])
def list_update(lists_id):
    #Save Edits to list and Update list in the database.
    updated_list = {
        'name': request.form.get('name'),
        'products': #Insert a product from the database?
    }
    lists.update_one(
        {'_id': ObjectId(list_id)},
        {'$set': updated_list})
    return redirect(url_for('view_lists', list_id=list_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
