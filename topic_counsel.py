import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import logging
from simpletransformers.t5 import T5Model, T5Args
from imblearn.over_sampling import RandomOverSampler
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def classify_topic(user_input):
    # Set device to CPU
    device = torch.device("cpu")

    # Initialize T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
    t5_model.to(device)

    # Read the CSV file and preprocess the data
    df = pd.read_csv('data/20200325_counsel_chat.csv')
    model_df = pd.DataFrame()
    model_df['q_text'] = df.questionText
    model_df['label'] = df.topic

    ros = RandomOverSampler()
    x_ros, y_ros = ros.fit_resample(
        np.array(model_df['q_text']).reshape(-1, 1),
        np.array(model_df['label']).reshape(-1, 1)
    )

    model_df_os = pd.DataFrame()
    model_df_os['q_text'] = x_ros.reshape(-1)
    model_df_os['label'] = y_ros

    le = LabelEncoder()
    labels = le.fit_transform(model_df_os.label)
    model_df_os['label'] = labels

    model_x_train, model_x_test, model_y_train, model_y_test = train_test_split(
        np.array(model_df_os.q_text),
        np.array(model_df_os.label),
        test_size=0.3,
        random_state=42
    )

    train_df = pd.DataFrame()
    train_df['q_text'] = model_x_train
    train_df['label'] = model_y_train

    test_df = pd.DataFrame()
    test_df['q_text'] = model_x_test
    test_df['label'] = model_y_test

    prefix_train = ['multi-class classification'] * train_df.shape[0]
    prefix_test = ['multi-class classification'] * test_df.shape[0]

    train_df.insert(0, 'prefix', prefix_train)
    train_df.rename(columns={'q_text': 'input_text', 'label': 'target_text'}, inplace=True)

    test_df.insert(0, 'prefix', prefix_test)
    test_df.rename(columns={'q_text': 'input_text', 'label': 'target_text'}, inplace=True)

    train_df['target_text'] = train_df['target_text'].astype(str)
    test_df['target_text'] = test_df['target_text'].astype(str)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.WARNING)

    # User input
    user_input = input("Enter your question: ")

    # Prepare input for classification
    input_prompt = "multi-class classification: " + user_input
    input_ids = tokenizer.encode(input_prompt, return_tensors="pt").to(device)

    # Generate classification output
    output = t5_model.generate(input_ids, max_length=100)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    print("Input Prompt:", input_prompt)
    print("Generated Text:", generated_text)

# Test the function
user_input = input("Enter your question: ")
classify_topic(user_input)
print(classify_topic)