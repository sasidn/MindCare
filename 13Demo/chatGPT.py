import openai
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to generate response from ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text
    message = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', message)
    message = message.strip()

    return message

# Define function to start the chatbot
def start_chatbot(user_input):
    # Generate a response from ChatGPT
    prompt = f"User:{user_input}\nChatbot:"
    response = generate_response(prompt)

    return response
