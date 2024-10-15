import os
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure API key
api_key = "AIzaSyDxv2Ey_iCoPRvjNca9glID-dgbwXomXfk"
genai.configure(api_key=api_key)

# Model generation configuration
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative AI model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the prompt from the form
    prompt = request.form.get('prompt')

    # Check if prompt is provided
    if not prompt:
        return jsonify({"error": "Prompt is missing"}), 400
    
    # Check if the prompt is related to financial queries
    if not is_financial_query(prompt):
        return jsonify({"error": "The AI only responds to financial queries."}), 400

    # Start a chat session and send the financial prompt
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            }
        ]
    )

    response = chat_session.send_message(prompt)

    # Check and return the response
    if response:
        result = response.text
    else:
        result = "Error occurred while processing the query"

    return jsonify({"result": result})

def is_financial_query(prompt):
    # Basic financial keyword check, you can enhance this further
    financial_keywords = [
        'investment', 'stocks', 'finance', 'market', 'loan', 
        'bank', 'economy', 'cryptocurrency', 'trading', 'equity', 
        'bonds', 'mutual funds', 'forex', 'capital', 'tax', 'interest rate'
    ]
    return any(keyword in prompt.lower() for keyword in financial_keywords)

if __name__ == '__main__':
    app.run(debug=True, port=5656)