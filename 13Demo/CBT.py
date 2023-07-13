from datetime import datetime
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()

class ThoughtRecord:
    def __init__(self, situation, emotions, automatic_thoughts, adaptive_response, outcome):
        self.situation = situation
        self.emotions = emotions
        self.automatic_thoughts = automatic_thoughts
        self.adaptive_response = adaptive_response
        self.outcome = outcome
        self.timestamp = datetime.now()


# Function to get user input for the thought record
def get_thought_record():
    situation = input("Situation: ")
    emotions = input("Emotions: ")
    automatic_thoughts = input("Automatic Thoughts: ")
    adaptive_response = input("Adaptive Response: ")
    outcome = input("Outcome: ")

    return ThoughtRecord(situation, emotions, automatic_thoughts, adaptive_response, outcome)


# Example usage
record = get_thought_record()

# Prepare the SQL query
sql = "INSERT INTO thought_record (date, situation, automatic_thoughts, emotions, adaptive_response, outcome) " \
      "VALUES (%s, %s, %s, %s, %s, %s)"

# Define the values to be inserted
values = (record.timestamp, record.situation, record.automatic_thoughts, record.emotions, record.adaptive_response,
          record.outcome)

# Execute the query
cursor.execute(sql, values)

# Commit the transaction
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()

# Accessing the record attributes
print("Situation:", record.situation)
print("Emotions:", record.emotions)
print("Automatic Thoughts:", record.automatic_thoughts)
print("Adaptive Response:", record.adaptive_response)
print("Outcome:", record.outcome)
print("Timestamp:", record.timestamp)
