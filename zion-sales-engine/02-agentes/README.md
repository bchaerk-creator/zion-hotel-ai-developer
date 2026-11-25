# 02 · Agentes internos do ZION SALES ENGINE

**Dono:** ZION SALES DIRECTOR. Criado em 25/11/2026.

## O que são (e o que não são)

São **agentes internos** de engenharia de vendas: leem dados, auditam, calculam e recomendam a Bruno. **Não** substituem nem interferem em **Bela, Zaya** e nos demais agentes de atendimento (que falam com leads e clientes). Nenhum agente daqui envia mensagem, atende lead ou muda configuração de atendimento.

## Os nove agentes

| Agente | Arquivo de definição | Executável (Claude Code) | Escreve em `zion-sales-engine/`? |
|---|---|---|---|
| ZION SALES DIRECTOR | `director.md` | `.claude/agents/zion-sales-director.md` | Sim |
| FUNNEL | `funnel.md` | `.claude/agents/zion-funnel.md` | Não |
| FINANCE | `finance.md` | `.claude/agents/zion-finance.md` | Não |
| CREATIVE | `creative.md` | `.claude/agents/zion-creative.md` | Não |
| MARKET | `market.md` | `.claude/agents/zion-market.md` | Não |
| DATA | `data.md` | `.claude/agents/zion-data.md` | Sim (relatórios, sem dados pessoais) |
| CONVERSION | `conversion.md` | `.claude/agents/zion-conversion.md` | Não |
| TRAFFIC | `traffic.md` | `.claude/agents/zion-traffic.md` | Não |
| AUDITOR | `auditor.md` | `.claude/agents/zion-auditor.md` | Não |

Os nomes `zion-*` do motor não colidem com os agentes anteriores da fábrica educacional (`zion-arquiteto-pedagogico`, `zion-construtor-ferramentas`, `zion-designer-aula`, `zion-designer-editorial`, `zion-especialista-hoteleiro`, `zion-publicador-clickmax`, `zion-redator-capitulo`, `zion-revisor-pedagogico`, `zion-roteirista`).

## Arquitetura: quem reporta a quem

```
                         Bruno (decide)
                              ^
                              |  aprovado / não aprovado
                        ZION SALES DIRECTOR   <- coordena e consolida
                         ^        ^        ^
                         |        |        |
        FUNNEL  FINANCE  CREATIVE  MARKET  DATA  CONVERSION  TRAFFIC   <- entregam relatórios
                                      |
                                   AUDITOR   <- valida o que o DIRECTOR vai levar a Bruno
```

- Os sete agentes especialistas entregam ao **DIRECTOR**.
- O **DIRECTOR** coordena, resolve conflitos com evidência e consolida.
- O **AUDITOR** valida a consolidação e confere conformidade, dados pessoais e alterações em produção.
- **Fluxo de aprovação:** AUDITOR → DIRECTOR → Bruno. Execução em produção só depois do "aprovado" de Bruno, por quem ele designar, e com registro em `14-historico-alteracoes/LOG.md`.

## Permissões

- Todos leem (ClickMax, Windsor/Meta, GitHub, páginas públicas, arquivos).
- Só **DIRECTOR** e **DATA** escrevem em `zion-sales-engine/`. Os demais devolvem texto ao DIRECTOR.
- Nenhum agente escreve em produção. O TRAFFIC nunca usa `execute_action` do Windsor.
- Bash existe apenas em FINANCE, DATA, CONVERSION e AUDITOR, para cálculo e testes de leitura (git, grep, Playwright/curl GET).
- Limite técnico a saber: o campo `tools` do Claude Code liga ou desliga ferramentas pelo nome. As ferramentas de leitura do ClickMax e do Windsor foram listadas uma a uma, e as de escrita ficaram de fora. A regra de "só leitura" no Bash e a de "escrever só em `zion-sales-engine/`" são dadas no prompt e conferidas pelo AUDITOR com `git diff --stat`.

## Persistência e memória

Os agentes são **arquivos de instruções versionados no Git**. Não existe processo rodando: nada fica "ligado" nem lembra de conversas anteriores. Cada execução começa do zero e **lê os arquivos**.

A "memória" do motor é o que está escrito aqui:
- `13-relatorios/`: relatórios de auditoria e de rotina;
- `14-historico-alteracoes/LOG.md`: o que mudou em produção;
- a tabela **Histórico de decisões** no fim do arquivo de cada agente;
- `01-metodologia/MANUAL_MESTRE.md`: as regras.

Se algo não foi gravado, o agente seguinte não sabe. Rotinas (por exemplo, relatório diário) precisam ser disparadas por Bruno ou por um agendamento, e cada disparo lê esses arquivos.

## Como usar

No Claude Code, chame o agente pelo nome (por exemplo, `zion-sales-director`) ou peça ao DIRECTOR para acionar os outros. Para reverter qualquer mudança nesta pasta: `git revert <commit>` (ver `zion-sales-engine/README.md`).

## O que cada agente tem (comando)

Cada agente tem: missão, responsabilidades, limites, ferramentas autorizadas, indicadores de desempenho, procedimentos operacionais, formato de relatório, critérios de aprovação e histórico de decisões. São internos e não substituem os agentes de atendimento.

## Rascunho a revisar

Missão e limites seguem o comando e o `CLAUDE.md`. **Indicadores, procedimentos e critérios de aprovação de cada agente são uma primeira versão** escrita a partir do manual e da auditoria, e esperam revisão de Bruno.
