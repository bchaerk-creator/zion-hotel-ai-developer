# Plano de execução · Zion Investor Experience

Resposta ao prompt de abertura de docs/MASTER.md, seção 16. Versão de 21 de setembro de 2026.
Nada abaixo é código de componente. A Fase 1 começa depois da aprovação deste plano.

Decisão de localização: o repositório zion-hotel-ai-developer usa a pasta docs/ da raiz
como site público do GitHub Pages. Por isso o projeto vive em zion-investor-experience/,
com seus próprios docs/, data/ e CLAUDE.md. Nada confidencial entra em docs/ da raiz.

---

## 1. Árvore de pastas

```
zion-investor-experience/
├── CLAUDE.md
├── package.json                  next, react, typescript, tailwindcss, framer-motion
├── next.config.ts                output: "export" na Fase 1, imagens AVIF e WebP
├── tailwind.config.ts            tokens de MASTER 13.2, fontes 13.3, breakpoint 900px
├── tsconfig.json
├── postcss.config.mjs
├── docs/
│   ├── MASTER.md                 fonte única
│   ├── PLAN.md                   este arquivo
│   ├── brief.md                  a fornecer
│   ├── territorio.md             a fornecer
│   ├── prototype-public.html     a fornecer, referência aprovada
│   ├── prototype-investor.html   a fornecer, referência aprovada
│   ├── pdf/                      kit de documentos, nomes de data/documents.json
│   └── photos/                   originais em alta, nomes de MASTER 13.4
├── data/
│   ├── types.ts                  tipos de todos os JSON
│   ├── sources.json              todas as fontes, referenciadas por sourceId
│   ├── company.json              posicionamento, fundador, método
│   ├── operations.json           sedes, indicadores 2025 e 1S 2026
│   ├── revenue.json              faturamento por período, R$ 9,88 mi
│   ├── brand.json                avaliações, audiência, comissão de canal
│   ├── model.json                premissas, cenários, forecast 7 anos     investorOnly
│   ├── capex.json                blocos, tiers, opcionais                  investorOnly
│   ├── program.json              23 destinos, ondas, corredores, consolidado
│   ├── raise.json                rodada, tranches, necessidade de caixa   investorOnly
│   ├── returns.json              yield, múltiplo, TIR, comparação Selic   investorOnly
│   ├── platform.json             empresas, modelo de capital, remuneração, valuation, cluster
│   ├── landBank.json             camadas, regiões, indicadores, oportunidades, módulo
│   ├── market.json               tese, números em validação, sustentabilidade, crédito público
│   ├── documents.json            kit e status
│   └── legal.json                rodapé, edições, termos proibidos
├── scripts/
│   ├── validate-data.mjs         valida JSON: fontes, status, aritmética, termos proibidos
│   └── images.mjs                Fase 1: gera AVIF e WebP de docs/photos para public/photos
├── public/
│   ├── photos/                   derivados otimizados, gerados
│   ├── fonts/                    Cormorant Garamond 300 e 400, DM Sans 400 e 500, woff2
│   └── og.jpg
├── src/
│   ├── app/
│   │   ├── layout.tsx            fontes, tokens, Footer, ScrollProgress
│   │   ├── globals.css           reset, tokens CSS, prefers-reduced-motion
│   │   ├── page.tsx              edição pública
│   │   ├── access/page.tsx       formulário de acesso
│   │   ├── investor/
│   │   │   ├── layout.tsx        Fase 3: proteção por NDA. Fase 1: gate simples por variável de ambiente
│   │   │   ├── page.tsx          edição para investidores
│   │   │   └── documents/page.tsx data room
│   │   └── admin/                Fase 4
│   ├── chapters/
│   │   ├── public/               um arquivo por capítulo, 00 a 13
│   │   ├── investor/             capítulos 13 a 21, os demais reutilizam public/
│   │   └── registry.ts           ordem, título, fundo e foto de cada edição
│   ├── components/               lista da seção 3
│   ├── lib/
│   │   ├── data.ts               importa e tipa os JSON, resolve sourceId
│   │   ├── format.ts             moeda, percentual, milhões, sem lógica de número novo
│   │   ├── edition.ts            "public" | "investor", filtra investorOnly
│   │   └── motion.ts             variantes do Framer Motion, hero e statement
│   └── styles/
│       └── typography.css        papéis tipográficos de MASTER 13.3
└── tests/
    ├── data.test.ts              roda validate-data e regras de edição
    └── public-edition.test.tsx   garante que a edição pública não renderiza retorno
```

Stack conforme MASTER 14: Next.js App Router, TypeScript, Tailwind com tokens, Framer Motion.
GSAP não entra na Fase 1. Vídeo do hero só quando o arquivo existir.

---

## 2. Arquivos de /data

Prontos em data/, com tipos em data/types.ts e conteúdo preenchido de docs/MASTER.md.
`node scripts/validate-data.mjs` confere:

- todo sourceId existe em sources.json;
- toda métrica tem period e status válido;
- retorno (yield, múltiplo, ciclo, TIR) só em arquivo com `investorOnly: true`;
- termos proibidos e R$ 11,2 mi ausentes;
- CAPEX: blocos somam o subtotal, subtotal mais contingência e giro dá o total, all-in fecha;
- faturamento: períodos somam R$ 9,88 mi;
- programa: 23 destinos, corredores somam 22 nomeados mais o destino em definição;
- land bank: camadas e regiões somam 6.521,09 ha, capacidade em suítes fecha com o módulo de 12;
- cluster: VPs somam R$ 2,34 mi e cada alocação fecha 100%.

Decisões tomadas ao preencher:

| Ponto | Decisão |
|---|---|
| Faturamento total R$ 9,88 mi | status `estimate`, porque R$ 6,70 mi da soma são estimativa da companhia. O total documentado, R$ 3,19 mi, é `validated` |
| Visualizações acumuladas 60 mi | `estimate`, porque MASTER diz "pela curva de crescimento" |
| Números de mercado | `pending`, selo "Fonte em validação" |
| Linhas de crédito público | `pending` até anexar o regulamento oficial de cada linha |
| Referência de custo por chave de alvenaria | `pending` |
| Valuation dos braços | `estimate`, com nota "estimativa interna, não laudo" |
| Piso interno no CAPEX | mantido com nota de pendência dentro do bloco |
| Terreno como garantia e sócio articulador | só como texto em `platform.reserved`, nunca renderizado |
| Pipeline do land bank, 7 etapas | Identificar, Qualificar, Visitar, Estruturar, Captar, Implantar, Operar. MASTER dá as pontas; as cinco do meio seguem o Método Zion 360, a confirmar com o protótipo |
| Timeline da prova, 5 marcos | 2020, 2023, 2024, 2025, 2026, com notas curtas derivadas de revenue.json, a confirmar com o protótipo |

---

## 3. Componentes e props

Todos em src/components. Nenhum recebe número solto: recebem `Metric`, linhas tipadas ou
os objetos de /data. Nenhum tem canto arredondado, sombra, ícone ou gradiente decorativo.

```ts
type Bg = "black" | "moss" | "cream" | "gold" | "photo";

ChapterHeader   { number: string; total: 13 | 21; title: string }           // alimenta o Header fixo
ScrollProgress  { }                                                          // fio dourado de 2px no topo
Header          { edition: "public" | "investor"; chapters: ChapterMeta[] }   // faixa preta 88% com desfoque

HeroPhoto       { photo: PhotoRef; eyebrow: string; lines: [string, string, string, string];
                  primary: Cta; secondary: Cta }                             // véu .55 a .92
HeroVideo       { src: string; poster: PhotoRef; ...HeroPhoto sem photo }   // só quando o vídeo existir

Statement       { text: string; support?: string; bg?: "black" | "moss" }    // até 3 linhas, caixa alta
Chapter         { id: string; bg: Bg; photo?: PhotoRef; veil?: "phrase" | "block"; children }

BigNumber       { metric: Metric; size?: "lg" | "md" }                       // sempre com SourceBadge
BigNumberGrid   { metrics: Metric[]; columns?: 2 | 4 }                       // vão de 32px
SourceBadge     { sourceId: string; status: MetricStatus; period?: string }  // validado: sublinhado; pendente: tracejado

Chain           { steps: { number: string; label: string; note?: string }[] } // só sequências reais
Ladder          { rungs: string[] }                                          // do mais apagado ao mais escuro
EcosystemDiagram{ core: Company; left: Company[]; right: Company[] }
ProportionBar   { segments: { label: string; share: number; tone: "gold" | "sand" | "cream" }[] }

DataTable       { columns: { key: string; label: string; align?: "left" | "right" }[];
                  rows: Record<string, string | number>[]; totalRowKey?: string;
                  sourceId?: string; status?: MetricStatus }                 // rola no próprio contêiner
RevenueTable    { data: RevenueData }                                        // período, valor, base, selo por linha
ScenarioTable   { scenarios: Scenario[]; showReturns: boolean }             // showReturns só em /investor
ForecastTable   { forecast: ModelData["forecast"]; scenario?: ScenarioId }
CapexTable      { capex: CapexData }

OpportunityCard { opportunity: Opportunity }                                 // grade de 2, fio de 1px
OpportunityGrid { opportunities: Opportunity[] }
ModuleBlock     { module: LandBankData["module"] }                          // o único fundo dourado
LegalStack      { companies: Company[]; providers: Company[] }              // fio dourado vertical

DocumentList    { documents: KitDocument[]; canDownload: boolean }
InvestorForm    { onSubmit: (payload: AccessRequest) => Promise<void> }     // linha inferior, alvos de 48px
Footer          { legal: LegalData; edition: "public" | "investor" }
```

Tipos auxiliares: `PhotoRef = { file: keyof typeof photos; alt: string }`, `Cta = { label: string; href: string }`,
`ChapterMeta = { number: string; title: string; bg: Bg; photo?: PhotoRef }`.

Regra de composição: `ScenarioTable` recebe `showReturns` explícito e a edição pública nunca passa `true`.
O teste public-edition.test.tsx renderiza a edição pública e falha se encontrar qualquer valor de returns.json.

---

## 4. Mapa das duas edições

### Edição pública, indicador "/ 13"

| Nº | Capítulo | Componentes | Fundo | Foto | Dados |
|---|---|---|---|---|---|
| 00 | Intro | HeroPhoto | foto | aerea_mata.jpg | company.tagline, quatro linhas do hero |
| 01 | The Opportunity | Statement, Ladder | preto, preto | | company.story; Ladder: camping, glamping, hospedagem na natureza, destino, hospitality real estate |
| 02 | The Market | Statement, BigNumberGrid, texto de apoio | creme | interior_ceu.jpg como detalhe | market.thesis, market.numbers com selo "fonte em validação" |
| 03 | Brasil | Statement sobre foto, Chain de corredores | creme, foto | bubble_frontal.jpg | program.corridors, program.waves só como lista de destinos, sem ano de retorno |
| 04 | The Founder | Retrato, texto corrido, Chain dos dois trilhos | preto | retrato de Bruno, a fornecer | company.founder, company.method |
| 05 | The Proof | Statement, duas colunas com DataTable e SourceBadge, BigNumberGrid, Chain de 5 marcos, RevenueTable | moss | bubble_deck.jpg, flo_casal_deck.jpg | operations.fy2025, operations.h12026, brand, revenue |
| 06 | Destinations | Statement sobre foto, Chain de 6 ondas | foto | aerea_noturna.jpg | program.waves, notas de Noronha e destino 23 |
| 07 | Ecosystem | EcosystemDiagram, texto | preto | | platform.companies, platform.capitalModel |
| 08 | The Land Bank | Statement, BigNumber, Chain do pipeline, ProportionBar, DataTable de camadas, DataTable de regiões, BigNumberGrid, OpportunityGrid | preto | | landBank |
| 09 | Development | Statement, aérea zenital, ModuleBlock | creme, dourado | aerea_zenital.jpg | landBank.module; sustentabilidade de market.sustainability |
| 10 | The Capital | Statement, texto de apoio, LegalStack resumido | preto | | platform.capitalModel, platform.exclusivity. Sem rodada, sem retorno |
| 11 | Legal Structure | LegalStack, DataTable das empresas | creme | | platform.companies, platform.outsidePerimeter |
| 12 | The Vision | Statement sobre foto | preto, foto | flo_noturna.jpg | company.message |
| 13 | Investor Access | InvestorForm, Footer | moss | | legal.footer |

Ritmo de fundos resultante, do capítulo 01 ao 13: preto, preto, creme, creme, foto, preto, moss, foto,
preto, preto, creme, dourado, preto, creme, preto, foto, moss. Igual ao MASTER 13.2.

### Edição para investidores, indicador "/ 21"

Abre com a linha "Edição para investidores. Uso confidencial, após NDA" acima do hero.
Capítulos 00 a 12 iguais à pública. O acesso passa a ser o capítulo 21.

| Nº | Capítulo | Componentes | Fundo | Foto | Dados |
|---|---|---|---|---|---|
| 13 | The Program | Statement, Chain de ondas com ano, DataTable do consolidado 2032 | preto | | program.consolidated |
| 14 | One Destination | Statement, DataTable de premissas, DataTable de pessoal, texto de configuração | creme | bubble_jacuzzi.jpg | model.assumptions, model.staffing, model.configuration |
| 15 | CAPEX | Statement, CapexTable, DataTable de tiers, BigNumber por chave, opcionais | preto | jacuzzi_zenital.jpg como detalhe | capex |
| 16 | Forecast | ScenarioTable com showReturns, ForecastTable por cenário | preto | | model.year1, model.forecast, aviso do otimista |
| 17 | The Raise | BigNumber, DataTable de necessidade de caixa, Chain das 3 tranches, termos | moss | | raise |
| 18 | The Return | ScenarioTable, DataTable de comparação com Selic, nota de credibilidade | preto | | returns |
| 19 | Zion and Value | DataTable de remuneração, DataTable de valuation, DataTable do cluster, margens da Management | creme | | platform.remunerationPerSite, platform.valuation, platform.organization, platform.management |
| 20 | Documents | DocumentList | preto | | documents, só dataRoom: true |
| 21 | Investor Access | InvestorForm, Footer | moss | flo_deck_mata.jpg como reserva | legal |

Regra: o conservador aparece sempre ao lado do base. Nenhuma tabela mostra o otimista sozinho.

---

## 5. O que ainda depende de informação que não temos

Bloqueia a Fase 1 de "ler igual aos protótipos":

1. docs/brief.md, docs/territorio.md, docs/prototype-public.html e docs/prototype-investor.html não estão no repositório. Sem eles, os textos de apoio e as frases de cada Statement serão escritos a partir do MASTER e precisam de conferência contra o protótipo.
2. As 14 fotos de MASTER 13.4 em docs/photos/. Sem elas o build usa placeholders escuros nas mesmas proporções.
3. Vídeo de drone para o hero. O retrato de Bruno Chaerk chegou em 21/09 e está em public/photos/bruno_chaerk.jpg, com bruno_chaerk_2.jpg como alternativa.

Não bloqueia, mas fica marcado no site:

4. Fontes oficiais dos números de mercado. Hoje entram com selo "fonte em validação".
5. Regulamento das linhas Fungetur, FNE Verde e Fundo Clima para trocar o status de pending para validated.
6. Referência de mercado do custo por chave em alvenaria.
7. Confirmação da linha de piso interno na planilha de CAPEX.
8. Etapas intermediárias do pipeline do land bank e as notas dos cinco marcos da timeline, a conferir com o protótipo.

Pendências de negócio que não afetam o código, herdadas de MASTER 18:

9. Parecer tributário sobre o enquadramento das SPEs.
10. Custo de fabricação da Store, reservado.
11. Área das duas sedes e vínculo formal dos quatro ativos em avaliação.
12. Atualização do teaser, da arquitetura jurídica e do modelo dos 23 destinos para o asset light. Até lá ficam fora do data room, como em documents.json.
13. Troca do faturamento acumulado no one pager e no documento do fundador.
14. Definição do 23º destino e a decisão sobre Fernando de Noronha.
15. Texto jurídico do rodapé revisado por advogado antes de publicar.

Decisões que precisam de resposta antes da Fase 2 e 3, não da Fase 1:

16. Qual CRM recebe o formulário de acesso. O site institucional atual usa HubSpot, portal 51284703.
17. Como será o gate de /investor na Fase 1: senha única por variável de ambiente é o padrão proposto até o login por NDA da Fase 3.
18. Onde o site será publicado. Vercel é o padrão proposto; GitHub Pages da raiz continua com o site institucional.

---

## Estado da Fase 1, 21 de setembro de 2026

Edição pública construída em português, em src/app/page.tsx, com os 14 capítulos do mapa acima,
Header com indicador e fio de progresso, formulário de acesso em /acesso, rodapé jurídico e build
estático em out/. Conferido em 1440px e 360px, sem rolagem horizontal, com e sem prefers-reduced-motion.
O HTML gerado não contém yield, TIR, múltiplo, ciclo, payback, rede de hotéis nem R$ 11,2 mi.

Ajustes feitos em relação ao plano:
- O bloco dourado mostra só módulos e suítes. A linha de hectares por cenário era um cálculo derivado e saiu.
- O hero reduz para clamp(34px, 11vw, 48px) abaixo de 480px, porque "HOSPITALIDADE" não cabe em 48px.
- A classe de espaçamento entre blocos chama-se `.bloco`, para não colidir com a utilidade `block` do Tailwind.
- O formulário guarda o pedido no navegador e confirma. A gravação no CRM é a Fase 2.

## Direção visual, revisão de 21 de setembro de 2026

O fundador pediu "muito verde, luxo natural" e entregou o Branding Guideline Zion Glamping
Collection 2023-2024. Aplicado:

| Token | Antes, MASTER 13.2 | Agora, guia de marca |
|---|---|---|
| black | #040605 | #1A2103, luxnature profundo |
| moss | #1B2117 | #212804, Luxnature |
| leaf | não existia | #A9CAA3, Liveleaf, fundo do capítulo Desenvolvimento |
| cream | #FEF5F0 | #FDF8F2, Isabelline |
| sand | #DED6BF | #E8DDCD, Bone |
| gold | #8B714E | #A68C5D, Camel |
| ink | #16190F | #212804, texto verde sobre creme |

Véus das fotos em verde, logo ZION em Camel, traço do globo do guia no hero e na visão.
Tipografia segue MASTER 13.3: o guia de 2023 usa Playfair Display e Hanken Grotesk, mas o
master de 2026 é a decisão mais recente e proíbe trocar.

Fotos provisórias: 13 imagens extraídas do próprio guia de marca, salvas em public/photos com os
nomes de MASTER 13.4 pelo conteúdo. São JPEGs de PDF, entre 438 e 1920 px de largura. Substituir
pelos originais em alta assim que chegarem, mesmos nomes. Em 21/09 chegaram os originais de aerea_mata, aerea_zenital, bubble_deck e bubble_jacuzzi, mais
uma aérea larga da araucária salva como aerea_araucaria.jpg, usada no capítulo Brasil. O hero voltou
para aerea_mata.jpg. Urubici usa jacuzzi_mata.jpg.

## Próximo passo

Com o plano aprovado, a Fase 1 segue nesta ordem: scaffold do Next.js com tokens e fontes,
lib/data.ts e lib/edition.ts, componentes na ordem em que aparecem na edição pública,
capítulos públicos, capítulos de investidor, testes de edição, build estático e deploy de teste.
