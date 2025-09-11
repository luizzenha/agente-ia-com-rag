from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

def load_policies() -> List[Document]:
    docs = []
    for pdf in Path("./pdfs").glob("**/*.pdf"):
        try:
            loader = PyMuPDFLoader(str(pdf))
            docs.extend(loader.load())
            print(f"Arquivo {pdf} carregado com sucesso \n")
        except Exception as e:
            print(f"Erro ao carregar o arquivo {pdf}: {e}")
    return docs


def split_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    return splitter.split_documents(docs)

def LoadChunks(): return split_docs(load_policies())

