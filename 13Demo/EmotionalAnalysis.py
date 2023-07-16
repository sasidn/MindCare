import mysql.connector
from transformers import pipeline

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()

# Fetch messages from the database
select_messages_sql = "SELECT DISTINCT trim(user_response) FROM messages WHERE user_response <> '' and username ='sasidn'"
cursor.execute(select_messages_sql)
messages = cursor.fetchall()

# Create a text classification pipeline for emotion prediction
pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest",top_k=None)

for message in messages:
    user_response = message[0]
    emotions = pipe(user_response)

    for emotion in emotions[0]:
        label = emotion['label']
        score = emotion['score']
        username = 'sasidn'
        # Insert emotion data into the table
        insert_emotion_sql = "INSERT INTO Emotional_Analysis (Responses, label, score,username) VALUES (%s, %s, %s,%s)"
        cursor.execute(insert_emotion_sql, (user_response, label, score,username ))

# Commit the changes to the database
db.commit()

print("Emotion results inserted into the table.")
