# main terminal chatbot (OpenAi + retrival + ticket saving)
import json 

with open("kb.json") as f:
    kb = json.load(f)["articles"]

# scans through the words in the question. 
# selects the article that best fits. 
def find_best_article(question, kb):
    question = question.lower()
    best_article = None 
    best_score = 0 

    for aticle in kb:
        score = 0 
        for word in question.split():
            if word in aticle["content"].lower() or word in article["title"].lower():
                score += 1 

        if score > best_score:
            best_score = score
            best_atcile = article 

    return best_article