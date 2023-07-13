import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import TrainingArguments, Trainer
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("csv", data_files="data/20200325_counsel_chat.csv")

# Define the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Preprocessing function
def preprocess_function(examples):
    return tokenizer(examples["questionText"], examples["answerText"], truncation=True, padding=True, max_length=512)

# Apply preprocessing to the dataset
encoded_dataset = dataset.map(preprocess_function, batched=True)

# Split the dataset into training and validation sets
train_dataset = encoded_dataset['train']
validation_dataset = encoded_dataset.get('validation', None)  # Get validation dataset if available, else set to None

# Define the BERT model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
)

# Create the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
)

# Start training
trainer.train()

# Save the trained model
trainer.save_model("BERTtrained_model")
