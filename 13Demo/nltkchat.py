from nltk.chat.util import Chat, reflections
from data.pair import pairs



# Create a Chat object and start the conversation
def chatbot():
    print("Hi, I'm a     MindCare chatbot. Type 'quit' to exit.")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    chatbot()