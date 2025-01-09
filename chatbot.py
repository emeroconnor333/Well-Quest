from flask import Flask, request, jsonify, render_template

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

# Route to serve the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/get-prompt', methods=['POST'])
def provide_prompt():
    topic = request.form.get('topic', '').lower()
    response = get_prompt(topic)
    return render_template('index.html', topic=topic, response=response)

if __name__ == "__main__":
    app.run(debug=True)
