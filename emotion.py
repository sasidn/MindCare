from transformers import pipeline

def predict_emotions(input_text):
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest",return_all_scores=True)
    emotions = pipe(input_text)
    print(emotions)
    predicted_emotion = emotions[0][0]['label']
    return predicted_emotion

# Example usage
user_input = input("Enter your message: ")
predicted_emotion = predict_emotions(user_input)
print("Predicted Emotion:", predicted_emotion)

