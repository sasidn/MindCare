import mysql.connector
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import config
db = mysql.connector.connect(**config.DB_CONFIG)
import datetime

sentimentm = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(sentimentm)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentimentm)


def get_sentiments():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**config.DB_CONFIG)
    cursor = conn.cursor()

    # Retrieve chat messages from the "message" table
    select_messages_sql = "SELECT message_id, user_response FROM messages"
    cursor.execute(select_messages_sql)
    messages = cursor.fetchall()

    sentiments = []

    # Process each chat message and get its sentiment
    for message in messages:
        message_id = message[0]
        user_input = message[1]
        input_ids = tokenizer.encode(user_input, return_tensors="pt")
        logits = sentiment_model(input_ids).logits
        sentiment = logits.argmax().item()
        sentiments.append(sentiment)

        # Insert sentiment, message_id, and tracking_date into Mood_Tracker table
        tracking_date = datetime.datetime.now().date()
        insert_mood_tracker_sql = "INSERT INTO Mood_Tracker (tracking_date, sentiment, message_id) VALUES (%s, %s, %s)"
        mood_tracker_values = (tracking_date, sentiment, message_id)
        cursor.execute(insert_mood_tracker_sql, mood_tracker_values)
        conn.commit()

    cursor.close()
    conn.close()

    return sentiments

chat_sentiments = get_sentiments()
print(chat_sentiments)