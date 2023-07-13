import csv
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load pre-trained model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Set device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Path to the file
file_path = 'data/20200325_counsel_chat.csv'

# Read the file and process each question
with open(file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question_text = row['questionText']
        topic = row['topic']

        # Define labels dynamically based on the unique topics in the file
        labels = list(set(row['topic'] for row in reader))

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

        # Get predicted label based on the index or fallback to the original topic value
        predicted_label = labels[predicted_label_index] if predicted_label_index < len(labels) else topic

        # Print the question and predicted topic
        print("Question:", question_text)
        print("Predicted Topic:", predicted_label)
        print()
