from flask import Flask, render_template,request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

#print(openai.api_key)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot-BERT", methods=["POST"])
def chatbot():
    user_input = request.form['message']
    prompt = f"User:{user_input}\nChatbot:"
    chat_history = []
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ","\nChatbot: "]

    )
    bot_response = response.choices[0].text.strip()

    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")

    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response,
    )

if __name__ == '__main__':
    app.run(debug=True)