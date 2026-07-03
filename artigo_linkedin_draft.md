Parei de aceitar "vibecoding" no meu fluxo de desenvolvimento com IA. O resultado? Fiz a própria IA criar uma aplicação do zero para testar e provar o valor de suas novas personas.

Se você desenvolve com IA, conhece esse ciclo: você pede um código, ela te entrega algo que "parece que funciona", mas na primeira carga de concorrência real ou verificação de segurança, quebra no ambiente de produção.

Para resolver isso de forma definitiva, conduzi um experimento: peguei as melhores práticas internas de engenharia vazadas do Claude Code (a nova CLI da Anthropic) e injetei diretamente nas minhas personas de desenvolvimento (Arquiteto, Backend, Frontend e CyberSec). 

Mas eu não queria apenas "acreditar" que tinha funcionado. Pedi para a minha IA criar um caso de teste prático para provar que as novas personas estavam programando sob os novos padrões. 

A IA (sob a coordenação do meu Arquiteto virtual, MauMau) projetou e construiu de forma autônoma uma aplicação financeira completa (FastAPI + React), aplicando barreiras rígidas de validação:

🛡️ Como a IA validou o Backend (@persona-backend):
* Em vez de fazer uma lógica simples de saldo, ela utilizou transações explícitas no banco com locks de escrita (`with_for_update`) para impedir Double Spending.
* Blindou endpoints contra IDOR escopando as queries no banco de dados com o ID do tenant vindo do header.
* Para provar o funcionamento, ela disparou 10 requisições simultâneas locais (race condition test), e em vez de apenas dizer "deve funcionar", anexou a saída literal do pytest do terminal comprovando o sucesso.

🎨 Como a IA validou o Frontend (@persona-frontend):
* Implementou uma interface premium (estilo Vercel/Linear) tratando os 4 estados lógicos obrigatórios (Success, Skeletons de Loading proporcionais para evitar Layout Shift, Error com botão de Retry e Empty States).
* Sanitizou a renderização de dados de entrada para neutralizar riscos de XSS no navegador.

🔍 Como o Arquiteto (@MauMau) auditou tudo:
* Ele fez a revisão cirúrgica do diff real (`git diff`) no terminal local.
* Exigiu saídas de compilação sem warnings e validou se erros de banco estavam mascarados para evitar vazamento de dados internos de infraestrutura.

No vídeo abaixo, você pode ver a aplicação rodando em tempo real: os skeletons carregando, a barreira anti-IDOR ocultando dados ao alternar de Tenant, e as transações de saldo travando o banco contra estouro de limite.

O maior aprendizado desse experimento é que a qualidade do código gerado por IA não depende apenas do modelo, mas sim do rigor das restrições e regras de validação que você impõe a ele.

Como você tem validado e garantido a qualidade do código gerado pelos seus agentes? 🚀
