import csv
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import mysql.connector
import config

# Load pre-trained model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Set device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Path to the file
file_path = 'data/20200325_counsel_chat.csv'

def predict_topics():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**config.DB_CONFIG)
    cursor = conn.cursor()

    # Retrieve chat messages from the "messages" table
    select_messages_sql = "SELECT message_id, user_response FROM messages"
    cursor.execute(select_messages_sql)
    messages = cursor.fetchall()

    for message in messages:
        message_id = message[0]
        user_response = message[1]

    # Read the file and process each question
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # Define labels dynamically based on the unique topics in the file
        labels = list(set(row['topic'] for row in reader))

        # Reset the file pointer to the beginning
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)

        for row in reader:
            question_text = row['questionText']
            topic = row['topic']

            # Tokenize input text
            inputs = tokenizer.encode_plus(
                question_text,
                add_special_tokens=True,
                truncation=True,
                max_length=512,
                padding='max_length',
                return_tensors='pt'
            )

            # Move input tensors to the appropriate device
            input_ids = inputs['input_ids'].to(device)
            attention_mask = inputs['attention_mask'].to(device)

            # Make predictions
            with torch.no_grad():
                outputs = model(input_ids, attention_mask=attention_mask)

            # Get predicted probabilities
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)[0]

            # Get predicted label index
            predicted_label_index = torch.argmax(probabilities).item()

            # Get predicted label based on the index or fallback to a default value
            predicted_label = labels[predicted_label_index] if predicted_label_index < len(labels) else 'Unknown'

            # Insert the predicted topic into the chat_history table
            insert_chat_history_sql = "INSERT INTO chat_history (chat_id, chat_summary, topic) VALUES (%s, %s, %s)"
            chat_history_values = (message_id, user_response, predicted_label)
            cursor.execute(insert_chat_history_sql, chat_history_values)
            conn.commit()

    cursor.close()
    conn.close()

# Example usage
predict_topics()
