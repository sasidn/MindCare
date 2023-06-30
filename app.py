from flask import Flask, Blueprint, render_template, request, redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
import config
import mysql.connector
import secrets

app = Flask(__name__)
db = mysql.connector.connect(**config.DB_CONFIG)

main_bp = Blueprint('main', __name__)

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
app.secret_key = secret_key


@app.route("/")
def home():

    username = request.args.get('username')

    return render_template('home.html',username=username)

@main_bp.route("/create_user", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Create a connection to the database
        connection = mysql.connector.connect(**config.DB_CONFIG)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Check if the username already exists in the database
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Username already exists
            cursor.close()
            connection.close()
            return "Username already exists. Please choose a different username."

        # Execute an INSERT query to add the user to the database
        query = "INSERT INTO users (username, name, password, email) VALUES (%s, %s, %s, %s)"
        values = (username, password, email)
        cursor.execute(query, values)

        if cursor.rowcount == 1:
            # Commit the changes to the database
            connection.commit()
            cursor.close()
            connection.close()
            return redirect("/?message=User%20registered%20successfully")
        else:
            # Some error occurred during registration
            cursor.close()
            connection.close()
            return "Error registering the user. Please try again."

        return redirect("/?message=User%20registered%20successfully")

    return render_template('create_user.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        try:
            email = request.form['email']

            # Perform forgot password logic here

            flash("Password reset email sent", "success")

            return redirect("/login")
        except Exception as e:
            flash("An error occurred: " + str(e), "error")
            print("Error:", e)
    return render_template('forgot_password.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a connection to the database
        connection = mysql.connector.connect(**config.DB_CONFIG)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute a SELECT query to check if the user exists
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if result:
            # User exists
            return render_template('dashboard.html', message="Login successful", username=username)

        else:
            # User does not exist or incorrect password
            return "Invalid credentials. Please try again!"

    return render_template('home.html')

@app.route("/dashboard.html")
def dashboard():
    username = request.args.get('username')
    session['username'] = username
    return render_template('dashboard.html', username=username)

@app.route("/chat")
def chat():
    username = request.args.get('username')
    session['username'] = username  # Store the username in the session
    return render_template('chat.html', username=username)

if __name__ == '__main__':
    app.run()