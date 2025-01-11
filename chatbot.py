from flask import Flask, request, jsonify, render_template
from textblob import TextBlob # for sentiment analysis
import re # keyword matching

app = Flask(__name__)

# Journal prompts dictionary
prompts = {
    "gratitude" : [
        "What was your favourite moment of this week?",
        "Who is someone that you feel grateful for?",
    ],
    "self-reflection" : [
        "What’s one thing you’ve learned about yourself recently?",
        "Describe a challenge you faced and how you overcame it.",
    ],
    "motivation": [
        "What motivates you to keep going?",
        "Write about a time you overcame a challenge.",
    ],
    "emotional awareness" : [
        "What emotions are you feeling right now? What might have caused them?",
        "Describe a time today when you felt your strongest emotion.",
    ],
    "stress": [
        "Write about what’s causing your stress today.",
        "List three ways to reduce your stress.",
    ],
}

# Keywords dictionary
keywords_to_topics = {
    # Gratitude
    "happy": "gratitude",
    "grateful": "gratitude",
    "joy": "gratitude",
    "thankful": "gratitude",
    "blessed": "gratitude",

    # Self-Reflection
    "fine": "self-reflection",
    "reflect": "self-reflection",
    "question": "self-reflection",
    "analyse": "self-reflection",
    "content": "self-reflection",

    # Motivation
    "procrastinate": "motivation",
    "lazy": "motivation",
    "goal": "motivation",
    "dream": "motivation",
    "inspired": "motivation",
    "productive": "motivation",

    # Emotional Awareness
    "sad": "emotional awareness",
    "down": "emotional awareness",
    "emotional": "emotional awareness",
    "upset": "emotional awareness",
    "hurt": "emotional awareness",
    "lonely": "emotional awareness",

    # Stress
    "worried": "stress",
    "anxious": "stress",
    "overwhelmed": "stress",
    "nervous": "stress",
    "stressed": "stress",
    "pressure": "stress",
}

def detect_keyword(text):
    for keyword, topic in keywords_to_topics.items():
        if re.search(rf"{keyword}", text, re.IGNORECASE):
            return topic
    return None # If no keyword matches

# Function to get a prompt based on a topic
def get_prompt(topic):
    return prompts.get(topic, ["Sorry, I don't have prompts for that topic."])

# Function to find the sentiment of the input
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# Route to serve the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/get-prompt', methods=['POST'])
def provide_prompt():
    user_input = request.form.get('topic', '')
    sentiment = analyze_sentiment(user_input)

    # get topic based on keyword
    topic = detect_keyword(user_input)

    # if no keywords found
    if not topic:
        # Map sentiment to appropriate topics
        if sentiment == "positive":
            topic = "gratitude"
        elif sentiment == "negative":
            topic = "stress"
        else:
            topic = "motivation"

    response = get_prompt(topic)
    return render_template('index.html', user_input=user_input, sentiment=sentiment, topic=topic, response=response)

if __name__ == "__main__":
    app.run(debug=True)
