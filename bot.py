import json
import os
import openai

# Make sure your environment variable is named OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load knowledge base
with open("kb.json") as f:
    kb = json.load(f)["articles"]

# Find the best matching article based on keyword overlap
def find_best_article(question, kb):
    question = question.lower()
    best_article = None
    best_score = 0

    for article in kb:  # fixed typo
        score = 0
        for word in question.split():
            if word in article["content"].lower() or word in article["title"].lower():
                score += 1

        if score > best_score:
            best_score = score
            best_article = article  # fixed typo

    return best_article
