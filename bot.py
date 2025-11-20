import json
import os
import openai
import re

# Make sure your environment variable is named OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load knowledge base
with open("kb.json") as f:
    kb = json.load(f)["articles"]

def clean_text(text):
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def find_best_article(question, kb):
    question_words = clean_text(question).spit()
    best_article = None
    best_score = 0

    for article in kb:
        # Combine title + content and clean it
        content_words = clean_text(article["title"] + " " + article["content"]).split()
        score = sum(1 for w in question_words if w in content_words)
        if score > best_score:
            best_score = score
            best_article = article

    return best_article

print(find_best_article("my laptop cant connect to the wifi", kb))