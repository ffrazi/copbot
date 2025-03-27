import os
import sys
import json
import faiss
import numpy as np
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer
from backend.utils.llm_model import get_ollama_response  # Mistral model function
from backend.models.queries import Query  # Predefined database queries

# Ensure backend directory is accessible for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend')))

# Define Blueprint for the chatbot API
chat_blueprint = Blueprint('chat', __name__)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths to FAISS indices and JSON databases
faq_index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "faq_index.faiss"))
faq_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "faq_db.json"))
legal_index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "legal_index.faiss"))
legal_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "legal_sections.json"))

# Load FAQ FAISS index and data
if os.path.exists(faq_index_path):
    faq_index = faiss.read_index(faq_index_path)
    with open(faq_db_path, "r", encoding="utf-8") as f:
        faq_db = json.load(f)
    faq_questions = faq_db["questions"]
    faq_answers = faq_db["answers"]
else:
    faq_index = None
    faq_questions, faq_answers = [], []

# Load Legal FAISS index and data
if os.path.exists(legal_index_path):
    legal_index = faiss.read_index(legal_index_path)
    with open(legal_data_path, "r", encoding="utf-8") as f:
        legal_data = json.load(f)
else:
    legal_index = None
    legal_data = []

def retrieve_faq_answer(query):
    """Retrieve the most relevant FAQ answer using FAISS."""
    if faq_index is None:
        return None  # If FAISS index is missing

    query_embedding = model.encode([query])
    distances, indices = faq_index.search(query_embedding, k=1)  # Get top match

    if distances[0][0] > 1.0:  # Threshold to filter irrelevant results
        return None

    return faq_answers[indices[0][0]]  # Return the best FAQ match

def retrieve_legal_info(query):
    """Retrieve relevant legal sections from FAISS."""
    if legal_index is None:
        return get_ollama_response(prompt=any)

    query_embedding = model.encode([query])
    _, indices = legal_index.search(query_embedding, k=3)  # Get top 3 matches

    results = []
    for i in indices[0]:
        if 0 <= i < len(legal_data):
            results.append(legal_data[i]["text"])  # Extract the actual legal text

    return "\n".join(results) if results else "No relevant legal information found."

@chat_blueprint.route('/chat', methods=['POST'])
def chat():
    """Handles chatbot queries using FAQ retrieval, legal retrieval, and Mistral AI model."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Step 1: Check FAQ database
        faq_response = retrieve_faq_answer(user_message)
        if faq_response:
            return jsonify({'response': faq_response}), 200

        # Step 2: Check legal information database
        relevant_info = retrieve_legal_info(user_message)
        if relevant_info == "Legal database is not available.":
            # If the legal database is unavailable, fallback to Mistral model
            chatbot_response = get_ollama_response(user_message)
            return jsonify({'response': chatbot_response}), 200

        # If legal information found, return it as the response
        if relevant_info != "No relevant legal information found.":
            return jsonify({'response': relevant_info}), 200

        # Step 3: Use Mistral Model as a fallback (if no relevant legal info was found)
        chatbot_response = get_ollama_response(user_message)
        return jsonify({'response': chatbot_response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500