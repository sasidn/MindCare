import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, render_template, request

app = Flask(__name__)
model_1name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side='left')
model = AutoModelForCausalLM.from_pretrained(model_name)
chat_history_ids = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history_ids

    user_input = request.form["message"]
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = torch.cat([chat_history_ids[:, -1024:], input_ids], dim=-1) if chat_history_ids is not None else input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
    )

    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Add bot response to chat history
    chat_history_ids = torch.cat([chat_history_ids, bot_input_ids], dim=-1)[:, -1024:]

    return {"bot_response": bot_response}



if __name__ == "__main__":
    app.run(debug=True)
