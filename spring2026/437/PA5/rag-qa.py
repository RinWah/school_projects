import os
import wikipediaapi
import ollama
from sentence_transformers import SentenceTransformer, util
import torch

wiki = wikipediaapi.Wikipedia(
    user_agent="RinProject/1.0 (pereirar@vcu.edu)",
    languages='en'
)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_rag_answer(question):
    topic_res = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': f"provide only the wikipedia article title for '{question}'"}
    ])
    topic = topic_res['message']['content'].strip().replace('"', '')
    
    cache+path = f"cache/{topic.replace(' ', '_')}.txt"
    