# Roteiro de Gravação para o LinkedIn 🎥

Este guia detalha o passo a passo de como você deve fazer a demonstração visual no vídeo/GIF para ilustrar o post do LinkedIn.

---

## 🎬 Preparação de Tela
1. **Lado Esquerdo da Tela**: Abra seu editor de código (VS Code/Cursor) mostrando o arquivo `C:\Users\mauri\Desktop\_templates_personas\persona-Backend.md` ou a regra global do **MauMau** contendo o trecho:
   * `Mitigação de Falsas Alegações` e `Segurança OWASP`.
2. **Lado Direito da Tela**: Deixe o navegador aberto na página `index.html` do frontend.
3. **Terminal (Embaixo)**: Deixe o terminal visível onde o servidor FastAPI (`app.py`) está rodando.

---

## ⏱️ Roteiro do Vídeo (Passo a Passo de Gravação)

### **Cena 1: A Promessa (Segundos 0-5)**
*   **Ação**: Comece o vídeo mostrando o painel de frontend carregando (dê um refresh `F5`).
*   **O que o usuário vê**: Os **Skeletons (Loading State)** piscando de forma suave por 1 segundo até o painel se renderizar por completo com os saldos carregados.
*   **Conceito Ilustrado**: *UX Premium (Claude Code Core)* — Nunca usar spinners genéricos, os skeletons respeitam a geometria exata do layout final para evitar quebras visuais e Layout Shift (FCP/TTI otimizados).

### **Cena 2: Testando Isolamento Multi-Tenant e Anti-IDOR (Segundos 5-15)**
*   **Ação**: Clique no botão superior direito alternando do **Tenant 1 (Mauri)** para o **Tenant 2 (Outro)**.
*   **O que o usuário vê**: A lista de contas à esquerda muda de forma instantânea e some com as contas do Mauri, exibindo apenas as contas do "Tenant 2".
*   **Conceito Ilustrado**: *Segurança nas Fronteiras* — A persona-backend foi instruída a escopar TODA query pelo ID do tenant do JWT. A @persona-cybersec testaria isso ativamente.

### **Cena 3: Simulação de Validação e Concorrência Atômica (Segundos 15-30)**
*   **Ação**: Volte para o Tenant 1. No formulário de transferência:
    1. Selecione a conta de destino `Conta Poupanca Mauri (ID: 2)`.
    2. Digite um valor válido (ex: `20.00`) e clique em **Transferir Recursos**.
*   **O que o usuário vê**: O botão muda para *"Processando Transação..."* por exatamente 1 segundo (a latência simulada) e depois atualiza os saldos das duas contas na tela instantaneamente, além de atualizar o histórico de "Atividade Recente" no card central com a descrição correta em português.
*   **Conceito Ilustrado**: *Validação Adversária* — O backend utiliza transações explícitas com locks na escrita (`with_for_update`) para impedir condições de corrida no banco de dados.

### **Cena 4: Tratamento de Erros Sem Vazamento de Contexto (Segundos 30-45)**
*   **Ação**: Tente efetuar uma transferência de um valor abusivo (ex: `5000.00`).
*   **O que o usuário vê**: O sistema processa e exibe uma caixa vermelha de erro estilizada informando *"Saldo insuficiente na conta de origem."*.
*   **Conceito Ilustrado**: *Error Masking* — O backend trata a exceção e retorna a mensagem correta, enquanto os logs internos registram o trace completo, mas sem expor segredos ou detalhes internos do banco para o frontend (prevenindo *Information Exposure*).

---

## 💡 Dicas de Gravação
*   **Ferramenta recomendada**: Use o **Loom** ou **OBS Studio** para gravar a tela em boa qualidade.
*   **Duração ideal**: Entre 40 e 50 segundos. Vídeos curtos e objetivos performam muito melhor no feed do LinkedIn.
*   **Corte Seco**: Edite o início e o fim da gravação para não mostrar você iniciando/parando o programa de gravação.
