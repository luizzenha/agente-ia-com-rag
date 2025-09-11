from langchain_core import embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from typing import List

def embed(api_key: str):
    embeddings = GoogleGenerativeAIEmbeddings(
        api_key=api_key,
        model="models/gemini-embedding-001"
    )
    return embeddings

def LoadRetriever(chunks: List[Document], api_key: str):
    embeddings = embed(api_key)
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4}
    )
    return retriever