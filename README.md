# Helpdesk AI (Terminal) — Interview Project

## Summary
Terminal-based AI Helpdesk Chatbot with Data-Science Ticket Analytics.
- Uses OpenAI (Chat API) to answer IT questions using local KB + RAG-style retrieval.
- Stores every interaction as a ticket (JSON).
- `analysis.py` performs clustering (K-Means) and trains a small priority-prediction model (Logistic Regression).
- Terminal-based, minimal, and designed to demonstrate the data-science skills listed on a résumé.

## Files
- `bot.py` — main interactive chatbot (terminal)
- `analysis.py` — analytics, clustering, training priority model
- `kb.json` — knowledge base (starter)
- `tickets.json` — example tickets (starter)
- `models/` — where models are saved by `analysis.py`
- `requirements.txt` — python dependencies

## Setup
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
