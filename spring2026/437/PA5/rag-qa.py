# step 1: document processing
# fetch text from wikipedia API
# split into chunks / passages
# generate embeddings for chunks using SentenceTransformers

# step 2: the retrieval 
# embed the user's question
# compare question vector vs passage vectors using cosine similarity
# grab top 3 passages

# step 3: generation 
# send 3 passages + question to ollama via local API
# printn answer
# print evidence with passages