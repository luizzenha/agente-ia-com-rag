from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import Runnable
from typing import Any, Dict
from agent_state import AgentState
from rag import perguntar_politica_RAG
from triagem_out import TriagemOut
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from statics import TRIAGEM_PROMPT, AUTO_RESOLVER, PEDIR_INFO, ABRIR_CHAMADO


def triagem(mensagem: str, llm: ChatGoogleGenerativeAI) -> Dict:
    triagem_chain = llm.with_structured_output(TriagemOut)
    saida: TriagemOut = triagem_chain.invoke([
        SystemMessage(content=TRIAGEM_PROMPT),
        HumanMessage(content=mensagem)
    ])
    return saida.model_dump()

def node_triagem(state: AgentState, llm: ChatGoogleGenerativeAI) -> AgentState:
    print("Executando nó de triagem...")
    return {"triagem": triagem(state["pergunta"], llm=llm)}

def node_auto_resolver(state: AgentState, retriever: VectorStoreRetriever, document_chain: Runnable[dict[str, Any], Any]) -> AgentState:
    print("Executando nó de auto_resolver...")
    resposta_rag = perguntar_politica_RAG(state["pergunta"], retriever, document_chain)

    update: AgentState = {
        "resposta": resposta_rag["answer"],
        "citacoes": resposta_rag.get("citacoes", []),
        "rag_sucesso": resposta_rag["contexto_encontrado"],
    }

    if resposta_rag["contexto_encontrado"]:
        update["acao_final"] = AUTO_RESOLVER

    return update

def node_pedir_info(state: AgentState) -> AgentState:
    print("Executando nó de pedir_info...")
    faltantes = state["triagem"].get("campos_faltantes", [])
    if faltantes:
        detalhe = ",".join(faltantes)
    else:
        detalhe = "Tema e contexto específico"

    return {
        "resposta": f"Para avançar, preciso que detalhe: {detalhe}",
        "citacoes": [],
        "acao_final": PEDIR_INFO
    }

def node_abrir_chamado(state: AgentState) -> AgentState:
    print("Executando nó de abrir_chamado...")
    triagem = state["triagem"]

    return {
        "resposta": f"Abrindo chamado com urgência {triagem['urgencia']}. Descrição: {state['pergunta'][:140]}",
        "citacoes": [],
        "acao_final":   ABRIR_CHAMADO
    }