from flask import Flask, render_template, request, flash, redirect, session,jsonify
from flask_mail import Message, Mail
import mysql.connector
import secrets
import bcrypt
from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
from wtforms import Form, StringField, PasswordField, validators
from datetime import date,datetime
from chatGPT import start_chatbot, generate_response
import json




app = Flask(__name__)
# Configure Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

mail = Mail(app)
# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
app.secret_key = secret_key

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()

# Define the UserForm for input validation
class UserForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" in session:
        return redirect("/dashboard")
    else:
        return redirect("/create_user")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Insert the user data into the MySQL table
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        try:
            cursor.execute(query, values)
            db.commit()
            print("User inserted successfully!")
            flash("User created successfully!", "success")

            print("Username:", username)
        except mysql.connector.Error as error:
            print(f"Error creating user: {error}")
            flash(f"Error creating user: {error}", "error")

        return redirect("/")

    return render_template("home.html")

@app.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        email = request.form["email"]

        # Check if the email exists in the database
        query = "SELECT username, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            username = result[0]
            password = result[1]

            # Send the password reminder email
            send_password_email(email, username, password)
            flash("Password reminder sent to your email!", "success")
        else:
            flash("Email not found!", "error")

        return redirect("/")

    return render_template("forget_password.html")

def send_password_email(email, username, password):
    msg = Message("Password Reminder", sender="your_email@example.com", recipients=[email])
    msg.body = f"Hello {username},\n\nYour password is: {password}\n\nBest regards,\nMindCare Team"
    mail.send(msg)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Query the database to fetch the user's password based on the username
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]

        # Verify the password
        if password == stored_password:
            # Successful login
            session['username'] = username
            return redirect("/dashboard.html")

    # Invalid login
    flash("Invalid username or password", "error")
    return redirect("/")


@app.route("/dashboard.html")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")


@app.route("/model.html", methods=["GET", "POST"])
def model():

    # Handle the GET request
    return render_template("model.html")

@app.route("/select", methods=["POST"])
def model_select():
    username = session["username"]
    chat_model = request.form.get("model")
    date = datetime.now()

    # Insert the user data into the MySQL table
    query = "INSERT INTO chat (username, chat_model, date) VALUES (%s, %s, %s)"
    values = (username, chat_model, date)
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as error:
        print(f"Error inserting: {error}")

    return redirect("/chat")

def check_trigger(user_response, trigger_words):
    for word in trigger_words:
        if word in user_response:
            # Trigger word found, display the pop-up
            print("CBT trigger:", word)
            flash("CBT trigger: " + word)
            return True

    # No trigger word found
    return False
@app.route("/chat", methods=["GET", "POST"])
def chat():
    chatbot_response = None

    username = session["username"]
    query = "SELECT MAX(Chat_id) FROM chat WHERE username = %s AND date = CURDATE()"
    cursor.execute(query, (username,))
    max_chat_id = cursor.fetchone()[0]

    messages = [
        {"name": "ChatBot", "img": "/static/chatbot.png", "time": "12:00 PM", "text": "Hello, how can I help you?"}
    ]

    if request.method == "POST":
        query = """
            SELECT Chat_Model
            FROM chat
            WHERE username = %s
                AND date = CURDATE()
                AND Chat_id = %s
        """
        cursor.execute(query, (username, max_chat_id))
        result = cursor.fetchone()

        if result:
            chat_model = result[0]
            if chat_model == 'ChatGPT':
                user_input = request.form["message"]
                chatbot_response = start_chatbot(user_input)

                query = """
                    INSERT INTO Messages (chat_id, Username, date, user_response, bot_response)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)
                """
                cursor.execute(query, (max_chat_id, username, user_input, chatbot_response))
                db.commit()

                cursor.execute('SELECT triggers FROM CBT_trigger')
                trigger_words = [word[0] for word in cursor.fetchall()]
                trigger_word_found = check_trigger(user_input, trigger_words)

                if trigger_word_found :
                    # Redirect to the Thought Diary page
                    return redirect("/thought_diary.html")

        return jsonify({"response": chatbot_response})

    return render_template("chat.html", messages=messages)


@app.route("/handle_popup_response", methods=["POST"])
def handle_popup_response():
    popup_response = request.form["popup_response"]

    # Process the popup_response and send the confirmation back to the client
    # For example, you can check if the response is "yes" and return a JSON response

    if popup_response == "yes":
        return {"popup_confirmed": True}
    else:
        return {"popup_confirmed": False}


@app.route("/thought_diary.html")
def thought_diary():
    return render_template("thought_diary.html")
@app.route("/thought_diary", methods=["POST"])
def thought_diary_post():
    if request.method == "POST":
        username = session["username"]
        current_date = date.today().strftime("%Y-%m-%d")
        situation = request.form["situation"]
        automatic_thoughts = request.form["automatic_thoughts"]
        emotions = request.form["emotions"]
        adaptive_response = request.form["adaptive_response"]
        outcome = request.form["outcome"]
        # Retrieve the values for emotions, adaptive response, and outcome in a similar way

        # Insert the thought entry into the database
        query = "INSERT INTO thought_diary (username, date, situation, automatic_thoughts, emotions, adaptive_response, outcome) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (username, current_date, situation, automatic_thoughts, emotions, adaptive_response, outcome)
        cursor.execute(query, values)
        db.commit()
        flash("Thought entry added successfully!", "success")
        print("success")

        # Store the thought entry data in the database or perform any other required actions

        # Redirect to the chat page after handling the form submission
        return redirect("/chat")

    # Handle GET requests separately if needed
    # ...
    print("cechking")
    # Return the Thought Diary page template
    return "Invalid request method for /thought_diary"




@app.route("/recommendation.html")
def get_recommendations():
    # Fetch recommendations from the recommendation_log table
    query = "SELECT r.recommendation, l.date, l.user_comments FROM recommendation r ,recommendation_log l where l.recommendation_id=r.recommendation_id"
    cursor.execute(query)
    recommendations = cursor.fetchall()

    # Render the HTML template with the recommendations data
    return render_template("recommendation.html", recommendations=recommendations)

@app.route("/chat_history.html", methods=["GET", "POST"])
def chat_history():
    username = session["username"]
    # Fetch thought diary data from the SQL table (replace with your own logic)
    query = "SELECT date,situation, automatic_thoughts, emotions,adaptive_response,outcome FROM thought_diary WHERE username = %s"
    cursor.execute(query, (username,))
    thoughts = cursor.fetchall()
    return render_template("chat_history.html", thoughts=thoughts)

@app.route("/add_thought_entry", methods=["POST"])
def add_thought_entry():
    username = session["username"]
    current_date = date.today().strftime("%Y-%m-%d")
    situation = request.form["situation"]
    automatic_thoughts = request.form["automatic_thoughts"]
    emotions = request.form["emotions"]
    adaptive_response = request.form["adaptive_response"]
    outcome = request.form["outcome"]
    # Retrieve the values for emotions, adaptive response, and outcome in a similar way

    # Insert the thought entry into the database
    query = "INSERT INTO thought_diary (username, date, situation, automatic_thoughts, emotions, adaptive_response, outcome) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (username, current_date, situation, automatic_thoughts, emotions, adaptive_response, outcome)
    cursor.execute(query, values)
    db.commit()
    flash("Thought entry added successfully!", "success")

    return redirect("/chat_history.html")


if __name__ == "__main__":
    app.run(port=5001)