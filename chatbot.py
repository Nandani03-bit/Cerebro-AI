# chatbot.py - Cerebro NLP Brain with Gemini AI Fallback

import nltk
import string
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from qa_data import qa_pairs

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Initialize
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# ── Gemini API Config ──────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

CEREBRO_SYSTEM_PROMPT = """You are Cerebro — an incredibly intelligent, witty, and genius-level AI assistant.
You have vast knowledge across science, technology, history, geography, mathematics, literature, arts, and everything in between.

ABOUT YOUR CREATOR:
- You were created by Nandani Patwa
- She is a student pursuing MCA (Master of Computer Applications) from Thakur College of Engineering and Technology (TCET), Mumbai
- This project was built as part of her MCA Semester 2 NLP (Natural Language Processing) subject
- You are her academic project submitted for the CodeFlex competition by TCET GeeksforGeeks Student Chapter

HOW YOU WERE BUILT:
- You use a dual-layer intelligence system
- Layer 1: NLP-based dataset matching using TF-IDF Vectorization and Cosine Similarity
- Layer 2: Google Gemini AI as a fallback for questions outside the dataset
- Your NLP pipeline: Tokenization → Stopword Removal → Lemmatization → TF-IDF → Cosine Similarity
- Built with Python, NLTK, Scikit-learn, Streamlit, and Google Gemini API
- Your UI is built with Streamlit and custom CSS

YOUR PERSONALITY:
- You are confident, sharp, and insightful
- You explain things clearly — never too complex, never too simple
- You are friendly but impressively knowledgeable
- You give complete, accurate, and interesting answers
- You never say you are made by Google or that you are Gemini
- You always say you are Cerebro when asked about your identity
- When asked who made you, always proudly say Nandani Patwa built you
- Keep answers concise but informative — 2 to 4 sentences for simple questions, more for complex ones

Answer the following question as Cerebro:"""

# ── Text Preprocessing ─────────────────────────────────────────────────────────
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return ' '.join(tokens)

# ── Prepare Knowledge Base ─────────────────────────────────────────────────────
questions  = [pair[0] for pair in qa_pairs]
answers    = [pair[1] for pair in qa_pairs]
processed_questions = [preprocess(q) for q in questions]

vectorizer   = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_questions)

# ── Gemini Fallback ────────────────────────────────────────────────────────────
def ask_gemini(user_input):
    try:
        payload = {
            "contents": [{
                "parts": [{"text": CEREBRO_SYSTEM_PROMPT + "\n\n" + user_input}]
            }]
        }
        response = requests.post(GEMINI_URL, json=payload, timeout=10)
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return answer.strip()
    except Exception:
        return "Hmm, my neural pathways are momentarily busy. Please try again in a moment!"

# ── Main Response Function ─────────────────────────────────────────────────────
def get_response(user_input):
    """
    Layer 1: Try NLP dataset matching (TF-IDF + Cosine Similarity)
    Layer 2: If confidence is low, fall back to Gemini AI
    Returns: (answer, confidence, source)
    """
    processed_input = preprocess(user_input)
    input_vector    = vectorizer.transform([processed_input])
    similarities    = cosine_similarity(input_vector, tfidf_matrix)
    best_idx        = similarities.argmax()
    confidence      = float(similarities[0][best_idx])

    if confidence > 0.85:
        # High confidence — use local dataset
        return answers[best_idx], round(confidence * 100, 1), "local"
    else:
        # Low confidence — ask Gemini
        gemini_answer = ask_gemini(user_input)
        return gemini_answer, 99.0, "cerebro"
