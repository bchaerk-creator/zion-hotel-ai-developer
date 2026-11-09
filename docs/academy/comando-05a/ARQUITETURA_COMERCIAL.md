# Comando 05A · Arquitetura comercial aprovada e análise de sobreposição

Data: 09/11/2026 · Sessão: ZAIOS platform development · Status: **planejamento. Nada foi alterado.**

## 1. Decisão registrada (Bruno, 09/11/2026)

**Arquitetura C · Ecossistema integrado com ofertas independentes.**

| Peça | Papel |
|---|---|
| **Zion Hotel Academy** | Marca educacional e organização das metodologias (jornadas, método, fábrica) |
| **Zion Collection Club** | Produto de assinatura, com benefícios específicos por plano |
| **Produtos digitais Zion** | Ferramentas (R$ 19) e mini mentorias (R$ 27) autônomas, vendidas individualmente |
| **Mentoria de Desenvolvimento Hoteleiro Zion 360°** | Programa premium independente: 12 semanas, 8 módulos, 8 entregáveis, revisões e defesa final |
| **ZAIOS** | Plataforma tecnológica compartilhada, com permissões por produto |

**Integração comercial não é unificação:** cada produto tem contrato, preço e benefícios próprios. A Mentoria não entra automaticamente em nenhum plano do Club.

**Preservado, sem nenhuma alteração:**
- Trilha 1, Jornada 2 (Gestão), Operação, Identidade e Vendas.
- Land Bank, Club, Zaya.
- Produtos, preços, checkouts, automações, funis.
- Participantes e direitos de acesso atuais.

## 2. Fontes e limites desta análise

**Lido nesta sessão, só em leitura:**
- ClickMax: 37 produtos e ofertas, portais, turmas, módulos da Trilha 1, tags de compra (só contagens), funil em uso, configuração da Zaya.
- Páginas do site: `docs/club-zion-collection/`, `inscricao/`, `land-members/`, `inscreva/`, `metodo/oferta/`, `previa/trilha1/`, `lancamento/hub.html`, `lancamento/aula.html`.

**Não consegui verificar:**
- **Asaas:** o Club Base é cobrado por link do Asaas e não há acesso a ele nesta sessão. A lista real de quem pagou fora do ClickMax precisa vir do Bruno.
- **Hotmart:** o "Zion Start R$ 970" e 9 e-books aparecem só numa sessão de agosto, como checkout pendente na Hotmart. Não estão no repositório nem no ClickMax.
- **Blueprint Mestre da Mentoria:** **não está no repositório nem nas sessões.** Tudo sobre a Mentoria abaixo usa só o que o comando descreve (12 semanas, 8 módulos, 8 entregáveis, revisões, defesa final).
- **Classificação da linha B:** pedida à sessão do Zion Arsenal em 09/11; entra na seção 4 quando chegar.

Este repositório é público: as contagens de compradores aparecem em faixas, sem dados pessoais.

---

## 3. Matriz de ofertas e benefícios

### 3.1 Ofertas ativas ou em uso comercial

| Produto | Preço e cobrança cadastrados | Status de venda | Público | Promessa | Entrega efetiva | Benefícios e acesso | Humano? | Sobreposição | Recomendação | Impacto em clientes atuais |
|---|---|---|---|---|---|---|---|---|---|---|
| **Club Base** | R$ 270 à vista ou 6x R$ 45; anual; link Asaas. No ClickMax há a oferta "Inscrição no Club Zion Collection + Land Bank", R$ 270, **incompleta** | **Vendido** (Zaya, página do Club, reunião) | Donos de terreno, primeiro projeto | "Aprenda o passo a passo para transformar o seu terreno"; "possibilidade" de parceria e investimento, sem garantia | Trilha 1 completa: **58 aulas no ClickMax** (as páginas e a Zaya dizem **43**); planilhas, exercícios, Dossiê; módulo bônus com 11 mini mentorias | Acesso anual; reunião de diagnóstico; mapa de direcionamento; masterclass às quintas; suporte; inscrição no Land Bank | Sim (reunião, masterclass, suporte) | Trilha 1 avulsa (R$ 297); inscrição Land Bank (R$ 97/R$ 270); página do Método (R$ 270); linha B (já inclusa como bônus) | **Manter** como porta de entrada principal; acertar 43 ou 58 aulas | É o produto com compradores (poucos, menos de 10 por tag, inclusive nos modelos antigos de R$ 97 e R$ 270). Direitos a preservar: ano de acesso, Trilha 1, Land Bank, reunião, masterclass |
| **Club Master** | R$ 980 à vista ou 12x R$ 81,67 | **Não vende** ("link de pagamento em preparação") | Quem já opera hospedagem e quer encher o calendário | "Do desenvolvimento à gestão, à operação e às vendas" | **Ainda não existe:** promete trilhas de Gestão, Operação e Aceleração de vendas (Gestão em produção: 2 de 8 módulos), Mapa do Calendário Vazio e Plano de 90 Dias | Tudo do Base + trilhas + aulas ao vivo | Sim (aulas ao vivo) | Jornadas 2 e 3 da Academy; mini mentorias A | **Manter em pausa** até o conteúdo existir; reposicionar como o plano do operador (perfis C e D) | Nenhum comprador registrado |
| **Club Pro** | R$ 2.900 à vista ou 12x R$ 241,67 | **Não vende** ("link de pagamento em preparação") | "Do terreno à operação, com a Zion acompanhando" | Acompanhamento do projeto | Reuniões semanais de acompanhamento (não estruturadas) | Tudo do Base e do Master + reuniões semanais | Sim | **Mentoria Premium**, com o mesmo preço e o mesmo apelo de acompanhamento semanal | **Diferenciar** (seção 5): o mesmo preço e a mesma promessa da Mentoria confundem | Nenhum comprador registrado |
| **"Mentoria R$ 2.900"** (vendida na reunião do funil em uso) | R$ 2.900; sem oferta no ClickMax; tag "COMPROU \| MENTORIA 2900" | Ofertada na reunião com o closer | Leads qualificados do formulário | Acompanhamento | Não definido; deve ser a Mentoria Premium do Blueprint | — | Sim | Club Pro (mesmo preço) | **Reposicionar** como a Mentoria de Desenvolvimento Zion 360° (Blueprint), com preço próprio | Nenhum comprador registrado (tag com 0) |
| **"Trilha + Clube R$ 490"** (vendida na reunião) | R$ 490; tag "COMPROU \| TRILHA + CLUBE 490" | Ofertada na reunião | Leads da reunião | Trilha + Club | Não documentado | Não documentado | ? | **Mesmo preço da Consultoria prévia (R$ 490)**, que é outro produto; e perto do Club Base | **Diferenciar ou descontinuar**: definir o que é, ou tirar da reunião | Nenhum comprador registrado |
| **Consultoria prévia com o Bruno** | R$ 490 (10x R$ 49); "vira crédito na assessoria" | Em páginas públicas (`inscreva`, `metodo/oferta`) | Quem quer falar com o Bruno antes | 45 min para entender a etapa e o próximo passo | Reunião de 45 min | Crédito na "assessoria" (produto não definido hoje) | Sim | "Trilha + Clube R$ 490"; reunião de diagnóstico do Base | **Avaliar**: manter só se a "assessoria" de destino existir (a Mentoria pode ser esse destino) | Tag "MÉTODO \| COMPROU CONSULTORIA PRÉVIA" com 0 |
| **Inscrição no Land Bank** | R$ 97 (modelo antigo) e R$ 270 (`inscreva`, `previa/trilha1`) | R$ 97 encerrado; R$ 270 = Club Base na prática | Donos de terreno | Inscrever a área no banco de áreas | Inscrição + Dossiê prévio + Trilha 1 | Land Bank | Avaliação pela equipe | Club Base | **Manter o Land Bank como benefício** (do Base e da Mentoria), não como produto separado | Quem pagou R$ 97 ou R$ 270 nos modelos antigos mantém a inscrição (tag "RAIOX \| PAGOU R$270", menos de 5) |
| **Ferramentas de R$ 19** (01, 05, 11, 13, 14, 17, 29) | R$ 19, pagamento único, Pix e cartão | Rascunho no ClickMax (vendedor em análise) | Anfitriões e operadores | "Aprenda o passo a passo para..." (um problema) | Planilha, guia e PDF, testados | Arquivo ou link | Não | Pequena: algumas tocam a Jornada 3 (limpeza, enxoval, ocorrências) e a ZAIOS (custos) | **Manter** como produto digital autônomo | Sem vendas (checkout não vende) |
| **Mini mentorias A01–A10** (anfitriões) | R$ 27 | Rascunho no ClickMax | Anfitriões com calendário vazio | Um problema por produto | 40 telas, cálculo, PDF | Link | Não | Jornadas 2 e 3 (complementar); Club Master (futuro) | **Manter** como produto digital autônomo e porta para a Jornada 2 | Sem vendas |
| **Mini mentorias B01–B10** (donos de terra) | R$ 27 | Rascunho no ClickMax | Donos de terreno | Investimento, sócio, capital, viabilidade, pitch | 40 telas, cálculo, PDF | Link | Não | **Já inclusas como bônus na Trilha 1 (Club Base)**; tocam Land Bank, Mentoria e ZAIOS | **Aguardando a classificação** pedida ao Arsenal (seção 4) | Sem vendas avulsas; quem tem o Base já recebe |
| **Mentoria de Desenvolvimento Hoteleiro Zion 360°** (premium) | **A definir** | Não existe como oferta | Projetos qualificados (candidatura) | Programa de 12 semanas, 8 módulos, 8 entregáveis, revisões, defesa final | **Aguarda o Blueprint Mestre** | Próprios do programa | Sim (central) | Club Pro; "Mentoria R$ 2.900" | **Criar só a partir do Blueprint**, sem incluir em plano do Club | Nenhum |
| **ZAIOS** | Não é produto vendido | Teste fechado (lista de liberados) | Membros | — | Desenvolvimento e Operação; Dossiê | Hoje só por liberação manual | — | Planilhas que fazem a mesma conta | **Plataforma compartilhada** com permissão por produto (seção 6) | Ninguém pagou por ela |

### 3.2 Ofertas antigas ou paradas

| Produto | Preço | Status | Recomendação |
|---|---|---|---|
| Trilha 1 avulsa (ClickMax) | R$ 297 | Oferta incompleta, nunca vendeu | **Avaliar descontinuação**: o Club Base entrega mais por R$ 270 |
| Trilha 2 Gestão, Trilha 3 Operação | R$ 297 cada | Arquivadas | Manter arquivadas; a Jornada 2 nova não deve usar esses produtos |
| Combo 3 trilhas | R$ 890 | Arquivado | Manter arquivado |
| Mentoria Zion 360° · Trilha A | R$ 15.900 | Arquivada | Manter arquivada (histórico) |
| Aula "Transforme seu terreno" | R$ 47 | Turma arquivada; página `lancamento/aula.html` pública | Avaliar tirar a página do ar (não agora) |
| "O projeto em 6 meses · 6 jornadas" | 6x R$ 549 | Página `lancamento/hub.html` pública, oferta antiga | **Atenção:** página pública com escada antiga ("6 jornadas", "rede de investidores"). Avaliar tirar do ar ou marcar como encerrada (não agora) |
| Estruturação Zion 360 · Dossiê; Coleção Método 7 volumes; Glamping Vol. 2; "Como criar um Airbnb de sucesso" | — | Arquivados | Manter arquivados |
| "Zion Start" (Hotmart) e 9 e-books | R$ 970 (e-books: NV) | Não verificado | Bruno confirma se existe na Hotmart; se existir, está perto do Club Master (R$ 980) |

---

## 4. Linha B do Zion Arsenal

Pedido feito à sessão responsável: classificar B01 a B10 em:
1. Autônomo.
2. Complementar, exige diferenciar a promessa.
3. Sobreposição significativa.

**Fato já confirmado:** o módulo "Bônus · Ferramentas Zion Collection Club" da Trilha 1 entrega 11 mini mentorias sobre investimento, sócio, capital, potencial turístico, custo de implantação, modelo, retorno, implantação por etapas, pitch e viabilidade. Ou seja, **quem compra o Club Base já recebe a linha B.**

Vender a linha B avulsa continua possível como produto de entrada. A promessa precisa deixar claro que é uma ferramenta pontual, e não a trilha, o Land Bank nem a Mentoria.

*(Classificação da sessão: pendente; será acrescentada aqui.)*

---

## 5. Mapa de sobreposições e proposta de diferenciação

### 5.1 Sobreposições

| # | Onde | Gravidade |
|---|---|---|
| 1 | **Club Pro (R$ 2.900, reuniões semanais) x Mentoria Premium ("Mentoria R$ 2.900")** | Alta: mesmo preço, mesmo apelo |
| 2 | **"Trilha + Clube R$ 490" x Consultoria prévia R$ 490** | Alta: mesmo preço, produtos diferentes |
| 3 | Club Base x Trilha 1 avulsa R$ 297 x inscrição Land Bank R$ 270 x página do Método R$ 270 | Média: quatro portas para quase a mesma coisa |
| 4 | Club Master promete trilhas que ainda não existem | Média: só vira problema se começar a vender |
| 5 | Linha B avulsa x bônus do Club Base | Baixa ou média: depende da promessa |
| 6 | "43 aulas" (páginas, Zaya) x 58 no ClickMax | Baixa: corrigir o texto (com "aprovado") |
| 7 | Páginas públicas antigas (6 jornadas R$ 549, aula R$ 47) | Média: escada antiga visível |

### 5.2 Um papel para cada produto

| Produto | Papel (o que resolve) | Profundidade | Humano |
|---|---|---|---|
| Ferramenta R$ 19 | Um problema pontual, em uma sessão | Ferramenta | Não |
| Mini mentoria R$ 27 | Um diagnóstico com relatório | Ferramenta guiada | Não |
| **Club Base** | Um ano de acesso ao caminho do terreno ao projeto, com Land Bank | Trilha gravada + encontros coletivos | Coletivo (masterclass) + 1 reunião |
| **Club Master** (quando houver conteúdo) | O caminho do operador: gestão, operação e vendas | Trilhas + aulas ao vivo coletivas | Coletivo |
| **Club Pro** | **Acompanhamento contínuo** do projeto ao longo do ano de assinatura | Assinatura com encontros periódicos | Sim, recorrente e sem currículo fechado |
| **Mentoria Premium** | **Programa fechado de transformação:** 12 semanas, 8 entregáveis revisados, defesa final, turma com candidatura | Programa | Sim, intensivo e com começo, meio e fim |

**Opções para separar Club Pro e Mentoria (decisão do Bruno):**
- **A (recomendada):** manter o Pro a R$ 2.900, mas trocar "reuniões semanais" por um ritmo de assinatura, por exemplo encontro mensal ou quinzenal em grupo. A Mentoria fica com o preço próprio do Blueprint e com o semanal intensivo.
- **B:** o Pro deixa de existir até a Mentoria estar pronta.
- **C:** manter os dois iguais em preço, com o Pro dando desconto na Mentoria. Não recomendo, porque mantém a confusão.

---

## 6. Regras preliminares de acesso (Academy, Club, ZAIOS)

Princípio: **cada oferta libera um conjunto fixo de direitos**, gravado no momento da compra e com prazo. A ZAIOS e o ClickMax leem o mesmo conjunto. A integração por webhook fica para depois, com autorização.

| Produto | ClickMax (turma ou curso) | ZAIOS | Prazo | Land Bank |
|---|---|---|---|---|
| Ferramenta R$ 19 | Entrega por arquivo ou link | — | Vitalício (arquivo) | — |
| Mini mentoria R$ 27 | Entrega por link | — | Vitalício | — |
| Club Base | Trilha 1 + portal do Land Bank | Jornada Desenvolvimento (P1 a P6) e Dossiê | 12 meses | Sim |
| Club Master | Base + Jornadas 2 e 3 | + Jornada Operação (V1, V2, G1, G2, G3) | 12 meses | Sim |
| Club Pro | Master + área de acompanhamento | Tudo do Master + revisão pela equipe (com consentimento do membro) | 12 meses | Sim |
| Mentoria Premium | Curso próprio (8 módulos) + turma da edição | Jornada Desenvolvimento + revisão dos 8 entregáveis pela equipe | 12 semanas do programa + prazo de consulta a definir | Sim (decisão) |

**Regras gerais:**
1. **Quem já comprou mantém exatamente o que comprou.** Nada é retirado por causa da arquitetura nova.
2. Um membro pode ter vários produtos; os direitos se somam, sem duplicar conteúdo.
3. A Mentoria não entra em plano do Club, e o Club não dá a Mentoria.
4. A ZAIOS mostra só o que o produto libera. Sem produto válido, o membro vê seus dados em modo leitura e pode baixá-los ou excluí-los, como já acontece hoje.
5. A permissão vem da compra confirmada (webhook ou liberação manual registrada), nunca de uma tag sozinha.

---

## 7. Impacto sobre clientes atuais

- **Compradores registrados no ClickMax:** poucos (menos de 10 por tag), todos na entrada do terreno (Trilha 1 + Land Bank, inclusive os modelos de R$ 97 e R$ 270). Membros nas turmas da Trilha 1 e no portal do Land Bank.
- **Club Master, Club Pro, Mentoria R$ 2.900, Trilha + Clube R$ 490, Consultoria R$ 490:** nenhum comprador registrado.
- **Pagamentos pelo Asaas** (Club Base) não aparecem no ClickMax. **O Bruno precisa confirmar a lista** para que ninguém perca o acesso.
- **Direitos a preservar:**
  - Acesso anual à Trilha 1.
  - Inscrição no Land Bank.
  - Reunião de diagnóstico.
  - Masterclass.
  - "Novos conteúdos ao longo do ano" (promessa genérica do Base; não obriga a dar Gestão nem Operação).
- **Risco principal:** quem comprou pelos modelos antigos (R$ 97 ou "Trilha + Clube") com promessas diferentes. Conferir o que foi prometido a cada um antes de qualquer mudança.

---

## 8. Pendências que exigem decisão do Bruno

1. **Blueprint Mestre da Mentoria:** enviar. Sem ele, a Mentoria não é desenhada.
2. **Club Pro x Mentoria:** escolher a opção A, B ou C (seção 5.2) e o preço da Mentoria.
3. **"Trilha + Clube R$ 490":** definir o que é ou tirar da reunião; e se a Consultoria prévia R$ 490 continua (e para qual "assessoria" vira crédito).
4. **Trilha 1 avulsa R$ 297** (incompleta): descontinuar?
5. **43 ou 58 aulas:** número oficial (para corrigir páginas e Zaya, com "aprovado").
6. **Páginas públicas antigas** (`lancamento/hub.html` 6x R$ 549, `lancamento/aula.html` R$ 47): manter, marcar como encerradas ou tirar do ar.
7. **Club Master:** manter em pausa até as Jornadas 2 e 3 existirem?
8. **Lista de compradores pelo Asaas e pela Hotmart** ("Zion Start" e e-books), para preservar acessos.
9. **Land Bank na Mentoria:** a Mentoria inclui inscrição no Land Bank?
10. **Prazo de acesso à ZAIOS** depois das 12 semanas da Mentoria.

---

## 9. Orientações enviadas às sessões (sem alterações)

| Sessão | Orientação |
|---|---|
| Marketing da Zion install | Mentoria Premium independente, só a partir do Blueprint, sem incluir em plano do Club e sem confundir com a Trilha 1 |
| Zion Arsenal | Classificar a linha B (pedido enviado); não excluir produtos nem alterar criativos |
| Produtos Zion configuration | Nada muda nos 26 rascunhos; usar esta matriz antes de qualquer ajuste de oferta |
| Zion infoprodutos catálogo | Ferramentas seguem como produtos digitais autônomos; sem prometer Club, Land Bank ou Mentoria |
| 7 volumes e ebook Zion | Nenhuma campanha muda; a Zaya não muda |
