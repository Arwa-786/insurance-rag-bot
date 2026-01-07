import tiktoken
import os
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chunking Logic
def chunk_text(text: str, chunk_tokens: int = 450, overlap_tokens: int = 80):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_tokens
        chunk = enc.decode(tokens[start:end])
        chunks.append(chunk)
        start = end - overlap_tokens
        if start < 0:
            start = 0
    return chunks

# Embedding
def embed_texts(texts):
    # Turning texts into Searchable numbers
    resp = client.embeddings.create(
        model = "text-embedding-3-small",
        input = texts
    )
    vecotrs = [d.embedding for d in resp.data]
    return np.array(vectors, dtype="float32")

# Retreival
def retrieve(query, index, chunks, k=4):
    # Embed the user question
    q_resp = client.embeddings.create(
        model = "text-embedding-3-small",
        input=[query]   
    )
    q_vec = np.array([q_resp.data[0].embedding], dtype="float32")
    
    # Search the FAISS index
    scores, ids = index.search(q_vec, k)
    
    results = []
    for i in ids[0]:
        if i == -1: # No match found
            continue
        results.append(chunks[i])
    return results