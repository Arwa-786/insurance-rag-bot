import os
import faiss
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from pypdf import PdfReader
from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from rag_utils import chunk_text, embed_texts, retrieve

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
app = FastAPI()

# Allow your React app (usually on port 5173 or 3000) to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, "*" allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index = None
chunks = None

class ChatIn(BaseModel):
    message: str

def load_pdf_text(path):
    reader = PdfReader(path)
    return "".join([page.extract_text() for page in reader.pages])

@app.post("/ingest")
def ingest():
    global index, chunks
    text = load_pdf_text("data/knowledge.pdf")
    chunks = chunk_text(text)
    vectors = embed_texts(chunks)
    
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    
    faiss.write_index(index, "data/docs.index")
    with open("data/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    return {"status": "ok", "chunks": len(chunks)}

@app.post("/chat")
def chat(payload: ChatIn):
    global index, chunks
    if index is None:
        if os.path.exists("data/docs.index"):
            index = faiss.read_index("data/docs.index")
            with open("data/chunks.pkl", "rb") as f:
                chunks = pickle.load(f)
        else:
            return {"answer": "Knowledge base not ingested yet."}

    relevant_chunks = retrieve(payload.message, index, chunks)
    context = "\n\n".join(relevant_chunks)
    
    # Generate content using Gemini 2.0 Flash
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Context:\n{context}\n\nQuestion: {payload.message}",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful insurance assistant. Use only the provided context."
        )
    )
    
    return {"answer": response.text}