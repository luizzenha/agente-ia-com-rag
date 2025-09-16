
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import Runnable
from typing import Any
from formatters import formatar_citacoes
from typing import Dict


def perguntar_politica_RAG(pergunta: str, retriever: VectorStoreRetriever, document_chain: Runnable[dict[str, Any], Any]) -> Dict:
    docs_relacionados = retriever.invoke(pergunta)

    if not docs_relacionados:
        return {"answer": "Não sei.",
                "citacoes": [],
                "contexto_encontrado": False}

    answer = document_chain.invoke({"input": pergunta,
                                    "context": docs_relacionados})

    txt = (answer or "").strip()

    if txt.rstrip(".!?") == "Não sei":
        return {"answer": "Não sei.",
                "citacoes": [],
                "contexto_encontrado": False}

    return {"answer": txt,
            "citacoes": formatar_citacoes(docs_relacionados, pergunta),
            "contexto_encontrado": True}