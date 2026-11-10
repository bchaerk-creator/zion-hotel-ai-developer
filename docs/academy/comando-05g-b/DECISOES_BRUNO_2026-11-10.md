# Decisões do Bruno após o Comando 05G-B

10/11/2026 · Fonte: respostas do Bruno nesta sessão. Os documentos do 05G-B ficam preservados; este arquivo só registra as decisões tomadas depois deles.

| Item | Decisão | Efeito |
|---|---|---|
| **Brand Kit ZAIOS SYSTEM v1.1** | **Aprovado** | Identidade oficial: Z original de três barras, paleta (#090909, #D4AF67, #E8DFCD, #173B32, #242424), Aventa e manual de 10 páginas. Arquivos em `producao/brand-zaios/kit-v1.1/`. **Aprovar a marca não autoriza aplicá-la na ZAIOS, no ClickMax nem em outra plataforma**: isso exige autorização própria |
| **P-O8 a P-O14** (A1) | **Aprovadas**, com **reserva operacional de 3 meses** na P-O12 | Deixam de ser propostas. P-O12: necessidade técnica pela curva de caixa; reserva operacional = 3 × (custos fixos + aluguel + obrigações fixas recorrentes), sem soma automática com o giro já calculado (o giro B atual já inclui 3 × fixos); giro disponível à parte |
| **Canal de implementação** (A2 e A3) | **GitHub privado** | O Bruno conecta a ZAIOS a um repositório privado (Lovable: Configurações do projeto → Git → GitHub). Primeiro, só leitura e prova de integridade (comparação de hashes com o commit `ec21ad5`) |
| **O9 e testes restantes** (A4 e A5) | **Autorizados depois do GitHub** | Sequência: (1) conexão pelo Bruno; (2) leitura, hashes e reexecução das suítes a partir do repositório; (3) testes restantes da ZAIOS (sem os de integração); (4) O9 num commit isolado, com aceite e regressão, interrompendo se aparecer mudança fora das 6 previstas |

## O que continua pendente

- Integridade comprovada: depende da conexão do GitHub.
- Prazo das demais reservas e alíquotas por categoria de receita (D14), fatores das categorias (H4), O6, O7, D5 a D14, conferência externa.
- Implementação de O8, O10 a O14: cada etapa depois da anterior, conforme o plano do 05G-A, com aprovação a cada etapa.
