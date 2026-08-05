# ZION ECOSYSTEM — Documento de Contexto Completo (Handoff)

> Cole este documento no início de uma nova conversa para continuar o desenvolvimento do projeto com todo o contexto. Última atualização: agosto/2026, branch `claude/zion-ecogropo-business-plan-g5th3y` do repo `bchaerk-creator/zion-hotel-ai-developer`.

---

## 1. O PROJETO EM UMA FRASE

O **Zion Ecosystem** é a plataforma de economia circular da Zion Hotel Group International em joint venture com a **Ecogrupo**: centros de industrialização de resíduos (CIRO) que coletam lixo de casas, glampings e prefeituras, transformam orgânicos em composto/biogás/créditos de carbono e recicláveis em madeira plástica — e **devolvem parte do valor ao município em mobiliário público** (bancos de praça, carteiras escolares, lixeiras), em troca de um gate fee menor que o custo do aterro.

**Tese central:** "O lixo de uma cidade é o único ativo que o fornecedor paga para entregar e que pode voltar para a população em forma de patrimônio público."

**POSICIONAMENTO DEFINIDO (ago/2026): a Zion é a representante oficial da Ecogrupo no Brasil.** Master representation das 4 frentes: modelo municipal Zero Waste/CIRO, portfólio de produtos, linha exclusiva "Resíduo Zero by Zion" (domos de material reciclado + operação glamping) e captação/expansão. Estrutura completa em `docs/representacao-ecogrupo-brasil.md`.

**Meta de captação: R$ 10 milhões** em créditos verdes federais (blended finance).

---

## 1.1 QUEM É A ECOGRUPO (dado real — deck oficial recebido em ago/2026)

**Holding boliviano de Cochabamba, 23+ anos, "a indústria de economia circular mais importante da Bolívia".** +300 t/mês geridas · +540 t CO2/mês mitigadas · +500 empregos · presença em 2 países. Empresas do grupo: Grow Green (hidroponia), Hydro System, Geocel, Transforma (tubos/pellets) e **Vive Glamping (domos de material reciclado — conexão direta com Zion Glamping)**. Sociedades: GrunTube (200 t plástico/mês), Alimenta (125 t alimentos/mês), Aveco (Rep. Dominicana), Parque Don Bosco (crowdfunding em naves industriais).

**Fatos que mudam o jogo:** (a) o modelo Zero Waste municipal deles opera em 5 municípios bolivianos; no Brasil há pipeline em estruturação em **Senador Canedo e Pirenópolis (GO) — as operações brasileiras AINDA NÃO FORAM INAUGURADAS**: a primeira inauguração do país será conduzida pela representação Zion, e o município que assinar será o pioneiro nacional; (b) a **contrapartida em doações ao município já é playbook contratual deles** (ano 1: 5 casas · ano 2: praça reciclada · ano 3: 2 t de alimentos · ano 4: energia elétrica; redução de 60–80% da disposição final); (c) o caso Sacaba é o blueprint financeiro ("mesmo gasto atual redirecionado do enterro para a industrialização, sem aumentar custo"); (d) portfólio industrial completo: tubos, geoceldas, madeira plástica, geomembranas, casas, domos, naves hidropônicas, proteína BSF, pirólise/biodiesel; (e) internacionalização 2026 mira Brasil, Costa Rica, Rep. Dominicana e Alemanha — **a JV com a Zion é o veículo da entrada no Brasil**.

**Dossiê completo:** `docs/perfil-ecogrupo.md` (deck original é confidencial — não distribuir).

## 2. O QUE JÁ FOI CONSTRUÍDO (entregáveis prontos)

Todos commitados na branch `claude/zion-ecogropo-business-plan-g5th3y`:

| Entregável | Arquivo | Conteúdo |
|---|---|---|
| Plano de captação R$ 10M | `docs/plano-negocio-zion-ecogrupo-economia-circular.md` | Mapa completo dos créditos verdes federais + estratégia híbrida + uso do CAPEX |
| Plano de negócio completo | `docs/plano-negocio-zion-ecosystem.md` | 5 camadas, 7 receitas, 7 etapas de implantação, roteiro ECROI para prefeituras, objeções, escada de 8 degraus |
| Benchmark Orizon | `docs/benchmark-orizon.md` | Dossiê da Orizon (ORVR3) como prova de mercado |
| Apresentação editorial (11 págs) | `docs/apresentacao-prefeituras.html` + artifact `claude.ai/code/artifact/014f1532-6b49-441e-9d57-f38e0d4b683f` | Pitch para prefeituras estilo revista (Cormorant + Aventa, preto/dourado), roteiro ECROI |
| Ebook 79 páginas | `docs/Zion_Ecosystem_Cidade_Circular.pdf` + gerador `tools/gerar_ebook_cidade_circular.py` | "CIDADE CIRCULAR — Como Transformar o Lixo do Seu Município em Patrimônio Público" |
| Perfil Ecogrupo | `docs/perfil-ecogrupo.md` | Dossiê completo extraído do deck oficial (confidencial) |
| Estrutura da representação | `docs/representacao-ecogrupo-brasil.md` | Modelo da representação oficial Zion × Ecogrupo no Brasil: 4 frentes, societário, roadmap de formalização |

---

## 3. O MODELO DE NEGÓCIO

### As 5 camadas da plataforma
1. **Captação de resíduo** (Ecogrupo): contrato municipal + assinaturas residenciais premium (R$ 39–79/mês) + B2B hotéis/glampings
2. **Industrialização** (Ecogrupo): planta CIRO — compostagem acelerada/biodigestor + linha de madeira plástica; rastreabilidade digital por tonelada
3. **Produtos**: composto, biofertilizante, biogás, mobiliário urbano e escolar
4. **Créditos ambientais**: CCRLR (reciclagem) + CRVE (carbono/metano evitado)
5. **Marca e expansão** (Zion): selo "Resíduo Zero by Zion", captação, relação institucional, replicação

### As 7 receitas da tonelada
1. Gate fee municipal (âncora — sempre menor que o custo de aterro)
2. Assinatura residencial B2C
3. B2B + selo Resíduo Zero
4. Venda de composto/biofertilizante
5. Venda de mobiliário de madeira plástica
6. CCRLR — créditos de reciclagem (Decreto 11.413/2023)
7. Créditos de carbono CRVE (Lei 15.042/2024 — SBCE); **regra: carbono é upside, nunca premissa do caso-base**

### Estrutura societária
SPE Zion Ecosystem Ltda: **Zion** = marca, estruturação, captação, institucional | **Ecogrupo** = operação industrial e logística. Contratos municipais na SPE como lastro de recebíveis. Fase 2: securitização (CRA verde, modelo ZION-01/CVM 88).

### Planta-piloto (CIRO) — referências
30–50 t/dia orgânicos + 10 t/dia recicláveis · município de 80–150 mil hab. ou consórcio · área 10–20 mil m² · 25–40 empregos diretos · CAPEX R$ 10M.

**CAPEX:** compostagem/biodigestor R$ 3,8M · madeira plástica R$ 2,4M · logística R$ 1,4M · tecnologia/P&D R$ 1M · licenças R$ 0,5M · giro R$ 0,9M.

---

## 4. A CAPTAÇÃO DOS R$ 10 MILHÕES (mapa dos créditos verdes)

| Fonte | Valor alvo | Tipo | Status/prazo |
|---|---|---|---|
| **Finep Mais Inovação — Economia Circular** | R$ 5M | Crédito + subvenção; projetos R$ 5–20M; exige ICT (UFSC/SENAI/IFSC) e TRL 3–7 | **PRAZO 31/08/2026 — CRÍTICO** |
| **Fundo Clima / BNDES — subprograma resíduos** | R$ 4M | Juros 1–8% a.a. (~6,15%), até 16 anos, 8 de carência, teto R$ 30M/beneficiário/ano | Protocolo após contrato âncora |
| **FNMA / editais MMA** | R$ 1M | Não reembolsável (compostagem comunitária, educação) | Monitorar SINIR+ |
| **Novo PAC Seleções — resíduos** | +R$ 3–5M | Repasse federal; quem pede é a prefeitura/consórcio; carteira ~R$ 1bi/543 municípios | Próximo ciclo — deixar projeto na gaveta |
| CCRLR + carbono | receita/ano | Recorrente desde o mês 1 | Habilitar desde o piloto |

**Lógica:** Finep paga a inovação, Fundo Clima paga a planta, FNMA paga a ponta comunitária, PAC paga a infra municipal, créditos pagam a dívida.

**Precedente-chave:** Fundo Clima já fez 1º aporte em resíduos urbanos (Ciclus, 2025); BNDES aprovou ~R$ 450M para biometano da Orizon — a porta está aberta.

**Regras de captação:** contrato antes de financiamento, sempre. Cada fonte paga o que sabe pagar. CAUC limpo + plano de resíduos atualizado = pré-requisito. Dossiê pronto antes do edital (60–90 dias para montar).

---

## 5. BENCHMARK ORIZON (ORVR3) — a prova de mercado

- Valor de mercado ~R$ 7 bi · IPO 2021 (R$ 554M) · origem Haztec (quase morreu sem foco, dívida 12x EBITDA)
- 18 ecoparques em 12 estados · resíduo de 40 milhões de brasileiros
- Receita 2025: R$ 1,05 bi · EBITDA R$ 500M (**margem 48%**) · lucro R$ 74M
- **Gate fee médio: R$ 84,80/t** (referência nacional de preço)
- 1,1 milhão de créditos de carbono vendidos em 2024; **Google comprou 750 mil**
- Mix receita: ~45% público / 55% privado
- URE Barueri (com Sabesp): 1ª waste-to-energy da América Latina, R$ 550M, 870 t/dia, opera 2027
- **Nosso espaço:** municípios de 30–150 mil hab. que a Orizon ignora + contrapartida visível + marca + narrativa política
- **Frase de pitch:** "Existe uma empresa na bolsa valendo R$ 7 bilhões fazendo isso nas capitais. Nós trazemos o modelo para a sua cidade — com uma diferença: aqui, o lixo volta em forma de praça."
- 4 lições: foco absoluto · mix público-privado · crédito como negócio próprio · CAPEX em parceria

---

## 6. A VENDA PARA PREFEITURAS (o método)

**Princípio:** a venda é política, não técnica. O prefeito não compra tratamento de resíduo — compra **a foto da inauguração da praça feita com o lixo da própria cidade**.

### Ordem de abordagem
1º Secretário de Meio Ambiente/Obras (aliado interno) → 2º Fazenda (economia) → 3º Prefeito (com os dois convertidos) → 4º Procuradoria → paralelo: Câmara. **Nunca chegar ao prefeito frio.**

### Roteiro ECROI da apresentação (11 páginas, 20 min)
- **E (0–3 min):** espelhamento com os números do município ("o senhor paga R$ X/t, R$ Y milhões/ano saindo da cidade")
- **C (3–7):** colapso de "lixo é despesa" + custo invisível: `custo/t × t/ano × 4 anos = R$ milhões enterrados sem uma obra`
- **R (7–11):** reencadramento — contrato de industrialização com retorno em produto; o caminhão que traz de volta
- **O (11–16):** inevitabilidade — caso Orizon (R$ 7 bi), financiamento federal aberto, **protótipo físico do banco na mesa** (o prefeito precisa sentar no banco)
- **I (16–20):** convite — protocolo de intenções (1 página, custo zero, sem exclusividade, sem licitação) + **Diagnóstico Circular gratuito em 30 dias**

**A única meta da 1ª reunião é o protocolo.** O contrato vem como consequência.

### A escada de 8 degraus
1. Reunião técnica (zero) → 2. Apresentação ao prefeito (zero) → 3. **Protocolo de intenções** (zero) → 4. Diagnóstico Circular 30 dias (cortesia) → 5. Contrato (gate fee < aterro + contrapartida trimestral em mobiliário) → 6. Cessão de área → 7. Captação PAC conjunta → 8. Inauguração → replicação (prefeito vende para prefeito)

### Objeções mapeadas (com respostas prontas nos docs)
Orçamento · licitação · risco da empresa · contrato vigente com aterro · catadores · cheiro · ganho político · "por que vocês" · troca de prefeito · cidade pequena demais.

### Erros que matam a reunião
Abrir com tecnologia · slides genéricos · pedir contrato · atacar o modelo atual · prometer carbono como certeza · sair sem próxima data.

### Calendário
Melhor janela: 1º–2º ano de mandato (entregas até 2028). Evitar últimos 6 meses (vedações eleitorais). Priorizar consórcios em regiões de municípios pequenos.

---

## 7. IDENTIDADE VISUAL DAS PEÇAS

- **Apresentação (HTML):** formato editorial revista — Cormorant serif display gigante com contraste de escalas + Aventa; preto `#040605`, creme `#FEF5F0`, sand `#DED6BF`, dourado `#C9A84C`; filetes dourados, citações em itálico dourado; fontes embutidas em base64 (repo `docs/assets/fonts/`)
- **Ebook (PDF/ReportLab):** padrão Zion Ebook Series — preto `#0A0A0A` + dourado `#C9A84C`, Helvetica, capa escura, interlúdios editoriais (substituindo fotos, indisponíveis neste ambiente), módulo ECROI final completo
- **Bordão adaptado:** "Fala comigo, prefeito!" (série municipal; original é "Fala comigo, hoteleiro!")
- Marcas registradas nas peças: Zion Ecosystem™ · CIRO™ · Selo Resíduo Zero by Zion™ · Diagnóstico Circular™

---

## 8. NÚMEROS DE REFERÊNCIA (usados em todas as peças)

Município-modelo de 100 mil hab.: 45 t/dia · 16.400 t/ano · R$ 150/t · **R$ 2,46M/ano · R$ 9,8M/mandato** · R$ 205 mil/mês · R$ 6.700/dia.
Composição do RSU: ~50% orgânico, ~30% recicláveis secos, <20% rejeito. Geração per capita ~0,95 kg/hab/dia. Metano = ~28x CO2. Custo aterro Brasil: R$ 80–200/t.
Caso ilustrativo "Cidade Modelo": gate fee R$ 128/t (−15%), desvio 70% no ano 2, contrapartida 4% do contrato em mobiliário (1 praça + 300 carteiras/ano), breakeven ano 2, margem >35% ano 3.

---

## 9. MARCOS LEGAIS (a "revolução silenciosa")

- **Lei 12.305/2010 (PNRS):** hierarquia, fim dos lixões, logística reversa, responsabilização do gestor
- **Lei 14.026/2020 (Marco do Saneamento):** metas, consórcios/regionalização, PPPs
- **Decreto 11.413/2023:** CCRLR — crédito de reciclagem vendável às indústrias obrigadas (substituiu o Recicla+/Decreto 11.044)
- **Lei 15.042/2024 (SBCE):** mercado regulado de carbono — CBE + CRVE; compostagem/desvio de aterro gera CRVE

---

## 10. ROADMAP E PRÓXIMOS PASSOS

### Urgente (agosto/2026)
1. **Submissão Finep até 31/08/2026** — fechar parceria ICT (UFSC/SENAI-SC/IFSC) esta semana
2. Constituir a SPE Zion Ecosystem Ltda (CNAE tratamento de resíduos)
3. Agenda com Secretaria de Meio Ambiente de Florianópolis (+ município da Rota dos Milagres/AL, onde há MOU)

### Decisões novas a tomar (abertas pelo deck da Ecogrupo)
- [ ] Município âncora: SC/Grande Floripa (base Zion) vs. Goiás (Senador Canedo/Pirenópolis — pipeline Ecogrupo ainda não inaugurado) vs. dois pilotos
- [ ] Regra de honestidade comercial em todas as peças: "23 anos validados na Bolívia, chegando ao Brasil agora" — nunca "já roda no Brasil"
- [ ] Incorporar a hoja de ruta Ecogrupo (casas → praça → alimentos → energia) ao contrato âncora e à apresentação
- [ ] Linha "domos Resíduo Zero": Vive Glamping fornecendo unidades para a rede Zion Glamping
- [ ] Adotar o argumento Sacaba ("mesmo gasto, sem aumento de custo") como alternativa ao desconto de 15% no gate fee
- [ ] Usar o histórico operacional Ecogrupo (23 anos, 2 municípios BR) como credencial técnica na proposta Finep/BNDES

### Fila de produção (pedir na próxima conversa)
- [ ] Personalizar a apresentação com nome e dados reais da 1ª prefeitura-alvo
- [ ] Minuta final do protocolo de intenções (base pronta no Anexo A do ebook)
- [ ] Template do Diagnóstico Circular
- [ ] Esqueleto da proposta Finep (TRL 3–7, projeto cooperado com ICT)
- [ ] Inserir fotos reais nos materiais (acervo não disponível no ambiente atual)
- [ ] Definir URL real do CTA (placeholder: zionhotelgroup.com.br/cidadecircular)
- [ ] Modelagem financeira completa 3 cenários (metodologia Zion: DSCR, valuation de saída)
- [ ] Vídeo 90s do ciclo + one-page do Diagnóstico Circular
- [ ] Próximo volume da série: "Consórcio Circular — Como Municípios Pequenos Somam Escala Industrial"
- [ ] Encomendar 2 protótipos físicos (banco + carteira) em madeira plástica

### Decisões já tomadas (não reabrir)
- **A Zion é a representante oficial da Ecogrupo no Brasil** (master representation, 4 frentes; veículo: Zion Ecosystem Brasil Ltda; formalizar via MOU → acordo definitivo)
- Nome da plataforma: **Zion Ecosystem** | Planta: **CIRO** | Produto de entrada: **Diagnóstico Circular** (gratuito mediante protocolo)
- Estratégia: blended finance (nunca fonte única) · carbono como upside · venda política antes da técnica · protocolo como única meta da 1ª reunião
- Público do ebook: prefeito + secretário + empreendedor local · Bordão municipal: "Fala comigo, prefeito!"

---

## 11. FONTES PRINCIPAIS (verificáveis)

- BNDES/Fundo Clima: bndes.gov.br · Agência Brasil (juros 1–8%)
- Finep: finep.gov.br (chamada Economia Circular, R$ 150M)
- PAC: gov.br/cidades · gov.br/casacivil
- FNMA/MMA: gov.br/mma · sinir.gov.br
- CCRLR: Decreto 11.413/2023 (Planalto) · institutoloop.org.br
- SBCE: Lei 15.042/2024 (Planalto)
- Orizon: ri.orizonvr.com.br · Brazil Journal · Exame · InfoMoney · Seu Dinheiro (site institucional bloqueia acesso automatizado — usar RI e imprensa)
- Setor: panoramas Abrema · SNIS/SINISA

*Todos os valores de editais devem ser confirmados nos instrumentos convocatórios vigentes no momento da submissão.*
