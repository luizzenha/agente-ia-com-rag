import os
from functools import partial
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langgraph.graph import StateGraph, START, END
from chunks import LoadChunks
from embeddings import LoadRetriever
from agent_state import AgentState
from nodes import node_triagem, node_auto_resolver, node_pedir_info, node_abrir_chamado
from rules import decidir_pos_triagem, decidir_pos_auto_resolver
from statics import AUTO_RESOLVER, OK, PEDIR_INFO, ABRIR_CHAMADO

# Obtém a chave da API de uma variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida")

llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        api_key=GOOGLE_API_KEY
)


prompt_rag = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um Assistente de Políticas Internas (RH/IT) da empresa ReZenha Desenvolvimento. "
     "Responda SOMENTE com base no contexto fornecido. "
     "Se não houver base suficiente, responda apenas 'Não sei'."),

    ("human", "Pergunta: {input}\n\nContexto:\n{context}")
])

document_chain = create_stuff_documents_chain(
    llm,
    prompt=prompt_rag
)

# Carrega os chunks e o retriever
chunks = LoadChunks()
retriever = LoadRetriever(chunks, GOOGLE_API_KEY)

# Cria o grafo de workflow
workflow = StateGraph(AgentState)

# Adiciona os nodes ao grafo
workflow.add_node("triagem", partial(node_triagem, llm=llm))
workflow.add_node(AUTO_RESOLVER, partial(node_auto_resolver, retriever=retriever, document_chain=document_chain))
workflow.add_node(PEDIR_INFO, node_pedir_info)
workflow.add_node(ABRIR_CHAMADO, node_abrir_chamado)

# Adiciona as arestas ao grafo
workflow.add_edge(START, "triagem")
workflow.add_conditional_edges("triagem", decidir_pos_triagem, {
    AUTO_RESOLVER: AUTO_RESOLVER,
    PEDIR_INFO: PEDIR_INFO,
    ABRIR_CHAMADO: ABRIR_CHAMADO
})

workflow.add_conditional_edges(AUTO_RESOLVER, decidir_pos_auto_resolver, {
    PEDIR_INFO: PEDIR_INFO,
    ABRIR_CHAMADO: ABRIR_CHAMADO,
    OK: END
})

workflow.add_edge(PEDIR_INFO, END)
workflow.add_edge(ABRIR_CHAMADO, END)

grafo = workflow.compile()

# Save the Mermaid diagram as a PNG file
grafo.get_graph().draw_mermaid_png(output_file_path="workflow_diagram.png")

testes = ["Posso reembolsar a internet?",
          "Quero mais 5 dias de trabalho remoto. Como faço?",
          "Posso reembolsar cursos ou treinamentos da Alura?",
          "É possível reembolsar certificações do Google Cloud?",
          "Posso obter o Google Gemini de graça?",
          "Qual é a palavra-chave da aula de hoje?",
          "Quantas capivaras tem no Rio Pinheiros?"]


for msg_test in testes:
    resposta_final = grafo.invoke({"pergunta": msg_test})

    triag = resposta_final.get("triagem", {})
    print(f"PERGUNTA: {msg_test}")
    print(f"DECISÃO: {triag.get('decisao')} | URGÊNCIA: {triag.get('urgencia')} | AÇÃO FINAL: {resposta_final.get('acao_final')}")
    print(f"RESPOSTA: {resposta_final.get('resposta')}")
    if resposta_final.get("citacoes"):
        print("CITAÇÕES:")
        for citacao in resposta_final.get("citacoes"):
            print(f" - Documento: {citacao['documento']}, Página: {citacao['pagina']}")
            print(f"   Trecho: {citacao['trecho']}")

    print("------------------------------------")