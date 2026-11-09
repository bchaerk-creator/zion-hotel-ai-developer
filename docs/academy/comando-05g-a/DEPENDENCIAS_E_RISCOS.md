# Dependências e riscos · Comando 05G-A

09/11/2026 · Proposta para revisão.

## 1. Dependências entre decisões

| Decisão | Depende de | É pré-requisito de |
|---|---|---|
| O8 | D11-A (veredito só após homologação); P-O8 | — (deve ser revisada depois de cada mudança de cálculo) |
| O9 | D7-C (método 1) | O10 (VPL com saída no horizonte) |
| O10 | O12 e O13 (necessário e captação); D8; D6; P-O10a/b/c | — (última etapa de cálculo) |
| O11 | O6 (R$ x %); O14 (o que é receita bruta); P-O11 | Equilíbrio, cenários, sensibilidade |
| O12 | D12; P-O12; H4 (prazos) | O13, O10 |
| O13 | O12; P-O13; D4 (nome "caixa disponível" é outro conceito) | O10 (necessidade de captação total) |
| O14 | D9, D10, D14; P-O14a–d; O11 | O11 (base bruta), O12 (meses negativos do regime), O10 |

## 2. Riscos técnicos

| # | Risco | Decisão | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|---|
| RT-1 | Mudar o tipo `Veredito` quebra selos de outros pilares, pendências ou a jornada | O8 | Média | Alto | Estado preliminar separado do enum, ou novo valor só usado no P6; regressão visual de todos os pilares |
| RT-2 | Respostas antigas sem os campos novos produzem resultado diferente sem aviso | O11, O12, O13, O14 | Alta | Alto | Padrões que reproduzem o cálculo atual (base bruta, outras como categoria A em % das diárias, sem disponível); aviso de "metodologia atualizada" ao recalcular |
| RT-3 | Dossiês já emitidos ficam incoerentes com a tela atual | Todas | Média | Médio | Versões antigas imutáveis (migração 0003, a conferir); marcar a versão da metodologia no dossiê |
| RT-4 | Curva de 120 meses muda o colchão e a decisão de projetos existentes | O10 | Alta | Alto | Mostrar antes e depois na primeira visita; listar as decisões que mudam nos cenários de teste |
| RT-5 | Dupla contagem do disponível (fontes + curva) ou do aluguel (fixo + modelo + giro) | O12, O13 | Média | Alto | Testes O12-3, O13-4 e INT-1; lista única de fontes e usos |
| RT-6 | Categorias de receita sobrepostas à hospedagem (ex.: taxa de limpeza) | O14 | Média | Médio | O14-2; regra de exclusividade; D14 |
| RT-7 | Implementação via agente do Lovable altera trechos fora do escopo | Todas | Média | Alto | Uma decisão por mensagem; `get_diff` após cada mensagem; regressão completa |
| RT-8 | Consumo de créditos acima do previsto | Todas | Média | Médio | Estimativa por etapa; aprovação prévia; preferir o canal GitHub se aprovado |
| RT-9 | Código em produção diferente da cópia auditada | Todas | Baixa a média | Alto | PR-3 e PR-4 (hash e commit antes de começar) |
| RT-10 | Testes próprios da ZAIOS (108) desatualizados após as mudanças | Todas | Alta | Médio | Atualizar junto, em cada etapa; não desativar testes |

## 3. Riscos para decisões de investimento (enquanto não implementado)

| Risco | Exemplo dos testes | Decisão que resolve |
|---|---|---|
| Ler o selo do P6 como aprovação | C3E: "Avançar" com VPL −R$ 2,79 mi | O8 |
| Valor de saída negativo distorcendo o VPL | C1: −R$ 92.517,75 | O9 |
| Falsa sensação de fôlego no caixa | C1: positivo no mês 36, negativo no mês 54 (capital adicional de R$ 85.232,63) | O10 |
| Atraso que parece melhorar o caixa | C2: menor saldo maior com atraso, mas R$ 256.539,15 a menos em 10 anos | O10 |
| Base contratual errada de gestão e royalties | C3: VPL −R$ 360.737,85 entre as bases | O11 |
| Capital de giro subestimado sem o aluguel | C1: base de R$ 9.000 x R$ 12.000 por mês | O12 |
| Captar menos que o necessário | C1: R$ 45.000 disponíveis x R$ 109.095,26 necessários | O13 |
| Receita fixa tratada como variável | C3E: R$ 345.600 em vez de R$ 480.000 | O14 |

## 4. Dependências externas

- **Créditos Lovable:**
  - nenhuma etapa deste comando consumiu créditos de desenvolvimento por ação própria. Só foram usadas leituras (`get_project`, `list_workspaces`, `get_workspace`, `list_files`, `read_file`);
  - o conector não mostra o saldo, então **não é possível comprovar consumo zero**. O Bruno pode conferir no painel.
- **ClickMax, Asaas e integrações:** nenhuma é afetada pelas decisões O8 a O14, pela leitura do código. Os cálculos são internos à ZAIOS.
