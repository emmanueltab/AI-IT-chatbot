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

def ask_openai(user_question, kb_article):
    """
    Sends the user question and KB article to OpenAI 
    Returns a clear step-by-step answer
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
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"





# Load knowledge base
with open("kb.json") as f:
    kb = json.load(f)["articles"]

# main:
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk a question (or type 'quit')\n >")
        if user_input == quit:
            break 


        article = find_best_article(user_input, kb)

        if article:
            print("\nMatched article:", article["title"])
            answer = ask_openai(user_input, article)
            print("\nAI Answer:\n", answer)
        else:
            print("No relevant article found. Try rephrasing your question.")