# Pendências para aprovação · Comando 05G-B

09/11/2026 · Lista exata do que depende do Bruno para seguir. Nada aqui foi executado.

## 1. Autorizações necessárias

| # | Autorização | Para quê | Texto sugerido |
|---|---|---|---|
| A1 | Aprovar ou ajustar as propostas P-O8 a P-O14 | Fechar a metodologia antes de implementar | "Aprovo P-O8, P-O10a, P-O10b, P-O10c, P-O11, P-O13 e P-O14; P-O12 com reserva de [N] meses" |
| A2 | Conectar a ZAIOS a um GitHub privado, só leitura | Prova de integridade (hash na origem) | "Autorizo conectar a ZAIOS ao GitHub privado em [conta], só leitura" |
| A3 | Canal de implementação | Definir se as mudanças passam pelo GitHub (commit isolado e revisável) ou pelo agente do Lovable (gasta créditos) | "Implementar pelo [GitHub / Lovable]" |
| A4 | Implementar a O9 | Primeira alteração isolada (`PLANO_IMPLEMENTACAO_O9.md`) | "Autorizo implementar a O9 conforme o plano do 05G-B" |
| A5 | Ler os 14 arquivos de teste restantes da ZAIOS (leitura, sem créditos) | Completar a execução dos testes próprios, exceto os de integração | "Autorizo a leitura dos testes restantes" |

## 2. Decisões metodológicas ainda abertas (não resolvidas por O8 a O14)

| Pendência | Tema |
|---|---|
| Prazo da reserva operacional | P-O12 (3 meses é proposta; 6 meses não está aprovado como regra universal) |
| Alíquota por categoria de receita | P-O14, D14 |
| Fatores das categorias de receita por tipo de hospedagem | P-O14, H4 |
| O6 | Modalidade em R$ ou em %, para aluguel, gestão e marca. A P-O11 propõe resolver junto |
| O7 | Impostos como despesa variável na G2 |
| D5, D6, D8, D9, D10, D12, D13, D14 | Decisões metodológicas pendentes desde o 05B |
| D7-C | Métodos 2 e 3 de saída e valor líquido (a O9 cobre só o múltiplo) |
| H4 | Parâmetros e limites (taxa, múltiplo, colchão, 8/12 anos, cenários, rampa, prazos) |
| B08, A09, B06 | Ressalvas das ferramentas do Arsenal (fora da ZAIOS) |
| Conferência externa | Contador ou analista sobre os esperados independentes |

## 3. Riscos de implementação a acompanhar

| Risco | Onde | Mitigação proposta |
|---|---|---|
| Implementar sem integridade comprovada | Todas as etapas | Fazer A2 antes de A4 |
| Sincronização do GitHub com a produção | A2 e A3 | Leitura primeiro; escrita só numa branch separada e com revisão |
| Mudanças fora do previsto | O9 | Interromper se algo diferente das 6 mudanças previstas aparecer nas suítes |
| Teste do dossiê com espaço não separável | Testes da ZAIOS | Confirmar no repositório original antes de usar essa suíte como regressão |
| Créditos | Canal Lovable | Estimar e aprovar antes; o saldo não aparece pelo conector |
