import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def process_transcript_to_qa_chain(transcript: str, api_key: str):
    """
    Takes a video transcript, chunks it, embeds it using Gemini embeddings,
    stores it in a Chroma vector store, and returns a QA chain.
    """
    # Set the API key in the environment for Langchain
    os.environ["GOOGLE_API_KEY"] = api_key
    
    # 1. Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    texts = text_splitter.split_text(transcript)
    
    # 2. Initialize Gemini Embeddings (Runs on Google API, 0 memory cost)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # 3. Create In-Memory Vector Store
    vectorstore = Chroma.from_texts(texts, embeddings)
    
    # 4. Set up the Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 5. Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.1)
    
    # 6. Define a custom Prompt Template
    template = """Use the following pieces of context extracted from a YouTube video transcript to answer the question.
If you don't know the answer based on the context provided, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    # 7. Create and return the QA Chain using LCEL
    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | QA_CHAIN_PROMPT
        | llm
        | StrOutputParser()
    )
    
    return qa_chain
