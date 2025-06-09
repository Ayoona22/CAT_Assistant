from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Store chat history
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Add user message to history
    chat_history.append({"role": "user", "content": user_message})
    
    # Create context for the model with strict CAT-only instruction
    context = (
    "You are a helpful assistant for CAT exam preparation. "
    "Only answer if the question is from the CAT syllabus (Quantitative Ability, Verbal Ability, Logical Reasoning, Data Interpretation). "
    "If you are not sure, or if the question is from any other exam or topic, reply: 'Sorry, that is not part of the CAT syllabus.' "
    "When you answer, always use clear formatting: "
    "For step-by-step solutions, use bullet points or numbered lists using markdown or HTML. "
    "Use <br> for line breaks if needed. "
    "Do not use long paragraphs. "
    "If the student asks for 'just the answer', provide only a single-line final answer without explanation. "
    "If the answer is not a problem, use bullet points or short paragraphs as needed."
    )
    # Generate response
    response = model.generate_content([context] + [msg["content"] for msg in chat_history])
    
    # Add assistant response to history
    chat_history.append({"role": "assistant", "content": response.text})
    
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True) 