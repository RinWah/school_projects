import os
import wikipediaapi
import ollama
from sentence_transformers import SentenceTransformer, util
import torch
# header comment for assignment
# cmsc 437 - NLP
# PA5 - retrieval-augmented generation
# rin pereira
# description: a RAG system using wikipedia as its source, dense embeddings, and ollama to answer questions.

# extra notes
# i chose dense retrival because it uses context instead of just simple word matches which can lead to better
# accuracy and better evidence retrieval. 
wiki = wikipediaapi.Wikipedia(
    user_agent="RinProject/1.0 (pereirar@vcu.edu)",
    language='en'
)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_rag_answer(question):
    topic_res = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': f"return only the wikipedia article title for this question. no punctuation, no sentences, no quotes. question: '{question}'"}
    ])
    topic = topic_res['message']['content'].strip().split('\n')[0].replace('"', '').replace('.', '')
    print(f"---- debug: searching wikipedia for topic: [{topic}] ----")
    
    cache_path = f"cache/{topic.replace(' ', '_')}.txt"
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            wiki_text = f.read()
    else:
        page = wiki.page(topic)
        if not page.exists(): 
            return "topic not found on wikipedia.", ["n/a", "n/a"]
        wiki_text = page.text
        os.makedirs("cache", exist_ok=True)
        with open(cache_path, 'w') as f:
            f.write(wiki_text)
    passages = [wiki_text[i:i+600] for i in range(0, len(wiki_text), 500)]
    passage_embeddings = embed_model.encode(passages, convert_to_tensor=True)
    query_embedding = embed_model.encode(question, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, passage_embeddings)[0]
    top_k_indices = torch.topk(scores, k=2).indices
    confidence = float(scores[top_k_indices[0]]) * 100
    evidence = [passages[i] for i in top_k_indices]
    context = "\n".join(evidence)
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': 'answer concisely using only the evidence provided.'},
        {'role': 'user', 'content': f"evidence: {context}\nquestion: {question}"}
    ])
    return response['message']['content'], evidence, confidence, topic
user_q = input("question: ")
answer, support, conf, wiki_topic = get_rag_answer(user_q)
print("\n" + "="*30)
print(f"confidence level: {conf: 2f}%")
print(f"source: https://en.wikipedia.org/wiki/{wiki_topic.replace(' ', '_')}")
print("="*30)
print(f"\n[answer]: {answer}")
print(f"\n[evidence]:\n1. {support[0]}\n2. {support[1]}")