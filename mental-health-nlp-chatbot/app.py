
from chat import get_response, bot_name

class ChatApplication:
    def __init__(self):
        self.chat_history = []

    def run(self):
        print("Chat Application")
        print("Type 'exit' to quit")

        while True:
            message = input("You: ")
            if message == "exit":
                break
            response = self.get_response(message)
            print("Bot: " + response)

    def get_response(self, message):
        response = get_response(message)
        return response

if __name__ == "__main__":
    app = ChatApplication()
    app.run()
