import json
import os
import re
import csv
from datetime import datetime
import subprocess

# -----------------------------
# Config
# -----------------------------
OLLAMA_MODEL = "llama3.2:3b"  # Small local model, fast and accurateclient = OpenAI()   # Reads OPENAI_API_KEY automatically from environment

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

def ask_ollama(user_question, kb_article):
    """
    Returns a polished step-by-step answer using a local Ollama LLM.
    """
    prompt = f"""
You are an IT helpdesk assistant.
User question: "{user_question}"
Use this article to answer:
"{kb_article['content']}"

Give a clear, step-by-step solution for the user.
If you cannot fully explain, suggest escalating to a human technician.
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:3b", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = result.stdout.decode("utf-8").strip()
        if not output:
            return f"Error: {result.stderr.decode('utf-8').strip()}"
        return output
    except Exception as e:
        return f"Error running Ollama: {e}"


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# -----------------------------
# Load Knowledge Base
# -----------------------------
with open("kb.json") as f:
    kb = json.load(f)["articles"]

# -----------------------------
# Logs Interactions for Data Analysis 
# -----------------------------
def log_interaction(question, article_title, success=None):
    """
    Logs each user interaction to 'chat_log.csv'.
    success: optional flag (True/False) to indicate if the solution worked
    """
    with open("chat_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), question, article_title, success])
        
# -----------------------------
# Main Loop
# -----------------------------
if __name__ == "__main__":
    clear_terminal()
    print("AI Helpdesk Chatbot (local mode)")

    while True:
        user_input = input("\nAsk a question (or type 'quit')\n > ").strip()
        if user_input.lower() == "quit":
            break

        article = find_best_article(user_input, kb)

        if article:
            print("\nMatched article:", article["title"])
            answer = ask_ollama(user_input, article)
            print("\nAI Answer:\n", answer)

            # Ask if the solution helped
            success_input = input("Did this solution help? (y/n) > ").lower()
            success = success_input == "y"
            log_interaction(user_input, article["title"], success)

        else:
            print("No relevant article found. Try rephrasing your question.")
            log_interaction(user_input, "No Match", success=False)



