import mysql.connector
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import config
import mysql.connector
import datetime

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()

sentimentm = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(sentimentm)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentimentm)


def get_sentiments():
    # Connect to the MySQL database
    #username = session["username"]
    username = 'sasidn'


    # Retrieve chat messages from the "message" table
    select_messages_sql = "SELECT user_response, message_id, chat_id, date, username FROM messages"
    cursor.execute(select_messages_sql)
    messages = cursor.fetchall()

    sentiments = []

    # Process each chat user response and get its sentiment
    for message in messages:
        user_input = message[0]
        message_id = message[1]
        chat_id = message[2]
        tracking_date = message[3]
        username = message[4]

        input_ids = tokenizer.encode(user_input, return_tensors="pt")
        logits = sentiment_model(input_ids).logits
        sentiment = logits.argmax().item()
        sentiments.append(sentiment)

        # Insert sentiment, message_id, tracking_date, and username into Mood_Tracker table
        insert_mood_tracker_sql = "INSERT INTO Mood_Tracker (tracking_date, sentiment, message_id, username) VALUES (%s, %s, %s, %s)"
        mood_tracker_values = (tracking_date, sentiment, message_id, username)
        cursor.execute(insert_mood_tracker_sql, mood_tracker_values)
        db.commit()

    cursor.close()
    db.close()

    return sentiments


chat_sentiments = get_sentiments()
print(chat_sentiments)