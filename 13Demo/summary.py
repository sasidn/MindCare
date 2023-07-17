import mysql.connector
from datetime import datetime
from transformers import pipeline

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)

cursor = db.cursor()

# Load the summarization pipeline with the CPU version of the model
summarizer = pipeline("summarization", model="philschmid/flan-t5-base-samsum", device=-1)

# Example usage with SQL query result
response_query = "SELECT m.user_response, m.bot_response FROM messages m JOIN chat c ON c.chat_id = m.chat_id;"
cursor.execute(response_query)
result = cursor.fetchall()

# Combine user and bot responses
combined_responses = ' '.join([f'{user_response} {bot_response}' for user_response, bot_response in result])

# Generate the summary
summary = summarizer(combined_responses)

# Convert the summary from list to string
summary_text = summary[0]['summary_text']

# Insert the summary into the summary table
current_date = datetime.now()
insert_query = "INSERT INTO summary (summary, date) VALUES (%s, %s)"
cursor.execute(insert_query, (summary_text, current_date))
db.commit()  # Don't forget to commit the changes

# Close the database connection
db.close()
