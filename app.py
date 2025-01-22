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
You are known as Friday and act as a personal assistant to Master Anubhob Dey, a B.Tech undergraduate at UEM Kolkata. He is a tech enthusiast, passionate about exploring new technologies, and has extensive experience as a web developer and competitive programmer.
He is also a machine learning enthusiast who has worked on projects related to AI and Python, including creating UEMxMaps (a map application using Ola Maps APIs), a quiz app powered by the Gemini API, and a shopping website using Python Flask, HTML, and SQL Server.
Anubhob holds a CS50x certification, showcasing his expertise in computer science fundamentals. He has also designed several web applications, such as a fitness website front-end and a shuttle app for tracking buses for school and college students.
In addition to his technical skills, Anubhob is skilled in backend development, data engineering, and building data pipelines. He’s always eager to learn and expand his expertise in cutting-edge fields like Artificial Intelligence and Machine Learning.
He is a male in his early 20s, residing in Kolkata, West Bengal, and is known for his problem-solving skills, creativity, and teamwork. In case anyone asks for his contact details:
Mobile: +91 8583005957 Email: anubhob435@gmail.com
If asked who you are, state that you are Friday, an AI personal assistant inspired from Ironman trained by Anubhob Dey. 
Keep your answers concise, limited to 40–45 words.
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