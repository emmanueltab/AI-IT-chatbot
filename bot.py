import json
import os
import openai
import re

# Make sure your environment variable is named OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define common stop words
STOP_WORDS = {"the", "for", "when", "a", "my", "to", "in", "on", "and", "is", "it", "of", "an", "or", "with", "at", "by"}

def clean_text(text):
    """
    1. Lowercases the text
    2. Removes punctuation/special characters
    3. Removes common stop words
    Returns a list of meaningful words
    """
    # Lowercase and remove non-alphanumeric characters
    text = re.sub(r"[^a-z0-9\s]", "", text.lower())
    # Split into words and filter out stop words
    words = [word for word in text.split() if word not in STOP_WORDS]
    return words

def find_best_article(question, kb):
    question_words = clean_text(question)
    best_article = None
    best_score = 0

    for article in kb:
        content_words = clean_text(article["title"] + " " + article["content"])
        # Score = number of matching words
        score = sum(1 for w in question_words if w in content_words)
        if score > best_score:
            best_score = score
            best_article = article

    return best_article

# Load knowledge base
with open("kb.json") as f:
    kb = json.load(f)["articles"]

# main:
if __name__ == "__main__":
    print(find_best_article("my laptop cant connect to the wifi", kb))