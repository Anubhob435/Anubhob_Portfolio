# Anubhob's Portfolio Website

This is the source code for Anubhob Dey's portfolio website. The website showcases Anubhob's skills, projects, and contact information. It also includes a chatbot named "Friday" that acts as a personal assistant.

## Features

- Responsive design
- Dark mode toggle
- Scroll reveal animations
- Chatbot assistant
- Project showcase
- Contact form

## Technologies Used

- HTML
- CSS
- JavaScript
- Flask
- Google Gemini API

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Anubhob_Portfolio.git
   cd Anubhob_Portfolio
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Run the Flask application:
   ```sh
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000` to view the website.

## Deployment

To deploy the website, you can use platforms like Render, Heroku, or any other hosting service that supports Python/Flask applications.

## License

This project is licensed under the MIT License.
