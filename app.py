from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'ansari.database.windows.net'
database = 'userdetail'
username = 'ansari'
password = 'Shakik123#'
driver = '{ODBC Driver 18 for SQL Server}'
connection_string = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'PORT=1433;'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'Encrypt=yes;'
    f'TrustServerCertificate=no;'
    f'Connection Timeout=30;'
)

# Function to establish a database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print("Error connecting to database: ", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    if conn is None:
        return 'Database connection error'

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Login WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            conn.close()
            return redirect(url_for('user_detail'))
        else:
            conn.close()
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
    skills = request.form.getlist('skill')

    conn = get_db_connection()
    if conn is None:
        return 'Database connection error'

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdetails (Name, PhoneNumber, Email) VALUES (?, ?, ?)", (name, phone, email))

        # Assuming there is a 'user_skills' table with a foreign key to userdetails
        for skill in skills:
            cursor.execute("INSERT INTO user_skills (username, skill) VALUES (?, ?)", (name, skill))

        conn.commit()
        conn.close()
        return 'Application submitted successfully!'
    except Exception as e:
        return f'An error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
