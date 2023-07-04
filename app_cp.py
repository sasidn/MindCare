from flask import Flask, render_template, request, redirect, flash, session, jsonify
import mysql.connector
import secrets
import config
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import logging
from logging import StreamHandler


logging.basicConfig(filename='logs.log', level=logging.INFO)

# Configure logger to output to console
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = StreamHandler()
logger.addHandler(stream_handler)

# Create a logger
logger = logging.getLogger(__name__)

app = Flask(__name__)
db = mysql.connector.connect(**config.DB_CONFIG)
dialogpt_model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(dialogpt_model_name, padding_side='left')
dialogpt_model = AutoModelForCausalLM.from_pretrained(dialogpt_model_name)

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
app.secret_key = secret_key


@app.route("/")
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)


@app.route("/create_user", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Create a connection to the database
        connection = mysql.connector.connect(**config.DB_CONFIG)

        try:
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
                flash("Username already exists. Please choose a different username.", "error")
                return redirect("/create_user")

            # Execute an INSERT query to add the user to the database
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            values = (username, password, email)
            cursor.execute(query, values)

            if cursor.rowcount == 1:
                # Commit the changes to the database
                connection.commit()
                flash("User registered successfully", "success")
                return redirect("/")
            else:
                # Some error occurred during registration
                flash("Error registering the user. Please try again.", "error")
                return redirect("/create_user")

        except Exception as e:
            flash("An error occurred: " + str(e), "error")
            return redirect("/create_user")

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

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
            return redirect("/forgot_password")

    return render_template('forgot_password.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a connection to the database
        connection = mysql.connector.connect(**config.DB_CONFIG)

        try:
            # Create a cursor object to interact with the database
            cursor = connection.cursor()

            # Execute a SELECT query to check if the user exists
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            cursor.execute(query, values)

            # Fetch the result
            result = cursor.fetchone()

            if result:
                # User exists
                return render_template('dashboard.html', message="Login successful", username=username)

            else:
                # User does not exist or incorrect password
                flash("Invalid credentials. Please try again!", "error")
                return redirect("/login")

        except Exception as e:
            flash("An error occurred: " + str(e), "error")
            return redirect("/login")

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

    return render_template('home.html')


@app.route("/dashboard.html")
def dashboard():
    username = request.args.get('username')
    session['username'] = username
    return render_template('dashboard.html', username=username)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = session.get('username')  # Retrieve the username from the session
        selected_model = request.form.get('model')  # Get the selected model from the form

        # Insert the selected model into the MySQL table
        try:
            conn = mysql.connector.connect(**config.DB_CONFIG)
            cursor = conn.cursor()

            # Prepare the SQL statement
            sql = "INSERT INTO chat (date, username, Chat_Model) VALUES (CURDATE(), %s, %s)"

            # Provide the values as a tuple
            values = (username, selected_model)

            # Execute the SQL statement
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            flash("Model selection inserted into the database successfully", "success")

        except mysql.connector.Error as error:
            flash("Error while inserting model selection into the database: " + str(error), "error")

    if 'chat_history_ids' not in session:
        session['chat_history_ids'] = []

    # Retrieve chat history from the session
    chat_history_ids = session['chat_history_ids']

    return render_template("chat.html", chat_history_ids=chat_history_ids)


@app.route("/chat", methods=["POST"])
def chat_post():
    try:
        user_input = request.form["message"]
        logger.info("User input: %s", user_input)
        chat_history_ids = session.get('chat_history_ids', [])  # Retrieve chat history from the session

        # Encode user input
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

        # Concatenate chat history and input
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if chat_history_ids else input_ids

        # Generate bot's response
        chat_history_ids = dialogpt_model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
        )

        # Decode bot's response
        bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        logger.info("Bot response: %s", bot_response)

        # Update chat history in the session
        session['chat_history_ids'] = chat_history_ids.tolist()

        return jsonify({"bot_response": bot_response})

    except Exception as e:
        # Log the error message for debugging
        logger.exception("An error occurred")
        return jsonify({"bot_response": "Error: An unexpected error occurred."})


if __name__ == "__main__":
    app.run(debug=True)
