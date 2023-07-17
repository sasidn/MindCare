from flask import Flask, render_template,request
import mysql.connector
import json

app = Flask(__name__)

# Configure database connection
db_config = {
    'host': 'localhost',
    'user': 'MindCare',
    'password': 'MindCare',
    'database': 'mindcare'
}

# Create database connection
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

@app.route('/')
def index():
    # Fetch response data from the SQL table
    response_query = "SELECT DISTINCT Responses FROM emotional_analysis WHERE username = %s"
    cursor.execute(response_query, ('sasidn',))
    responses = [response[0] for response in cursor.fetchall()]
    print(responses)

    return render_template('emotional_analysis.html', responses=responses, emotions_labels=[], emotions_score=[])


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
if __name__ == '__main__':
    app.run(port=5001)
