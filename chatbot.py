from flask import Flask, request, jsonify, render_template
from textblob import TextBlob

app = Flask(__name__)

# Journal prompts dictionary
prompts = {
    "stress": [
        "Write about what’s causing your stress today.",
        "List three ways to reduce your stress."
    ],
    "motivation": [
        "What motivates you to keep going?",
        "Write about a time you overcame a challenge."
    ]
}

# Function to get a prompt based on a topic
def get_prompt(topic):
    return prompts.get(topic, ["Sorry, I don't have prompts for that topic."])

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
