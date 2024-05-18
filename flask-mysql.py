from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

# Load environment variables from .env file
load_dotenv()

# MySQL database configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

# Function to create MySQL connection
def create_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    return conn

# Function to create database if not exists
def create_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
    conn.close()

# Function to create users table if not exists
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_db.users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reg_number VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    age VARCHAR(10) NOT NULL,
                    address VARCHAR(255) NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Route for index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process the form submission
        reg_number = request.form['reg_number']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (reg_number, name, age, address) VALUES (%s, %s, %s, %s)", (reg_number, name, age, address))
        conn.commit()
        conn.close()
        
        flash('Data saved successfully', 'success')
        return redirect(url_for('index', message='Data saved successfully'))
    else:
        # Render the index template
        message = request.args.get('message')
        return render_template('index.html', message=message)

# Route for displaying all users
@app.route('/display')
def display():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    
    return render_template('display.html', data=data)

# Route for searching a user by registration number
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=%s", (reg_number,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return render_template('display.html', data=[result])
        else:
            return render_template('search.html', message='Data not found', reg_number=reg_number)
    else:
        return render_template('search.html')

# Route for updating user information
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name=%s, age=%s, address=%s WHERE reg_number=%s", (name, age, address, reg_number))
        conn.commit()
        conn.close()
        
        flash('Data updated successfully', 'success')
        return redirect(url_for('index', message='Data updated successfully'))
    else:
        return render_template('update.html')

# Route for deleting a user
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=%s", (reg_number,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM users WHERE reg_number=%s", (reg_number,))
            conn.commit()
            flash('Data deleted successfully', 'success')
        else:
            flash('Data not found', 'error')
        
        conn.close()
        return render_template('delete.html', message='Data deleted successfully' if result else 'Data not found')
    else:
        return render_template('delete.html')

# Main block to run the application
if __name__ == '__main__':
    create_database() 
    create_table()
    app.run(debug=True)
