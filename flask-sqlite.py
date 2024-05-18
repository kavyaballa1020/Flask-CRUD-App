from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

def create_connection():
    conn = sqlite3.connect('data.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    reg_number TEXT,
                    name TEXT,
                    age TEXT,
                    address TEXT
                    )''')
    conn.commit()
    conn.close()

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
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (reg_number, name, age, address) VALUES (?, ?, ?, ?)", (reg_number, name, age, address))
    conn.commit()
    conn.close()
    
    flash('Data saved successfully', 'success')
    return redirect(url_for('index', message='Data saved successfully'))

@app.route('/display')
def display():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    
    return render_template('display.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=?", (reg_number,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return render_template('display.html', data=[result])
        else:
            return render_template('search.html', message='Data not found', reg_number=reg_number)
    else:
        return render_template('search.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name=?, age=?, address=? WHERE reg_number=?", (name, age, address, reg_number))
        conn.commit()
        conn.close()
        
        flash('Data updated successfully', 'success')
        return redirect(url_for('index', message='Data updated successfully'))
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE reg_number=?", (reg_number,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM users WHERE reg_number=?", (reg_number,))
            conn.commit()
            flash('Data deleted successfully', 'success')
        else:
            flash('Data not found', 'error')
        
        conn.close()
        return render_template('delete.html', message='Data deleted successfully' if result else 'Data not found')
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    create_table() 
    app.run(debug=True)
