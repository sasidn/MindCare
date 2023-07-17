import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()

username = 'sasidn'

# Fetch emotional analysis data from the SQL table for the selected response
response = 'selected_response'  # Replace 'selected_response' with the actual selected response
emotion_query = "SELECT label, SCORE FROM emotional_analysis WHERE username = %s AND Responses = %s"
cursor.execute(emotion_query, (username, response))
emotions = cursor.fetchall()
emotions_labels = []
emotions_score = []
for emotion in emotions:
    emotions_labels.append(emotion[0])
    emotions_score.append(emotion[1])

# Create a DataFrame from the emotions data
df_emotions = pd.DataFrame({'Emotion': emotions_labels, 'Score': emotions_score})

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(df_emotions['Emotion'], df_emotions['Score'])
plt.xlabel('Emotion')
plt.ylabel('Score')
plt.title('Emotional Analysis for Response: {}'.format(response))
plt.xticks(rotation=45)
plt.tight_layout()

# Display the chart
plt.show()

# Close the cursor and connection
cursor.close()
db.close()
