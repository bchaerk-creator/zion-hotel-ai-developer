# Relatório executivo · Comando 05G-A

09/11/2026 · Para Bruno Chaerk · **Documentação e planejamento. Nenhuma implementação, correção, deploy ou homologação.**

## 1. Registros conferidos

| Registro | Situação |
|---|---|
| `docs/academy/comando-05f/` (8 documentos) | Existe. Os hashes conferem com `HASHES_05F.txt` (8 de 8) |
| `testes/financeiro/resultados/2026-11-09-05f/` | Existe (`RESULTADO_05F.md`, `resultado_05f.json`) |
| Commit `2255189` | Está na `main` (`origin/main`) |
| Branch `claude/zaios-planejamento` | Tem o espelho do 05F (commit `3944491`) |
| ZAIOS | Continua no commit `ec21ad5`, sem edição desde 07/11/2026 |
| Documentos 05B, 05D, 05E e 05F | Preservados, sem alteração |

## 2. Confirmação das sete decisões

**O8, O9, O10, O11, O12, O13 e O14** estão registradas em `DECISOES_APROVADAS_O8_O14.md`, como **aprovadas e não implementadas**. O registro também lista os pontos que as decisões deixam em aberto (rótulos, convenções, prazos, fatores).

## 3. Mapa dos módulos e arquivos afetados

`MATRIZ_IMPACTO_TECNICO.md` traz arquivo, função e linha, verificados no código (commit `ec21ad5`):

| Camada | Arquivos |
|---|---|
| Cálculo | `src/calc/receitas.ts`, `src/calc/viabilidade.ts`, `src/calc/capex.ts` |
| Composição | `src/exercicios/receitas-calculo.ts`, `viabilidade-calculo.ts`, `capex-calculo.ts` |
| Campos | `src/exercicios/receitas.ts`, `viabilidade.ts`, `capex.ts`, `tipos.ts` |
| Interface | `src/components/zion/ResultadoPilar.tsx`, `ResultadoReceitas.tsx`, `ResultadoViabilidade.tsx`, `src/lib/viabilidade-texto.ts` |
| Relatórios | `src/lib/dossie.ts` (o PDF herda) |
| Dados | Tabela `respostas_exercicios`: respostas e resultado em JSON. **Não precisa de migração de tabela**, mas exige compatibilidade com o que já está salvo |
| Integrações | Nenhuma externa afetada (ClickMax, Asaas) |

**Achado relevante para a O12:** existem **dois conceitos de capital de giro**:
- o "mínimo" do P5 (6 × fixo), que vai para a "necessidade total" e para o dossiê;
- o "recomendado" do P6 (máximo entre A e B), que vai para a captação.

O plano propõe uma definição única.

## 4. Alterações futuras necessárias

Resumo em `PLANO_IMPLEMENTACAO_FUTURA.md`, em 8 etapas:
1. O9;
2. O8, junto com a D11-A;
3. O11;
4. O14;
5. O12;
6. O13;
7. O10;
8. consolidação do dossiê.

Cada etapa tem linha de base, aceite, regressão e aprovação. Antes de começar, há 5 pré-requisitos, entre eles:
- as respostas às perguntas pendentes;
- a escolha do canal de implementação: Lovable, que consome créditos, ou um repositório GitHub privado, que também resolve a integridade.

## 5. Riscos e dependências

Em `DEPENDENCIAS_E_RISCOS.md`: 10 riscos técnicos. Os principais:
- respostas antigas mudando de resultado sem aviso;
- o tipo do selo, que é compartilhado por todos os pilares;
- a curva de 120 meses mudando decisões;
- dupla contagem do aluguel e do capital disponível.

A ordem de dependência é O12 → O13 → O10, e O11 ↔ O14.

## 6. Plano de testes

Em `PLANO_TESTES_REGRESSAO.md`:
- **20 testes de aceite e 1 de integração**, com esperados calculados de forma independente em Python (`testes/financeiro/aceite_05g/`).
- **Executado neste comando:** a linha de base contra a ZAIOS atual. São 11 verificações: 10 FALHA, como esperado antes da implementação, e 1 PASSA (O9-2: saída com EBITDA positivo já está correta).
- **Pendentes:** aceite, regressão (237 + 288 + 108 testes próprios da ZAIOS), testes de tela e de compatibilidade.

Exemplos pedidos no comando, com o esperado:

| Decisão | Teste | Esperado |
|---|---|---|
| O8 | P6 sem selo de aprovação | Nenhum "Avançar", "Ajustar" ou "Redesenhar" no P6; conflito sinalizado no C3E |
| O9 | EBITDA negativo | C1: saída R$ 0; VPL com saída = VPL sem saída = −R$ 891.343,30 |
| O10 | Caixa no ano 5 | C1: positivo até o mês 36 (R$ 22.704,75); negativo no mês 54; capital adicional de R$ 85.232,63 |
| O11 | Bases diferentes | C2: EBITDA de R$ 571.888,56, R$ 564.688,56, R$ 559.288,56 ou R$ 552.088,56, conforme a combinação |
| O12 | Aluguel uma vez | Base mensal de R$ 12.000 (C1), R$ 36.000 (C2) e R$ 125.000 (C3) |
| O13 | Disponível < necessário | C1: déficit de R$ 64.095,26; usos de R$ 859.095,26, sem duplicidade |
| O14 | Receita independente | C3 → C3E: a categoria C fica em R$ 480.000; hoje cairia para R$ 345.600 |

## 7. Pendências que exigem decisão sua

Em `PENDENCIAS_METODOLOGICAS.md`:
- **As anteriores, todas abertas:** O6, O7, B08, A09, B06, H4, D5 a D14, integridade, segunda transcrição, pró-labore, reservas, quebra, contingência e conferência externa.
- **Novas, para viabilizar a implementação:**

| # | Pergunta |
|---|---|
| P-O8 | Rótulo da indicação preliminar do P6; se a régua de margem continua |
| P-O10a/b/c | Convenção de desconto no horizonte misto; como modelar o atraso; se o CAPEX atrasa junto |
| P-O11 | Aceitar também valor fixo em R$ (ligado à O6)? A "receita bruta" inclui todas as categorias? |
| P-O12 | Prazo ou método do componente de meses fixos do giro |
| P-O13 | O que conta como capital disponível e como entra na curva |
| P-O14a/b/c/d | Fatores por categoria; efeito da rampa e dos cenários; alíquotas; migração do `outras_pct` |

## 8. Classificação do que foi feito

| Categoria | Itens |
|---|---|
| **Decisões metodológicas aprovadas** | O8 a O14 (Bruno, 09/11/2026) |
| **Alterações técnicas propostas** | 8 etapas e 7 grupos de alterações (`PLANO_IMPLEMENTACAO_FUTURA.md`). Nenhuma executada |
| **Testes executados** | Cálculo independente dos esperados; linha de base de 11 verificações contra a cópia da ZAIOS |
| **Testes pendentes** | Aceite e regressão sobre a implementação; tela; compatibilidade; testes próprios da ZAIOS |
| **Homologações não concedidas** | Nenhuma homologação matemática definitiva, metodológica, econômica ou da plataforma |

**Créditos:**
- só foram feitas leituras no Lovable (`get_project`, `list_workspaces`, `get_workspace`, `list_files`, `read_file`);
- não houve nenhuma mensagem ao agente, edição ou deploy;
- o conector não mostra o saldo, então **não declaro consumo zero como comprovado**.

## 9. Proposta da próxima etapa (não executada)

**Comando 05G-B: definições de implementação e integridade.**
1. O Bruno responde P-O8 a P-O14 e escolhe o canal de implementação (PR-2).
2. Se escolher o GitHub privado: conectar, comparar os hashes e fazer a segunda transcrição por comparação direta.
3. Recalcular os esperados condicionais (O10, O12, O13 e integração) com as definições aprovadas.
4. Só então, em comando separado e autorizado: a etapa 1 da implementação (O9), com linha de base, aceite e regressão.

Aguardo sua revisão e autorização expressa.
