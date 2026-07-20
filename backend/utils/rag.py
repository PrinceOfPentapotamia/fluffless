import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

class ContextStuffingQAChain:
    def __init__(self, transcript: str, api_key: str):
        self.transcript = transcript
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key
        )
        # We stuff the entire transcript into the system prompt. Gemini 1.5 has a 1M token context window!
        self.system_prompt = f"You are a helpful assistant. Answer the user's questions based ONLY on the following YouTube video transcript. If the answer is not in the transcript, say 'I cannot find the answer in the video.'\n\nTRANSCRIPT:\n{transcript}"

    def invoke(self, question: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=question)
        ]
        response = self.llm.invoke(messages)
        return response.content

def process_transcript_to_qa_chain(transcript: str, api_key: str):
    """
    Takes a raw transcript and returns a QA chain object that uses context stuffing.
    This completely bypasses the need for vector embeddings, ChromaDB, and embedding rate limits.
    """
    # 1. Disable all SSL warnings (due to Zscaler)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 2. Return the new chain
    return ContextStuffingQAChain(transcript, api_key)
