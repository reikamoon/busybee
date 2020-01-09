from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/bees')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
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
    return render_template('today.html')

@app.route('/mylists')
def view_lists():
    #Show my shopping lists from db.lists
    return render_template('Ashow_shoppinglist.html', lists=lists.find())

@app.route('/mylists/<list_id>', methods=['GET', 'POST'])
def show_list(list_id):
    #Show a single List
    list = lists.find_one({'_id': ObjectId(list_id)})
    print(list)
    return render_template('list_view.html', list=list)


@app.route('/mylists/new/list')
def new_list():
    #Create a New List
    return render_template('Anew_shoppinglist.html', lists={}, title='New List')

@app.route('/mylists', methods=['POST'])
def submit_list():
    #Submit a new list to the db.lists.
    new_list = {
    'name': request.form.get('name'),
    'products': request.form.get('products')
    }
    lists_id = lists.insert_one(new_list).inserted_id
    return redirect(url_for('view_lists', lists_id=lists_id))

@app.route('/mylists/<list_id>/edit', methods = ['POST'])
def edit_list():
    #edit my shopping list
    product_list = lists.find_one({'_id': ObjectId(list_id)})['products']
    return render_template('Aedit_shoppinglist.html', lists=product_list)

@app.route('/mylists/<list_id>/edit', methods=['POST'])
def list_update(lists_id):
    #Save Edits to list and Update list in the database.
    updated_list = {
        'name': request.form.get('name'),
        'products': request.form.get('products')
    }
    lists.update_one(
        {'_id': ObjectId(list_id)},
        {'$set': updated_list})
    return redirect(url_for('view_lists', list_id=list_id))



# products
@app.route('/mylists/<list_id>/new')
def new_product(list_id):
    #Create a new product
    list = lists.find_one({'_id': ObjectId(list_id)})
    return render_template('Bnew_product.html', list=list, products={})

@app.route('/mylists/<list_id>', methods=['POST'])
def submit_product(list_id):
    #Submit Product to Database and add to list
    product_list = lists.find_one({'_id': ObjectId(list_id)})['products']
    print(product_list)
    new_product = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'URL': request.form.get('url'),
        'image_url': request.form.get('image_url')
    }
    print(new_product)
    product_list.append(new_product)
    # product_id = products.insert_one(new_product).inserted_id
    lists.update_one(
    {'_id': ObjectId(list_id)},
    {'$set': {'products': product_list}})
    return redirect(url_for('show_list', list_id=list_id))

# Calculator
@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

#about page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
