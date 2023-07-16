from transformers import pipeline


def predict_emotions(input_text):
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest",
                    top_k=None)
    emotions = pipe(input_text)
    print(emotions)

    predicted_emotions = []
    for emotion in emotions[0]:
        label = emotion['label']
        score = emotion['score']
        predicted_emotions.append((label, score))

    return predicted_emotions


# Example usage
user_input = input("Enter your message: ")
predicted_emotions = predict_emotions(user_input)
print("Predicted Emotions:")
for emotion in predicted_emotions:
    label, score = emotion
    print(f"Label: {label}, Score: {score}")


