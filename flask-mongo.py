from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

# Load environment variables from .env file
load_dotenv()

# MongoDB Atlas connection URI
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

# Implement other routes similarly

if __name__ == '__main__':
    app.run(debug=True)
