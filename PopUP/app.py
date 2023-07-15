from flask import Flask, render_template, request, redirect, session
import secrets
from datetime import date, datetime
from chatGPT import start_chatbot
import json
app = Flask(__name__)

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
app.secret_key = secret_key

def check_trigger(user_response, trigger_words):
    for word in trigger_words:
        if word in user_response:
            # Trigger word found
            return word

    # No trigger word found
    return None

@app.route("/")
def chat():
    user_input = request.args.get("user_input")
    trigger_words = ["sad"]
    trigger_word = check_trigger(user_input, trigger_words)
    if trigger_word:
        # Check if the pop-up has been displayed before
        session["popup_displayed"] = True
        return render_template("popup_example.html")
    else:
        return render_template("popup_example.html")

@app.route("/handle_popup_response", methods=["POST"])
def handle_popup_response():
    popup_response = request.form["popup_response"]

    if popup_response == "yes":
        return redirect("/thought_diary")
    elif popup_response == "no":
        return redirect("/")
    else:
        return redirect("/")

@app.route("/thought_diary")
def thought_diary():
    return render_template("thought_diary.html")


if __name__ == "__main__":
    app.run(port=5001)
