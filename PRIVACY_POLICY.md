# Privacy Policy

**Last Updated: July 18, 2026**

Fluffless is designed with privacy and transparency in mind. Because this is a self-hosted, local-first application, your data remains in your control.

## 1. Information Collection
**We do not collect, store, or sell your personal data.** 
When you run Fluffless locally on your own machine, all video processing and data extraction happens entirely on your hardware. We do not have servers monitoring your usage.

## 2. Third-Party Services
Fluffless relies on a few third-party services to function. When you use the app, data is transmitted to these providers according to their respective privacy policies:
- **YouTube:** Fluffless fetches video transcripts directly from YouTube. By providing a URL, you are requesting data from YouTube's servers.
- **Google Gemini API:** The transcript data (text) and your chat prompts are sent to Google's Gemini API to generate the answers. Please review Google's API Privacy Policy for details on how they handle API requests.
- **HuggingFace (Local):** Vector embeddings are generated locally on your machine using HuggingFace models, meaning none of your video data is sent to a third-party embedding provider.

## 3. Local Storage
Fluffless utilizes local storage (ChromaDB) on your machine to temporarily store vector embeddings for the purpose of chat history and contextual answering. This data never leaves your computer and is overwritten or deleted when you restart the application or process a new video.

## 4. Open Source
Fluffless is completely open source. You are encouraged to inspect the code to verify how your data is handled.

## 5. Contact
If you have any questions about this Privacy Policy, please open an issue on the GitHub repository.
