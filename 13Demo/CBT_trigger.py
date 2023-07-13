import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="MindCare",
    password="MindCare",
    database="mindcare"
)
cursor = db.cursor()
def check_trigger(user_response):

    cursor.execute('SELECT triggers FROM CBT_trigger')
    trigger_words = cursor.fetchall()

    for word in trigger_words:
        if word[0] in user_response:
            # Trigger word found, display the pop-up
            break

    db.close()