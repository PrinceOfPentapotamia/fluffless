# ✨ Fluffless

**STOP THE FLUFF. GET THE FACTS.**

Fluffless is an AI-powered brutalist web application designed to instantly debunk clickbait YouTube videos. Just paste a URL, and Fluffless will fetch the transcript, run it through an embedded local LLM architecture, and instantly give you the core answer the video is trying to hide from you.

## 🚀 Features
- **Instant Auto-Debunk:** Automatically cuts through clickbait and answers the core question of the video title.
- **RAG Chat Interface:** Ask follow-up questions about the video's content.
- **Context Stuffing**: Bypasses rate limits and memory issues by stuffing the entire video transcript directly into Gemini 1.5's massive 1M token context window for highly accurate, holistic summaries.
- **Brutalist UI:** A custom-built, striking, high-contrast user interface.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **AI/LLM:** LangChain, Google Gemini API, HuggingFace Local Embeddings
- **Vector Database:** ChromaDB

## 📦 Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PrinceOfPentapotamia/fluffless.git
   cd fluffless
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

5. **Run the Application:**
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
   Open `http://127.0.0.1:8000` in your browser.

## ⚠️ Note on SSL (Corporate Firewalls)
This application includes monkey-patches for `requests` and `httpx` to bypass SSL verification errors common in corporate environments (e.g., Zscaler). 

## 📝 License
MIT License

## 🔒 Privacy Policy
Please read our [Privacy Policy](PRIVACY_POLICY.md) to understand how data is handled in this local-first application.
