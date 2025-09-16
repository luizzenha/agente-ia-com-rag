from agent_state import AgentState
from statics import KEYWORDS_ABRIR_TICKET, PEDIR_INFO, ABRIR_CHAMADO, OK


def decidir_pos_triagem(state: AgentState) -> str:
    print("Decidindo após a triagem...")
    decisao = state["triagem"]["decisao"]
    return decisao


def decidir_pos_auto_resolver(state: AgentState) -> str:
    print("Decidindo após o auto_resolver...")

    if state.get("rag_sucesso"):
        print("Rag com sucesso, finalizando o fluxo.")
        return OK

    state_da_pergunta = (state["pergunta"] or "").lower()

    if any(k in state_da_pergunta for k in KEYWORDS_ABRIR_TICKET):
        print("Rag falhou, mas foram encontradas keywords de abertura de ticket. Abrindo...")
        return ABRIR_CHAMADO

    print("Rag falhou, sem keywords, vou pedir mais informações...")
    return PEDIR_INFO
