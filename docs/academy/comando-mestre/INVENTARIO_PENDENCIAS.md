# Inventário único de pendências · Comando Mestre

10/11/2026 · Situação **depois** da execução do Comando Mestre. Classes: **Concluído** · **Aprovado, aguardando implementação** · **Pendente, com solução técnica recomendada** · **Bloqueado por dependência externa**.

"Concluído" aqui quer dizer implementado e testado na **cópia de desenvolvimento**. Nada foi aplicado na ZAIOS ativa.

## 1. Decisões metodológicas

| Item | Classe | Situação |
|---|---|---|
| O8 · indicação preliminar no P6 (com P-O8) | Concluído | Selo "Indicação preliminar"; margem antes e depois dos custos do modelo; conflito com a viabilidade explícito |
| O9 · saída por múltiplo nunca negativa | Concluído | MAX(0, múltiplo × EBITDA) com aviso |
| O10 · horizonte de 10 anos (com P-O10a, b, c) | Concluído | 120 meses; 36 em detalhe e anos 4 a 10 anuais; alertas; capital adicional; atraso no horizonte fixo; VPL anual |
| O11 · bases de gestão e royalty (com P-O11) | Concluído | Hospedagem, receita bruta ou valor fixo; hipótese sem contrato |
| O12 · giro sem dupla contagem (com P-O12, 3 meses) | Concluído | Necessidade técnica + reserva operacional configurável |
| O13 · disponível x necessário (com P-O13) | Concluído | Fonte, diferença, déficit, excedente, captação adicional |
| O14 · receitas complementares A, B, C (com P-O14) | Concluído | Custos, alíquota, meses e rampa próprios |
| O7 · impostos por natureza na G2 | Concluído | Impostos sobre a receita como dedução; tributos fixos como despesa fixa |
| B08 · dois pontos de equilíbrio (Arsenal) | Concluído (branch de desenvolvimento) | Operacional (sem reserva) e de caixa (com reserva). Branch `dev/mestre-arsenal`, fora da main |
| A09 · calendário real (Arsenal) | Concluído como **proposta provisória** | 365/366 dias; 31 × 12 deixa de virar 372. Aguarda aprovação |
| A09 · gestão nas deduções (O2) | Pendente, com solução recomendada | Mostrar o resultado antes da gestão e a gestão como custo do modelo, como na ZAIOS |
| O6 · modalidade em R$ x % (Folha J2) | Pendente, com solução recomendada | A ZAIOS já aceita as duas (O11). Falta alinhar a Folha J2 ao mesmo dicionário |
| D5 · fixos × 12 com menos meses no A09 | Pendente, com solução recomendada | Fixos proporcionais aos meses de operação, ou aviso. Exige decisão (ver consolidação) |
| D6 · base da contingência | Pendente, com solução recomendada | Base ZAIOS (obra e infraestrutura) como padrão; ferramentas simples com rótulo "base simplificada" |
| D8 · payback acima do horizonte | Pendente, com solução recomendada | Manter o estendido marcado como "estendido" (como hoje) |
| D9 · custo variável por noite ou por estadia | Concluído na ZAIOS | Os dois existem, e as categorias A e B têm custo próprio |
| D10 · cenários de referência | Pendente (H4) | Parâmetros da Zion; a ferramenta mostra a definição usada |
| D11-A · sinal x veredito | Concluído na ZAIOS P6 (via O8) | Ferramentas do Arsenal seguem sem mudança |
| D12 · fôlego x cobertura da reserva | Pendente, com solução recomendada | Dicionário com os dois nomes e as duas fórmulas |
| D13 · float x centavos | Concluído | ZAIOS em centavos sem arredondar até a tela; todo código novo segue a regra |
| D14 · taxa de limpeza e outras receitas | Parcial | Alíquota própria das complementares implementada; a taxa de limpeza segue fora da hospedagem (decisão de 08/11). Alíquota por fonte é decisão do contador |
| B06 · regra de referência sem documento | Bloqueado por dependência externa | Falta o documento de origem da regra |
| H4 · parâmetros e limites | Pendente: decisão do Bruno | Taxa, múltiplo, colchão de 10%, 8/12 anos, cenários, rampa, atraso de 6 meses, estresses |
| D2-C · reserva de reposição 3–6% x 3–5% na ZAIOS | Aprovado, aguardando implementação | Ajustar a faixa de referência para 3–6% e o padrão para 4% (não feito: muda resultados de projetos salvos sem aviso; ver consolidação) |
| D1, D3-A, D4, D7-C (aprovadas antes) | Aprovado, aguardando implementação | Rótulos de retorno (D1), quebra (D3-A), pró-labore x distribuição (D4), métodos 2 e 3 de saída (D7-C). Fora do escopo das O8 a O14 |
| Conferência externa (contador ou analista) | Bloqueado por dependência externa | Recomendada antes da homologação |

## 2. Funcionalidades

| Item | Classe |
|---|---|
| Campos novos no P6 (bases e valor fixo das taxas, contrato, categorias A/B/C, meses de reserva, outras obrigações, aluguel no fixo) e na Viabilidade (capital disponível) | Concluído na cópia de desenvolvimento |
| Telas do P6 e da Viabilidade e textos do dossiê com as regras novas | Concluído na cópia; **sem mudança visual de marca** |
| Aplicação da identidade ZAIOS SYSTEM v1.1 na plataforma | Fora desta etapa (não autorizado) |

## 3. Erros e inconsistências no código

| Item | Classe |
|---|---|
| Falha do teste `financas-indicadores.test.ts:98` (espaço não separável) | Diagnosticado: o formatador usa U+00A0; a cópia do teste traz espaço comum. Trocando só esse caractere, os 50 testes do arquivo passam. Confirmação depende do arquivo original (GitHub) |
| Erros de tipo da cópia | 2 avisos de `key` em componentes, presentes na base (faltam os tipos do React na cópia parcial); nenhum erro novo de tipo nas regras |

## 4. Testes que ainda faltam

| Item | Classe |
|---|---|
| 14 arquivos de teste restantes da ZAIOS (sem os de integração) | Bloqueado: leitura autorizada só depois do GitHub (decisão de 10/11) |
| Testes de integração (Supabase, autenticação, gravação) | Bloqueado por serviço externo; não rodam em ambiente isolado |
| Teste de interface no navegador (telas novas) | Bloqueado: a cópia não tem o projeto inteiro (rotas, componentes de UI); exige o repositório |

## 5. O que impede a conclusão

1. **Integridade da origem**: sem o GitHub privado, a cópia é transcrição; não há hash do código original.
2. **Homologação do Bruno** das premissas provisórias (A09 calendário real, custos mantidos no atraso, categoria C sem rampa por padrão, P5 com estimativa de 6 meses) e dos parâmetros H4.
3. **Aplicação no projeto real** por branch no repositório privado, com testes da plataforma e revisão, antes de qualquer publicação.

## 6. O que depende do Bruno

Ver `RELATORIO_FINAL.md`, item 6.

## 7. O que o Claude conclui sozinho, sem créditos

Feito nesta etapa: implementação, testes, referência independente, compatibilidade, documentação e pacote. Depois do GitHub: conferência de integridade, aplicação dos patches numa branch, leitura e execução dos testes restantes. Nesta etapa não houve nenhuma mensagem ao agente do Lovable, que é a ação que consome créditos; só leituras de projeto e de arquivo. O saldo de créditos não aparece pelo conector, então não há comprovação numérica de consumo zero.
