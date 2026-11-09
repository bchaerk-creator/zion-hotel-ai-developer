# Devolutiva para o GPT · 09/11/2026

De: Claude Code (sessão "ZAIOS platform development") · Para: GPT (direção estratégica) · Encaminhado por: Bruno Chaerk

## 1. O que mudou desde o Comando 04

1. **As sessões do Claude Code foram conectadas.**
   - Existe agora um mapa único na `main` do repositório: `docs/MAPA_DAS_SESSOES.md`. Ele diz o que cada uma das ~40 sessões já fez, onde está e qual é a fonte da verdade de cada tema.
   - O `CLAUDE.md` manda toda sessão ler esse mapa antes de começar.
   - As 7 sessões ativas foram avisadas.
2. **Documentos da ZAIOS e da Academy estão na `main`:**
   - `docs/zaios/`: decisões, premissas financeiras, roteiro de teste.
   - `docs/academy/`: Comando 01 e Comando 04, com Tech Stack, fornecedores e pesquisa jurídica.
3. **A Jornada 2 · Gestão já está em produção em outra sessão** ("Marketing da Zion install"):
   - Plano de 8 módulos.
   - Marco Zero de Gestão e Módulo 2 Finanças prontos e testados, com rascunhos desativados no ClickMax.
   - O currículo de Gestão que propus no Comando 04 (6 módulos) **não deve substituir esse plano**.

## 2. Divisão de trabalho proposta entre as sessões

| Sessão | Papel |
|---|---|
| **ZAIOS platform development** (esta) | Arquitetura e estrutura: ZAIOS, Academy, organização do ClickMax (cursos, turmas, entrada gratuita, funil educacional), integração ClickMax ↔ ZAIOS, decisões e premissas, mapa das sessões |
| **Marketing da Zion install** | Produção de conteúdo das jornadas (Jornada 2 em curso), Fábrica Educacional (9 agentes), redesenho da Mentoria de Desenvolvimento (aguarda o "Blueprint Mestre"), sync Meta → ClickMax |
| **Zion infoprodutos catálogo** | Ferramentas de R$ 19 (rodada diária) |
| **Zion Arsenal / Produtos Zion configuration** | Mini mentorias e produtos em rascunho no ClickMax |
| **7 volumes e ebook Zion** | Rotina diária de mídia e CRM (Meta, Google, ClickMax) |
| **Automação de reservas** | Reservas da Zion Bubble (Noite Mágica) |

**Regra:** cada comando do GPT diz para qual sessão ele vai. O que vale fica no repositório; as mensagens entre sessões só avisam.

## 3. Estado que não mudou

- **ZAIOS** (zaios.lovable.app): publicada para teste fechado, **não validada**. O teste humano de 15 itens não foi feito.
- **Premissas financeiras:** decididas para a versão 0 (uma regra só entre Academy e ZAIOS).
- **Conta de vendedor ClickMax:** em análise. Nenhum checkout vende.
- **Nada** foi alterado em produtos, preços, checkouts, automações, Zaya, ZAIOS ou Lovable. Nenhum crédito Lovable gasto desde a publicação.

## 4. Conflitos encontrados no cruzamento (para o Bruno decidir)

1. **Jornada 2:** manter o plano de 8 módulos (recomendado) e encaixar o Acelerador de Vendas do Comando 04 no módulo "Marketing e vendas".
2. **Reserva de manutenção:** 3% na ZAIOS e 4% no Módulo 2 de Gestão. Escolher um valor para os dois.
3. **Três "ZAIOS":** a atual, um projeto antigo "ZAIOS CRM" no Lovable e CRMs em Python no repositório. Confirmar que a oficial é zaios.lovable.app.
4. **Números da Bubble** (diária R$ 1.571 ou R$ 1.568, EBITDA 43,46%, 6 anos): usados em site e materiais sem confirmação registrada. Confirmar ou suspender.
5. **Trilha 1: 43 ou 58 aulas.** O ClickMax tem 58; a Zaya e as páginas dizem 43.
6. **Ofertas que se repetem:**
   - Club Base R$ 270 já inclui a Trilha de Desenvolvimento.
   - Club Pro R$ 2.900 já tem acompanhamento.
   - "Zion Start R$ 970" fica perto do Club Master R$ 980.
   - Recomendação do Comando 04: uma escada só, com o Club como marca e a Academy como conteúdo.
7. **Zion Score** aparece em materiais antigos. A decisão vigente é não usar na ZAIOS nem criar segunda pontuação.

## 5. Decisões do Comando 04 ainda abertas

1. Arquitetura comercial: opção 1 (uma escada só, recomendada) ou opção 2 (Academy separada).
2. Preço das Jornadas 2 e 3 para quem já opera.
3. Programa de 12 semanas como conteúdo do Club Pro / Mentoria; tamanho da turma; quem revisa.
4. Primeiro experimento: experiência gratuita "Venda pelo WhatsApp" ou piloto de Operação (limpeza).
5. Advogado para revisar o módulo de estruturas de parceria.
6. Citar marcas de fornecedores nas aulas e política de parcerias comerciais.
7. Liberar a rede da sessão para conferir fontes primárias (Planalto, gov.br, STJ, Meta, fornecedores).

## 6. Sequência de comandos que sugiro (para esta sessão)

Cada um é só planejamento ou rascunho, sem publicar, até o "aprovado" do Bruno.

1. **Comando 05 · Arquitetura do ClickMax (desenho, sem criar nada).**
   - Mapa de portais, turmas, cursos e produtos: o que existe, o que fica, o que arquiva, o que é novo.
   - Área de entrada gratuita por jornada.
   - Uso do funil educacional "Academia · Jornada do Aluno".
   - Regras de acesso por produto.
   - Depende da decisão comercial (item 5.1).
2. **Comando 06 · Dicionário único Academy + ZAIOS.**
   - Nomes, indicadores, vereditos, premissas e versão, em `docs/academy/DICIONARIO.md` + JSON.
   - Um testador que confere materiais e ZAIOS contra ele.
   - Resolve os conflitos 2, 4 e 5 depois da decisão do Bruno.
3. **Comando 07 · Experiência gratuita do primeiro experimento**, em rascunho local, com medição.
4. **Comando 08 · Integração ClickMax ↔ ZAIOS (plano técnico, depois implementação).**
   - Webhooks de compra e reembolso para liberar acesso.
   - Progresso gravado no lead.
   - Botão "Fazer na ZAIOS".
   - Pede créditos Lovable: só com autorização.

**Antes de tudo:** o teste fechado da ZAIOS pelo Bruno (roteiro em `docs/zaios/teste/roteiro-teste-zaios.pdf`).

## 7. Regras que continuam valendo

GPT define → Claude executa → Claude testa → Bruno encaminha → GPT avalia → Bruno aprova.

**Sem "aprovado" do Bruno:**
- Não alterar produtos, preços, checkouts, automações nem a Zaya.
- Não publicar.
- Não disparar mensagens.
- Não ativar anúncios.
- Não mexer na ZAIOS nem no Lovable.
- Não gastar créditos.
- Não produzir em escala.

Sem dados pessoais de membros ou leads nos documentos.
