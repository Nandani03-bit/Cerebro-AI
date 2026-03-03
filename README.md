# Cerebro-AI
NLP-based intelligent chatbot using TF-IDF, Cosine Similarity, and Gemini AI fallback built using Python and Streamlit.
# 🤖 General Knowledge NLP Chatbot
### MCA Semester 2 - NLP Project

---

## 📌 Project Overview

This is an NLP-powered General Knowledge Chatbot built using Python.
It uses **TF-IDF vectorization** and **Cosine Similarity** to match
user questions to the most relevant answer from a knowledge base.

---

## 🧠 NLP Concepts Used

| Concept | What it does |
|---|---|
| **Tokenization** | Splits text into individual words |
| **Stopword Removal** | Removes common words like "is", "the", "what" |
| **Lemmatization** | Converts words to root form (running → run) |
| **TF-IDF** | Converts text to numerical vectors |
| **Cosine Similarity** | Finds the most similar question |

---

## 📁 Project Structure

```
nlp_chatbot/
│
├── app.py              ← Streamlit Web UI
├── chatbot.py          ← NLP Logic (core brain)
├── qa_data.py          ← Q&A Knowledge Base
├── requirements.txt    ← Required libraries
└── README.md           ← This file
```

---

## ⚙️ How to Run

### Step 1: Install Python
Make sure Python 3.8+ is installed on your system.

### Step 2: Install required libraries
Open terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3: Run the chatbot
```bash
streamlit run app.py
```

### Step 4: Open in browser
Streamlit will automatically open the chatbot in your browser.
If not, go to: **http://localhost:8501**

---

## 🔍 How It Works (Step-by-Step)

```
User types a question
        ↓
Text is preprocessed (lowercase → remove punctuation → tokenize → remove stopwords → lemmatize)
        ↓
Processed text is converted to TF-IDF vector
        ↓
Cosine similarity is calculated with all known questions
        ↓
The answer with highest similarity score is returned
```

---

## 📚 Topics Covered in Knowledge Base

- 🔬 **Science** – Photosynthesis, DNA, Gravity, Big Bang, Atoms
- 🗺️ **Geography** – Largest country, Longest river, Capitals
- 📜 **History** – World War 2, Gandhi, Moon landing, French Revolution
- 💻 **Technology** – Internet, AI, Machine Learning, Computers

---

## 🛠️ Libraries Used

- **Python** – Core programming language
- **NLTK** – Tokenization, stopwords, lemmatization
- **scikit-learn** – TF-IDF vectorization, cosine similarity
- **Streamlit** – Web interface

---

## ✏️ How to Add More Q&A Pairs

Open `qa_data.py` and add your questions and answers in this format:
```python
("Your question here?", "Your answer here."),
```

---

## 👨‍💻 Created By
MCA Semester 2 Student | NLP Subject Project
