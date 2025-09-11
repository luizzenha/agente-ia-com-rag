# Assistente de Políticas Internas

Este é um assistente virtual baseado em IA para responder perguntas sobre as políticas internas da empresa ReZenha Desenvolvimento. O sistema utiliza processamento de linguagem natural para entender e responder perguntas com base em documentos de políticas da empresa.

## 🚀 Funcionalidades

- Carregamento e processamento de documentos PDF de políticas
- Busca semântica para encontrar trechos relevantes
- Geração de respostas baseadas no contexto das políticas
- Citações das fontes para referência

## 🛠️ Estrutura do Projeto

```
genai/
├── pdfs/                         # Pasta contendo os arquivos de políticas em PDF
├── chunks.py                    # Carrega e divide os documentos
├── embeddings.py                # Gera embeddings e configura o sistema de busca
├── formatters.py                # Formata as saídas e citações
├── script.py                    # Script principal da aplicação
├── triagem_out.py               # Modelos de saída para o sistema de triagem
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Google AI Studio com chave de API

## 🔧 Instalação

1. Clone o repositório:
   ```bash
   git clone <seu-repositorio>
   cd genai
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure a variável de ambiente com sua chave da API do Google:
   ```bash
   export GOOGLE_API_KEY="sua_chave_aqui"
   ```
   Ou crie um arquivo `.env` na raiz do projeto com:
   ```
   GOOGLE_API_KEY=sua_chave_aqui
   ```

## 🚀 Como Usar

1. Coloque seus arquivos de política na pasta `pdfs/`

2. Execute o script principal:
   ```bash
   python script.py
   ```

3. O script irá processar os documentos e permitir que você faça perguntas sobre as políticas.

## 📝 Exemplo de Uso

```python
# Exemplo de pergunta
resposta = perguntar_politica_RAG("Posso reembolsar a internet do home office?")
print(resposta['answer'])
for citacao in resposta['citacoes']:
    print(f"Fonte: {citacao['documento']}, Página: {citacao['pagina']}")
    print(f"Trecho: {citacao['trecho']}")
```

## 📚 Documentação dos Módulos

### chunks.py
- `load_policies()`: Carrega documentos PDF da pasta `pdfs/`
- `split_docs(docs)`: Divide os documentos em pedaços menores
- `LoadChunks()`: Função auxiliar que carrega e divide os documentos

### embeddings.py
- `embed(api_key)`: Configura o modelo de embeddings do Google
- `LoadRetriever(chunks, api_key)`: Configura o sistema de busca vetorial

### formatters.py
- `extrair_trecho(texto, query, janela)`: Extrai trechos relevantes com base na consulta
- `formatar_citacoes(docs_rel, query)`: Formata as citações para exibição

## ⚠️ Notas Importantes

- Mantenha sua chave de API segura e não a compartilhe
- O sistema é baseado nas políticas fornecidas na pasta `pdfs/`
- Para melhores resultados, mantenha os documentos de políticas atualizados

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
Desenvolvido por Zenha para ReZenha Desenvolvimento
