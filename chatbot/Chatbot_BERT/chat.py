import json
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
from torch.nn.utils.rnn import pad_sequence
from sklearn.preprocessing import LabelEncoder

# Step 1: Load intents.json file
with open('intent.json', 'r') as file:
    intents = json.load(file)

# Step 2: Tokenization
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Step 3: Building Vocabulary
vocab = tokenizer.get_vocab()

# Step 4: Input Preparation
inputs = []
outputs = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokenized = tokenizer.tokenize(pattern)
        indexed = tokenizer.convert_tokens_to_ids(tokenized)
        inputs.append(indexed)
        outputs.append(intent['tag'])

# Step 5: Label Encoding
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(outputs)

class IntentDataset(Dataset):
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        input_ids = torch.tensor(self.inputs[index])
        attention_mask = torch.ones_like(input_ids)
        label = torch.tensor(self.outputs[index], dtype=torch.long)  # Specify the dtype as torch.long
        return input_ids, attention_mask, label

# Step 6: Create Dataset and Dataloader
dataset = IntentDataset(inputs, encoded_labels)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Step 6: Model Architecture
class AttentionModel(nn.Module):
    def __init__(self, num_classes):
        super(AttentionModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.fc = nn.Linear(768, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask)
        last_hidden_state = outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0]
        logits = self.fc(pooled_output)
        return logits
def collate_fn(batch):
    input_ids, attention_masks, labels = zip(*batch)
    input_ids = pad_sequence(input_ids, batch_first=True)
    attention_masks = pad_sequence(attention_masks, batch_first=True)
    labels = torch.tensor([int(label) for label in labels])  # Convert labels to integers and then to a tensor
    return input_ids, attention_masks, labels

dataset = IntentDataset(inputs, encoded_labels)

dataloader = DataLoader(dataset, batch_size=16, shuffle=True, collate_fn=collate_fn)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AttentionModel(num_classes=len(intents['intents']))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100
for epoch in range(num_epochs):
    total_loss = 0.0
    for batch in dataloader:
        input_ids, attention_mask, labels = batch
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = model(input_ids, attention_mask)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss}')


# Step 7: Model Evaluation
def evaluate(model, question):
    tokenized = tokenizer.tokenize(question)
    indexed = tokenizer.convert_tokens_to_ids(tokenized)
    input_ids = torch.tensor(indexed).unsqueeze(0)
    attention_mask = torch.ones_like(input_ids)
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        _, predicted = torch.max(logits, 1)
        predicted_label = intents['intents'][predicted.item()]['tag']
        responses = [intent['responses'] for intent in intents['intents'] if intent['tag'] == predicted_label]
        if responses:
            response = random.choice(responses[0])
        else:
            response = "Sorry, I couldn't understand your question."

    return predicted_label, response

# Example usage
#question = "Hello, how are you?"
#predicted_label, response = evaluate(model, question)
#print(f'Question: {question}')
#print(f'Predicted Label: {predicted_label}')
#print(f'Response: {response}')

# Step 8: Inference
while True:
    question = input("User: ")
    predicted_label, response = evaluate(model, question)
    print("Predicted Label:", predicted_label)  # Print the predicted label
    if predicted_label == 'noanswer':
        print("Bot: Sorry, I couldn't understand your question.")
    else:
        print("Bot: " + response)
