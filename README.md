# Resilient AI Finance App 🛡️

Uma demonstração prática e laboratório de testes projetado e construído de forma autônoma por agentes de IA sob regras estritas de engenharia de software (**Anti-Vibecoding**). 

Este projeto serve como prova de conceito para validar a evolução de personas de IA (Arquiteto, Backend e Frontend) utilizando princípios avançados de design de código de nível enterprise, como controle de concorrência real, isolamento de dados por Tenant e UI/UX de alta fidelidade baseada em múltiplos estados lógicos.

---

## 🧠 Como Foi Feito? (O Experimento de Auto-Refinamento)

O desenvolvimento deste app foi guiado pela persona **MauMau** (Principal Software Engineer e Arquiteto virtual), que atua de forma orquestrada sem escrever código-fonte diretamente. Ele planeja a arquitetura, desenha as especificações e audita os códigos gerados pelas demais personas executoras.

Para este teste:
1. **Auditoria de Personas**: As personas executoras (`@persona-backend` e `@persona-frontend`) foram auditadas a partir de regras inspiradas nas melhores práticas de engenharia de ferramentas de ponta (como o Claude Code).
2. **Auto-Refinamento**: Os prompts das personas foram atualizados no sistema para injetar regras explícitas de diagnóstico preventivo de erros, segurança (OWASP), concorrência e UI avançada.
3. **Escrita Cirúrgica**: As próprias personas modificaram e aplicaram as correções em seus prompts de sistema e no código-fonte, testando o pipeline localmente.

Para entender os bastidores completos de como fizemos a IA auditar e evoluir seu próprio cérebro operacional, leia o documento [Bastidores do Refinamento](file:///c:/Users/mauri/Desktop/Projetos_Pessoais/demonstracao_teste_personas/artigo_explicativo_workflow.md).

---

## 🛠️ A Aplicação e Arquitetura

A aplicação simula uma **Plataforma Financeira Simplificada** dividida em duas partes principais:

### 1. Backend (`/backend`) - FastAPI + SQLite (SQLAlchemy)
Implementado pela `@persona-backend` focando em segurança e consistência de dados:
* **Prevenção de Double Spending (Race Conditions)**: Processamento de transferências usando transações explícitas com locks de escrita no banco de dados (`with_for_update`) na consulta de contas.
* **Isolamento Rigoroso (Anti-IDOR)**: Toda query de leitura/escrita no banco é escopada de forma redundante pelo `tenant_id` injetado pelo cabeçalho (simulando token JWT). O usuário de um Tenant jamais consegue ler ou alterar dados de outro.
* **Validação de Entrada**: Uso do Pydantic para validação rígida de tipos, limites decimais (`max_digits=12`, `decimal_places=2`) e strings sanitizadas.

### 2. Frontend (`/frontend`) - React (SPA via CDN) + Tailwind CSS
Implementado pela `@persona-frontend` com alto rigor de design visual e estados de tela:
* **UI/UX Premium**: Estilo com tema escuro (Deep Dark), tipografia Outfit do Google Fonts e efeito de Glassmorphism.
* **Estados Lógicos Completos**:
  * **Success**: Exibição dos saldos reais e históricos de transações.
  * **Loading**: Skeletons estruturados com gradientes animados para prevenir Layout Shifts bruscos.
  * **Error**: Interface de falha com mensagens amigáveis e botão de Retry funcional.
  * **Empty**: Estado de feedback visual limpo se a conta não possuir transações.
* **Segurança no Browser**: Escapamento nativo de strings para blindagem contra XSS (cross-site scripting) visual em transações.
* **Laboratório de Teste Interativo**: Um menu lateral permite alternar entre tenants e forçar simulações de falhas (como transferências sem saldo ou acessos não autorizados) para testar os limites do sistema na hora.

---

## 📂 Estrutura do Repositório

```bash
├── backend/
│   ├── app.py                # Servidor FastAPI com endpoints de Contas e Transferências
│   ├── demo_finance.db       # Banco SQLite local populado
│   └── requirements.txt      # Dependências Python (FastAPI, SQLAlchemy, Uvicorn)
├── frontend/
│   └── index.html            # Dashboard SPA em React + Tailwind
├── .gitignore                # Regras de Git para evitar arquivos de cache e banco local
├── artigo_linkedin_draft.md  # Rascunho do post do LinkedIn
├── artigo_explicativo_workflow.md # Detalhamento dos bastidores do refinamento
└── README.md                 # Este documento
```

---

## 🚀 Como Executar Localmente

### Passo 1: Inicializar o Backend

Certifique-se de ter o Python 3.10 ou superior instalado.

1. Navegue até o diretório do backend:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # No Linux/Mac:
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o servidor:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
   O backend estará disponível em `http://localhost:8000`.

### Passo 2: Executar o Frontend

Como o frontend é uma Single Page Application contida em um único arquivo HTML que consome React e Tailwind via CDN, você não precisa instalar nenhuma dependência do Node.js.

1. Basta abrir o arquivo `frontend/index.html` diretamente em seu navegador web (dando duplo clique no arquivo ou usando uma extensão como Live Server no VS Code).
2. Certifique-se de que o backend está rodando no endereço `http://localhost:8000`.

---

## 🧪 Casos de Teste e Validações

O repositório também inclui as discussões, prompts e logs dos testes que validaram as novas personas:
* Consulte o [Caso de Teste do Backend](file:///c:/Users/mauri/Desktop/Projetos_Pessoais/demonstracao_teste_personas/backend_test_case.md) para ver como a `@persona-backend` protegeu o endpoint de transferência de saldo.
* Consulte o [Caso de Teste do Frontend](file:///c:/Users/mauri/Desktop/Projetos_Pessoais/demonstracao_teste_personas/frontend_test_case.md) para ver a arquitetura do componente com skeletons e CTAs de Retry contra falhas.
