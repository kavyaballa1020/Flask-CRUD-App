from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

def create_connection():
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    return db

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/', methods=['POST'])
def insert():
    reg_number = request.form['reg_number']
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    
    db = create_connection()
    users_collection = db.users
    users_collection.insert_one({'reg_number': reg_number, 'name': name, 'age': age, 'address': address})
    
    flash('Data saved successfully', 'success')
    return redirect(url_for('index', message='Data saved successfully'))

@app.route('/display')
def display():
    db = create_connection()
    users_collection = db.users
    data = users_collection.find()
    
    return render_template('display.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        db = create_connection()
        users_collection = db.users
        result = users_collection.find_one({'reg_number': reg_number})
        
        if result:
            return render_template('display.html', data=[result])
        else:
            flash('Data not found', 'error')
            return redirect(url_for('index'))
    else:
        return render_template('search.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        
        db = create_connection()
        users_collection = db.users
        users_collection.update_one({'reg_number': reg_number}, {'$set': {'name': name, 'age': age, 'address': address}})
        
        flash('Data updated successfully', 'success')
        return redirect(url_for('index', message='Data updated successfully'))
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        db = create_connection()
        users_collection = db.users
        result = users_collection.delete_one({'reg_number': reg_number})
        
        if result.deleted_count:
            flash('Data deleted successfully', 'success')
        else:
            flash('Data not found', 'error')
        
        return render_template('delete.html', message='Data deleted successfully' if result.deleted_count else 'Data not found')
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
