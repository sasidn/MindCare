from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Route to render the chat page
@app.route("/")
def chat():
    return render_template("popup_example.html")

# Route to handle the popup response
@app.route("/handle_popup_response", methods=["POST"])
def handle_popup_response():
    popup_response = request.form["popup_response"]

    # Process the popup_response and send the confirmation back to the client
    # For example, you can check if the response is "yes" and redirect to the Thought Diary page
    if popup_response == "yes":
        return redirect("/thought_diary")
    else:
        return redirect("/")

# Route to render the Thought Diary page
@app.route("/thought_diary")
def thought_diary():
    return render_template("thought_diary.html")

if __name__ == "__main__":
    app.run(port=5001)
