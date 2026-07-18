from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import ssl
import requests
import urllib3
import httpx
import certifi

# 1. Disable all SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. Globally disable SSL verification in requests
old_request = requests.Session.request
def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)
requests.Session.request = new_request

# 3. Disable standard library SSL verification
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = certifi.where()

old_httpx_init = httpx.Client.__init__
def new_httpx_init(self, *args, **kwargs):
    kwargs['verify'] = False
    old_httpx_init(self, *args, **kwargs)
httpx.Client.__init__ = new_httpx_init

old_httpx_async_init = httpx.AsyncClient.__init__
def new_httpx_async_init(self, *args, **kwargs):
    kwargs['verify'] = False
    old_httpx_async_init(self, *args, **kwargs)
httpx.AsyncClient.__init__ = new_httpx_async_init

from dotenv import load_dotenv
load_dotenv()

from backend.utils.youtube import extract_video_id, get_transcript, get_video_title
from backend.utils.rag import process_transcript_to_qa_chain

app = FastAPI(title="Fluffless API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store for QA chains (Keyed by video ID)
qa_chains = {}

class ProcessRequest(BaseModel):
    url: str
    api_key: str | None = None

class ChatRequest(BaseModel):
    video_id: str
    question: str

@app.post("/api/process-video")
def process_video(req: ProcessRequest):
    video_id = extract_video_id(req.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    api_key = req.api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="Gemini API Key required")

    try:
        title = get_video_title(req.url)
        transcript = get_transcript(video_id)
        qa_chain = process_transcript_to_qa_chain(transcript, api_key)
        
        # Store for future chats
        qa_chains[video_id] = qa_chain
        
        # Auto-debunk
        auto_prompt = f"The title of this video is '{title}'. Based on the transcript, answer the core question posed by the title in 2-3 sentences. Cut straight to the point and do not use fluff."
        answer = qa_chain.invoke(auto_prompt)
        
        return {
            "video_id": video_id,
            "title": title,
            "debunk": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def chat(req: ChatRequest):
    qa_chain = qa_chains.get(req.video_id)
    if not qa_chain:
        raise HTTPException(status_code=404, detail="Video not processed yet")
    
    try:
        answer = qa_chain.invoke(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))
