# Define a list of pairs containing patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how are you?"]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there"]
    ],
    [
        r"what is your name?",
        ["I am a chatbot. You can call me whatever you like."]
    ],
    [
        r"how are you?",
        ["I'm doing well, thank you! How can I help you today?"]
    ],
    [
        r"(.*)help(.*)",
        ["I'm here to help you. Please tell me what you need assistance with."]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day."]
    ],
[
        r"what is mental health?",
        ["Mental health includes our emotional, psychological, and social well-being. It affects the way we think, feel, and act, and determines how we handle stress, relate to others, and make choices in life [1]."]
    ],
    [
        r"what are mental health chatbots?",
        ["Mental health chatbots are a type of artificial intelligence (AI) that are designed to help people with their mental health. They can provide support, advice, and coping strategies for a variety of mental health issues, including anxiety, depression, stress, and addiction [3]."]
    ],
    [
        r"how can mental health chatbots help?",
        ["Mental health chatbots can provide immediate assistance to those in need, without the fear of judgment or the need to wait for an appointment. They can track your responses over time and offer coping strategies for when you're feeling down."]
    ],
    [
        r"what are the best mental health chatbots?",
        ["Some of the best mental health chatbots include Youper, Woebot, and Wysa. These chatbots use cognitive behavioral therapy and positive psychology techniques to help users manage their mental health [3]."]
    ],
    [
        r"what are the challenges of developing a mental health chatbot?",
        ["Developing a conversational AI for mental health is challenging because it requires a deep understanding of the complexities of human emotions and behavior. It also requires a large and diverse dataset of mental health information and resources, as well as ongoing updates and improvements to ensure accuracy and relevance [6]."]
    ],
    [
        r"can mental health chatbots replace real-life human interactions with a healthcare professional?",
        ["No, mental health chatbots cannot replace real-life human interactions with a healthcare professional. Both patients and therapists agree that mental health chatbots could help clients better manage their own mental health, but they are not a replacement for in-person therapy [2]."]
    ],
    [
        r"what are the two main approaches to developing a therapeutic chatbot?",
        ["The two main approaches to developing a therapeutic chatbot include goal-oriented and open-ended models, with correspondingly guided and free-flow dialog patterns. Goal-oriented chatbots are designed to achieve specific objectives, while open-ended chatbots allow for more free-form and exploratory conversations [2]."]
    ],
    [
        r"what are some of the best tools for building and maintaining a mental health chatbot?",
        ["Some of the best tools for building and maintaining a mental health chatbot are DialogFlow and Rasa. These platforms provide natural language processing (NLP) capabilities, as well as tools for training and testing chatbots [2]."]
    ],
    [
        r"what is cognitive behavioral therapy?",
        ["Cognitive behavioral therapy (CBT) is a type of talk therapy that focuses on changing negative patterns of thinking and behavior. It is a widely used and effective treatment for a variety of mental health issues, including anxiety, depression, and addiction [3]."]
    ],
    [
        r"what is positive psychology?",
        ["Positive psychology is a branch of psychology that focuses on the study of positive emotions, character strengths, and virtues. It emphasizes the importance of cultivating positive experiences and relationships, and has been shown to improve mental health and well-being [3]."]
    ]
]