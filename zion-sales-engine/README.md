# ZION SALES ENGINE

Central de engenharia de vendas digitais da Zion Hotel Academy. Criada em 25/11/2026 por autorização de Bruno Chaerk (Comando Mestre ZION SALES ENGINE).

Fica na raiz do repositório e **não** dentro de `docs/`, que é o site institucional. Nada aqui é publicado no site.

## Mapa

| Pasta | Propósito | Dono (agente) |
|---|---|---|
| `00-diretoria` | Decisões, prioridades e pendências para Bruno | ZION SALES DIRECTOR |
| `01-metodologia` | Manual mestre e metodologias | ZION SALES DIRECTOR |
| `02-agentes` | Definição dos 9 agentes internos | ZION SALES DIRECTOR |
| `03-inteligencia-mercado` | Mercado, público, concorrência, ofertas | MARKET |
| `04-engenharia-financeira` | CPA, margem, ponto de equilíbrio, cenários | FINANCE |
| `05-funis` | Desenho e diagnóstico dos funis | FUNNEL |
| `06-criativos` | Matriz de conceitos, inventário, briefings | CREATIVE |
| `07-landing-pages` | Auditoria e especificação de páginas | CONVERSION |
| `08-checkouts` | Auditoria e testes de checkout | CONVERSION |
| `09-tracking` | Rastreamento, pixel, CAPI, UTM, conciliação | DATA |
| `10-meta-ads` | Estrutura de campanhas e leitura de mídia | TRAFFIC |
| `11-testes-ab` | Hipóteses, protocolos e resultados de testes | TRAFFIC (com DATA) |
| `12-dashboard` | Especificação do painel diário | DATA |
| `13-relatorios` | Relatórios de auditoria e de rotina (sanitizados) | AUDITOR (arquivo), DATA e DIRECTOR (escrita) |
| `14-historico-alteracoes` | Log do que mudou em produção | ZION SALES DIRECTOR |

Ponto de partida: `01-metodologia/MANUAL_MESTRE.md`. Agentes: `02-agentes/README.md`. Executáveis do Claude Code: `.claude/agents/zion-sales-director.md` e os outros oito `zion-*` do motor.

## Regras de governança

1. **Só leitura por padrão.** Os agentes leem ClickMax, Windsor/Meta, GitHub e páginas públicas. Escrita em produção (ClickMax, Meta, automações, mensagens) só com "aprovado" de Bruno, caso a caso.
2. **Fluxo de aprovação:** AUDITOR valida, DIRECTOR consolida, Bruno decide. Nada vai para produção sem esse caminho.
3. **Gasto, disparo e automação:** gastar com anúncio, ligar campanha, disparar mensagem a leads, ativar automação e mexer no que já existe exigem "aprovado". Campanhas nascem pausadas.
4. **Não editar o que já existe:** `CLAUDE.md`, `docs/`, `producao/` e os agentes `zion-*` anteriores ficam intactos. Este diretório só cresce com arquivos novos; mudança em arquivo daqui é registrada em `14-historico-alteracoes/LOG.md`.
5. **Sem dados pessoais no repositório:** nada de senhas, tokens, chaves, e-mails, telefones nem nomes de clientes, leads ou compradores. Use "cliente A/B". O repositório é visível no GitHub.
6. **Evidência marcada:** [E] evidência lida, [H] hipótese, [NC] não confirmado. Número sem fonte não entra.
7. **Regras fixas do `CLAUDE.md` valem aqui:** sem invenção, sem promessa de resultado, fotos reais, "Aprenda o passo a passo", identidade Zion.
8. **Toda mudança em produção** gera uma linha em `14-historico-alteracoes/LOG.md` (data, o que, ids, aprovado por).

## Como reverter

Tudo aqui é versionado. Para desfazer uma mudança neste diretório:

```
git log --oneline -- zion-sales-engine/        # achar o commit
git revert <hash>                              # cria um commit que desfaz, sem apagar o histórico
```

Para desfazer a criação inteira da estrutura, reverta o commit "Cria zion-sales-engine" (o primeiro que toca esta pasta). Nunca use `git reset --hard` nem force push na `main`.
Reverter arquivos **não** desfaz alterações feitas em produção (ClickMax, Meta): essas são desfeitas na própria plataforma, e o `LOG.md` diz o que foi mudado e onde.
