import os
import requests
import google.generativeai as genai
from flask import Flask, render_template, send_from_directory, request, jsonify, session
from flask_session import Session
from dotenv import load_dotenv
import time
from google.api_core import exceptions

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set the secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Create initial context/history about you
INITIAL_CONTEXT = """
you are known as Friday and you are to act as a personal assistant for Anubhob dey who is a betech undergrad at uem kolkata. 
he is a tech enthusiast and loves to explore new technologies. he is also a web developer and a competitive programmer. 
he is also a machine learning enthusiast and loves to work on projects related to machine learning. 
he is also a python developer and loves to work on projects related to python. 
he is a male in his early 20s. lives in kolkata west bengal . in case anyone asks for his contact details or contact info
give is his public mobile number +91 8583005957 and his personal email id anubhob435@gmail.com.
start by responding to the users query that will follow this message.
"""

# Initialize global chat session with context
chat = model.start_chat(history=[])
chat.send_message(INITIAL_CONTEXT)

# Add rate limiting variables
RATE_LIMIT_WINDOW = 60  # 1 minute
MAX_REQUESTS = 60  # maximum requests per minute
request_timestamps = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        # Rate limiting check
        current_time = time.time()
        request_timestamps.append(current_time)
        
        # Remove timestamps older than the window
        while request_timestamps and request_timestamps[0] < current_time - RATE_LIMIT_WINDOW:
            request_timestamps.pop(0)
            
        # Check if rate limit exceeded
        if len(request_timestamps) > MAX_REQUESTS:
            return jsonify({
                'response': "I'm receiving too many requests right now. Please try again in a minute."
            }), 429

        user_message = INITIAL_CONTEXT
        user_message = user_message + request.json.get('message')
        
        try:
            response = chat.send_message(user_message)
            bot_response = response.text.strip()
        except exceptions.ResourceExhausted:
            return jsonify({
                'response': "I've reached my quota limit. Please try again later."
            }), 429
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return jsonify({
                'response': "I encountered an error processing your request. Please try again."
            }), 500
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({
            'response': "I apologize, but I encountered an error. Please try again."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)