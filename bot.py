import json
import os
from openai import OpenAI
import re

# -----------------------------
# Config
# -----------------------------
USE_OPENAI = False  # Set True to use OpenAI API
client = OpenAI()   # Reads OPENAI_API_KEY automatically from environment

STOP_WORDS = {
    "the", "for", "when", "a", "my", "to", "in", "on", "and",
    "is", "it", "of", "an", "or", "with", "at", "by"
}

# -----------------------------
# Helper Functions
# -----------------------------
def clean_text(text):
    """
    Lowercase, remove punctuation, remove stop words.
    Returns a list of meaningful words.
    """
    text = re.sub(r"[^a-z0-9\s]", "", text.lower())
    return [w for w in text.split() if w not in STOP_WORDS]

def find_best_article(question, kb):
    question_words = clean_text(question)
    best_article = None
    best_score = 0
    for article in kb:
        content_words = clean_text(article["title"] + " " + article["content"])
        score = sum(1 for w in question_words if w in content_words)
        if score > best_score:
            best_score = score
            best_article = article
    return best_article

def ask_openai(user_question, kb_article):
    """
    Returns a polished step-by-step answer.
    Uses mock response if USE_OPENAI = False
    """
    if not USE_OPENAI:
        return f"Step-by-step solution (mocked):\n{kb_article['content']}"

    prompt = f"""
You are an IT helpdesk assistant.
User question: "{user_question}"

Use this article to answer:
"{kb_article['content']}"

Give a clear, step-by-step solution for the user.
If you cannot fully explain, suggest escalating to a human technician.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# -----------------------------
# Load Knowledge Base
# -----------------------------
with open("kb.json") as f:
    kb = json.load(f)["articles"]

# -----------------------------
# Main Loop
# -----------------------------
if __name__ == "__main__":
    clear_terminal()
    print("AI Helpdesk Chatbot (mock mode)" if not USE_OPENAI else "AI Helpdesk Chatbot")

    while True:
        user_input = input("\nAsk a question (or type 'quit')\n > ")
        if user_input.lower() == "quit":
            break

        article = find_best_article(user_input, kb)
        if article:
            print("\nMatched article:", article["title"])
            answer = ask_openai(user_input, article)
            print("\nAI Answer:\n", answer)
        else:
            print("No relevant article found. Try rephrasing your question.")
