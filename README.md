# 🤖 AI-Powered FAQ Chatbot (Flask)

An intelligent question answering system for companies that combines
semantic search over internal FAQs with Google Gemini LLM as a fallback.

---------------------------------

## 📌 Overview

This project is a Flask-based web application that answers user questions in Persian.
It first searches for the most relevant answer from a predefined FAQ knowledge base
using sentence embeddings. If no close match is found, it queries the Gemini API
and dynamically expands the knowledge base.

---------------------------------

## 🚀 Features

- Semantic search using Sentence Transformers
- Multilingual embedding model
- Automatic fallback to Google Gemini API
- Dynamic FAQ expansion
- Simple and clean UI
- Flask-based lightweight web app
- Environment variable-based API key security

---------------------------------

## 🧠 How It Works

1. User submits a question
2. The question is converted into a vector embedding
3. Similarity is calculated against internal FAQ embeddings
4. If similarity score > threshold → return FAQ answer
5. Otherwise → ask Gemini API and store the new Q&A

---------------------------------

## 🛠 Technologies Used

- Python
- Flask
- Sentence Transformers
- PyTorch
- Google Gemini API
- HTML & CSS

---------------------------------

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/USERNAME/ai-faq-chatbot-flask.git
cd ai-faq-chatbot-flask

---------------------------------

## 2. Create virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

---------------------------------

3. Install dependencies

pip install -r requirements.txt

---------------------------------

🔐 Environment Variables
Set your Gemini API key as an environment variable:
Windows (PowerShell)

setx GEMINI_API_KEY "YOUR_API_KEY"

---------------------------------

Linux / macOS

export GEMINI_API_KEY="YOUR_API_KEY"

---------------------------------

▶️ Run the Application

python app.py

---------------------------------

The application will automatically open in your browser at:

http://127.0.0.1:5000

---------------------------------

📷 Screenshots

---------------------------------

⚠️ Notes
This project is intended for educational and demo purposes
Do not expose your API keys in public repositories

---------------------------------

📄 License

MIT License

---------------------------------

# 5️⃣ requirements.txt
flask
sentence-transformers
torch
requests

```bash
