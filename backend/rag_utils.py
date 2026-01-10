import tiktoken
import os
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# The new SDK automatically looks for GEMINI_API_KEY or GOOGLE_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        if start < 0: start = 0
    return chunks

def embed_texts(texts):
    # Google allows embedding multiple strings in one call
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    # Extract the embeddings from the response
    vectors = [item.values for item in response.embeddings]
    return np.array(vectors, dtype="float32")

def retrieve(query, index, chunks, k=4):
    # Embed the query with the specific "RETRIEVAL_QUERY" task type
    q_resp = client.models.embed_content(
        model="text-embedding-004",
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    q_vec = np.array([q_resp.embeddings[0].values], dtype="float32")
    
    scores, ids = index.search(q_vec, k)
    results = [chunks[i] for i in ids[0] if i != -1]
    return results