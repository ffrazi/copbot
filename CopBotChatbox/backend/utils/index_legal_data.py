import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAQ data
faq_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "faq.json"))
with open(faq_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Extract questions and answers
questions = [entry["Question"] for entry in faq_data]
answers = [entry["Answer"] for entry in faq_data]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode questions into embeddings
question_embeddings = model.encode(questions)

# Create FAISS index
index = faiss.IndexFlatL2(question_embeddings.shape[1])
index.add(np.array(question_embeddings))

# Save FAISS index
faiss_index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "faq_index.faiss"))
faiss.write_index(index, faiss_index_path)

# Save questions and answers for retrieval
faq_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "faq_db.json"))
with open(faq_db_path, "w", encoding="utf-8") as f:
    json.dump({"questions": questions, "answers": answers}, f, indent=4)

print("✅ FAISS index and FAQ database saved successfully.")
