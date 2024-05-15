from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'tcp:ansari.database.windows.net'
database = 'userdetail'
username = 'ansari'
password = 'Shakik123#'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'


# Function to establish a database connection
def get_db_connection():
    return pyodbc.connect(connection_string)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check credentials against the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Login WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            conn.close()  # Close the database connection
            return redirect(url_for('user_detail'))
        else:
            conn.close()  # Close the database connection
            return 'Invalid username or password'

    except Exception as e:
        return f'An error occurred: {str(e)}'


@app.route('/user_detail')
def user_detail():
    return render_template('user_detail.html')


@app.route('/submit_application', methods=['POST'])
def submit_application():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    skills = request.form.getlist('skill')  # Get list of skills

    # Insert data into the userdetails table
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdetails (Name, PhoneNumber, Email) VALUES (?, ?, ?)", (name, phone, email))

        # Insert skills into a separate table, assuming 'user_skill' table structure
        for skill in skills:
            cursor.execute("INSERT INTO userdetails (Skills) VALUES (?)", (skill))

        conn.commit()
        conn.close()  # Close the database connection
        return 'Application submitted successfully!'
    except Exception as e:
        return f'An error occurred: {str(e)}'


if __name__ == '__main__':
    app.run()
