from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

# Load environment variables from .env file
load_dotenv()

# MySQL database configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

def create_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    return conn


def create_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
    conn.close()

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


if __name__ == '__main__':
    create_database()
    create_table() 
    app.run(debug=True)
