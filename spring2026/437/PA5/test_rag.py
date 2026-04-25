import ollama
from sentence_transformers import SentenceTransformer, util
import torch
# 1. the knowledge (usually this comes from your wiki caache)
passages = [
    "Alexander Fleming discovered penicillin in 1928 at St. Mary's Hospital.", 
    "The capital of France is Paris, known for the Eiffel Tower.",
    "Python is a high-level programming language created by Guido van Rossum."
]
# 2. setup retrieval (the linear algebra part!)
# this model converts text into a 384-dimensional vector
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
passage_embeddings = embed_model.encode(passages, convert_to_tensor=True)
# 3. the user question
question = "who found penicillin?"
query_embedding = embed_model.encode(question, convert_to_tensor=True)
# 4. retrieval via cosine similarity
# finding the 'closest' vector in 384D space
scores = util.cos_sim(query_embedding, passage_embeddings)[0]
best_idx = torch.argmax(scores).item()
evidence = passages[best_idx]
print(f"--- top evidence found ---\n{evidence}\n")
# 5. generation via ollama
response = ollama.chat(model='llama0.21.2', messages=[
    {'role': 'system', 'content': 'answer the question using only the provided evidence.'},
    {'role': 'user', 'content': f"evidence: {evidence}\nquestion: {question}"}
])
print(f"--- final answer ---\n{response['message']['content']}")