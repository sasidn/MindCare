from flask import Flask, render_template,request,json,redirect,flash
from datetime import date, datetime
import mysql.connector
import json

app = Flask(__name__)

# Configure database connection

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)

# Create database connection

cursor = db.cursor()
@app.route('/')
def index():
    username = 'sasidn'
    # Fetch thought diary data from the SQL table (replace with your own logic)
    query = "SELECT date,situation, automatic_thoughts, emotions,adaptive_response,outcome FROM thought_diary WHERE username = %s"
    cursor.execute(query, (username,))
    thoughts = cursor.fetchall()

    # Fetch mood tracker  from the SQL table
    mood_query = "SELECT Message_id, sentiment FROM mood_tracker WHERE username = %s"
    cursor.execute(mood_query, (username,))
    moods = cursor.fetchall()
    sentiment_labels = []
    sentiment_data = []

    for mood in moods:
        sentiment_labels.append(mood[0])
        sentiment_data.append(mood[1])
    # Fetch emotion response data from the SQL table
    response_query = "SELECT DISTINCT Responses FROM emotional_analysis WHERE username = %s"
    cursor.execute(response_query, (username,))
    responses = [response[0] for response in cursor.fetchall()]

    # Fetch summary data from the SQL table
    summary_query = "SELECT date, summary FROM summary WHERE username = %s"
    cursor.execute(summary_query, (username,))
    summary = cursor.fetchall()

    # Fetch emotion response data from the SQL table
    sum_query = "SELECT DISTINCT trim(date) as trackingDate FROM summary WHERE username = %s"
    cursor.execute(sum_query, (username,))
    trackingDates = [trackingDate[0] for trackingDate in cursor.fetchall()]

    return render_template(
        "chat_history.html",
        thoughts=thoughts,
        sentiment_labels=sentiment_labels,
        sentiment_data=sentiment_data,
        responses=responses,
        summary=summary,
        trackingDates=trackingDates
        )

@app.route('/update_emotional_analysis', methods=['POST'])
def update_emotional_analysis():
    selected_response = request.json.get('response')

    # Fetch emotional analysis data from the SQL table based on the selected response
    emotion_query = "SELECT label, SCORE FROM emotional_analysis WHERE responses = %s AND username = %s"
    cursor.execute(emotion_query, (selected_response, 'sasidn'))
    emotions = cursor.fetchall()
    emotions_labels = [emotion[0] for emotion in emotions]
    emotions_score = [emotion[1] for emotion in emotions]

    data = {
        'emotions_labels': emotions_labels,
        'emotions_score': emotions_score
    }

    return json.dumps(data)


if __name__ == "__main__":
    app.run(port=5001)
