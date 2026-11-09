# Mentoria de Desenvolvimento Hoteleiro Zion 360° · Inventário da estrutura atual (09/11/2026)

Levantamento somente leitura, feito antes de qualquer implementação do novo Blueprint Mestre. Nada foi criado, alterado, renomeado ou apagado. Fora do escopo do redesenho: Gestão Hoteleira (Jornada 2), Operação Hoteleira, Identidade e Vendas.

## 1. ClickMax · workspace Bruno's Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`
Totais vivos: 2.753 contatos · 38 produtos · 7 funis · 73 automações. Vendedor: `pending` (banco aprovado, KYC 06/11, sem motivo). Gateway Ticto. Nenhum checkout nativo vende enquanto o vendedor estiver pendente.

### 1.1 Projetos
| Projeto | id | Conteúdo |
|---|---|---|
| Infoprodutos Zion (padrão) | `8d1152a4-4490-4666-bcb5-582b75c82660` | 33 páginas: Ferramentas R$ 19, Academy 01, 20 ZAR (A01–A10, B01–B10) R$ 27, Club Zion Collection (home, planos, checkout), vitrine |
| Zion Reservas | `7085d5da-a844-40b3-8cfd-2abeae417ef2` | 8 páginas Noite Mágica / Bubble, 1 funil publicado, 2 formulários, 3 fluxos, 1 domínio |
| Projeto de Bruno | `e1c7dc7a-37f9-488d-a686-6e2a5f40f268` | 46 páginas (Lançamento, Club, Curso Faça agora Pilar 0–7, Land Bank, e-books), 6 funis, 71 fluxos, 2 disparos |

### 1.2 Portais de membros
| Portal | id | Turmas | Conteúdos | Membros |
|---|---|---|---|---|
| Zion Hospitality Business (`mentoria-zion`) | `6d1b8c4d-05b0-4bf8-b3ba-5e8e1d0b2b79` | 9 (2 ativas: "Transforme Seu Terreno…" 3 membros, "Turma Fundadores" 1 membro; 7 "Arquivo") | 2 | 11 |
| Zion Land Bank (`zion-land-bank`) | `6d7ceb1c-8aa6-407e-b6c0-23d7b7c80294` | 1 ("Candidatos", padrão, 6 membros, ligada ao produto Inscrição Club + Land Bank) | 2 (Panorama + Trilha 1) | 6 |

### 1.3 Conteúdos (cursos) · 12, nenhum à venda (`availableForSale=false`)
| Conteúdo | id | Estrutura | Situação |
|---|---|---|---|
| **Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso** (Trilha 1 · Desenvolvimento) | `fa9a6c54-e40c-4ee0-99cc-ee6ec70e68fb` | Marco Zero (7) + Pilares 1–7 (5,5,5,6,5,7,7) + Bônus Ferramentas (11) = 58 aulas, todas ativas | **Ativo, em uso por 2 turmas e pelo Land Bank. É a base atual da Mentoria de Desenvolvimento.** |
| **Panorama do Desenvolvimento Hoteleiro · Marco Zero** | `03aa8ff9-a274-4a33-8506-2bdf5dc4d87f` | Marco Zero (10 aulas, 8 ativas) + Suporte e extras (2) | Ativo no Land Bank |
| Jornada 2 · Gestão (rascunho em revisão) | `f1d16209-776d-45c0-a57a-de1c8ce7dd41` | Marco Zero (4) + Módulo 2 Finanças (4), tudo desativado | Fora do redesenho |
| Bônus · Trilha Identidade e Branding | `b449ff2d` | 2 aulas | Fora do redesenho |
| Bônus · Trilha Aceleração de Vendas | `f3bf41a9` | 3 aulas | Fora do redesenho |
| Bônus · Trilha Operação | `2036a7b8` | 2 aulas | Fora do redesenho |
| Bônus · Trilha Gestão | `a28341aa` | 3 aulas | Fora do redesenho |
| Arquivo · Trilha 2 · Gestão | `02363489` | 7 módulos vazios (CAPEX, receitas, P&L, viabilidade, jurídico, capital, lançamento) | Arquivado |
| Arquivo · Trilha 3 · Operação hoteleira | `1d07adf7` | 7 módulos vazios | Arquivado |
| Arquivo · Trilha 4 · Aceleração de vendas | `1775d90d` | 7 módulos vazios | Arquivado |
| Arquivo · Aula gratuita de entrada | `17c64c44` | 7 aulas (desativadas) + 4 e-books + 2 | Arquivado |
| Arquivo · Biblioteca (Z00–Z02, D00–D06, F00–F06) | `6ce56665` | 18 módulos, 36 aulas ativas | Arquivado; é a versão anterior da Mentoria 360° (pilares D e F) |

### 1.4 Produtos e ofertas (38)
- Projeto de Bruno: Mentoria Zion 360° Trilha A, Glamping Vol. 2, Airbnb de Sucesso, Estruturação Zion 360 (Dossiê), Coleção 7 volumes, Trilha 2, Trilha 3, Combo 3 trilhas (ofertas arquivadas); Trilha 1 · Desenvolvimento `046301c3` (oferta incompleta, ligada à turma ativa).
- Infoprodutos Zion: Academy 01, Ferramentas 01/05/11/13/14/17/29, 20 ZAR, Inscrição no Club Zion Collection + Land Bank `38722fcf` (todas com oferta incompleta ou pendente de aprovação; nenhuma vendendo).
- Vendas reais hoje passam pelo Asaas (links no site e na Zaya), não pelo ClickMax.

### 1.5 Funis (7)
Publicado: Noite Mágica (Zion Reservas). Rascunho: Club · Diagnóstico → Hub → Adesão; Aula de Sábado; Ebooks Zion 360; Zion Partnership; Cupom Noite Mágica; Ebook Glamping Vol. 2.

### 1.6 Automações (73 fluxos)
- Ativos ligados ao funil em uso: entrada de lead Meta → CRM; TAG AUTOMÁTICA PREENCHEU FORMULÁRIO; [CRM] Entrada/Passagem das etapas do pipeline Land Bank; Club · Lead do formulário Meta → Zaya (94 contatos); Land Members · Disparo inscrição (173); Método Zion · Comprou Trilha 1 ou Pacote → boas-vindas; Novo aluno (CLUB | MEMBRO) → boas-vindas; Alerta reunião Land Bank agendada.
- Grupos: Funil Land Members, Funil Terreno, Funil Zaya · Sessão de direcionamento, Raio-X Zion (rascunhos), Zion Reservas (rascunhos), ★ EM USO AGORA (3 rascunhos).

### 1.7 Pipelines (17)
Em uso: **★ Land Bank · Formulário → Zaya → Reunião → Venda** `40529cf1` (97 cards; 75 em Novo lead, 12 Zaya qualificando, 5 Ligar hoje, 2 já pagou, 2 reunião agendada, 1 nutrir). Zion Reservas: Reserva Direta (32). Antigos (grupo "z · não usar agora"): 14 pipelines, entre eles FUNIL SDR (1.735 cards), Ligações Bruno (40), Academia · Jornada do Aluno (0, estrutura Z00–Z02 + D/F/E/M/L/G/O), FUNDAÇÃO · Jornada Educacional (0).

### 1.8 Agente de IA
Zaya `db450d9a` · ativa · SDR inbound · claude-sonnet-4-6 · 67 conversas, 20 escaladas · vende Club Zion Collection Base R$ 270 via Asaas. Persona cita "Trilha de Desenvolvimento completa: Marco Zero e 7 pilares, 43 aulas".

### 1.9 Formulários e quizzes (11)
Ativos: Noite Mágica (B); Club · Pré-diagnóstico da aula Marco Zero (3 respostas); Pilar 01 · Território. Rascunhos: Land Bank Diagnóstico da mentoria, Investidores, Mentorias e Premium, Operadores Bubble, Bubble pós-aula, Aplicação Turma Fundadores, Cupom Bio, Fundação Marco Zero.

### 1.10 Integrações
Meta Lead Ads → Windsor → ingest ClickMax (sync horário, tag META | FORM LAND BANK → Zaya). Asaas (pagamentos e webhooks de confirmação no site Lovable). GitHub Pages hospeda vídeos, fichas, planilhas, capas usados pelas aulas.

## 2. Lovable · workspace ZION's Lovable `ZQFE9t8mYPEpsSRKN6YI` (21 projetos)
| Projeto | id | Publicado | Relação com a Mentoria |
|---|---|---|---|
| **Zion Hospitality Platform** (site zionhotelgroup.com: método, planos, Asaas → ClickMax, store, advisor, diagnóstico, land-members) | `dd227afd-30fd-4bce-92c0-2f5aff9dce3f` | sim · editado 07/11 | Vitrine e checkout atual |
| **Zaios** (plataforma dos associados: empreendimentos, ferramentas de capital, receitas, custos, viabilidade, jornada de desenvolvimento e operação, dossiê PDF, login por magic link) | `51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc` | sim · editado 07/11 | Candidata natural a "ferramenta" da Mentoria 360° |
| **Zion Dossie Aulas** (exercícios das aulas ao vivo, endpoint de feedback do mentor virtual para a Trilha 1) | `9b225613-b7e9-44dd-b059-b570171899ec` | sim · 29/10 | Em uso pela Trilha 1 |
| Zion Landing Page (diagnóstico grátis) | `e2f04e7b` | não | |
| Zion Hospitality Ecosystem / Zion Ecossistema (hubs de 6 verticais) | `a4665945` / `f35ca215` | não | Protótipos |
| Zion Land Guide, Zaios Pipeline, Noite Mágica Landing, Zion Access Club, Zion Map, Zion Score Map, Zion Compass, Zion Structure, ZION Hospitality Compass, Zion Glamping Club | vários | não | Protótipos e páginas antigas |
| Airbnb Success Blueprint, Remix (Glamping), Zion Airbnb Guide, Glamping Ventures | vários | 2 publicados | Páginas de e-books |
| Remix of Architect Portfolio Website Template | `059b19fa` | não | Irrelevante |

## 3. Repositório e GitHub Pages
- `docs/trilha1/` (aulas, capas, ferramentas da Trilha 1), `docs/escola/` (Z/D/F: Marco Zero, d00–d06, f00–f06, versão anterior), `docs/clube/`, `docs/land-members/`, `docs/landbank/`, `docs/dossie/`, `docs/raio-x/`, `docs/metodo/`, `docs/p/` (entregáveis discretos), `docs/trilha2/` (Jornada 2, fora do redesenho).
- `producao/planos/` (D00–D06, F00–F06, T00, Z01, Z02: planos editoriais da Mentoria 360° anterior), `producao/clube/`, `producao/fabrica/` (Fábrica Educacional: agentes, padrão de lição, rotinas), `producao/jornada2/`, `producao/catalogo/`, `producao/utilitarios/`, `producao/low-ticket/`, `producao/zion-arsenal/`.
- Skill `zion-learning-design` (52 unidades Z00–Z02 e pilares D, F, E, M, L, G, O).

## 4. Pontos de atenção para o planejamento
1. A Trilha 1 (`fa9a6c54`) está ativa com 4 membros reais em 2 turmas e no Land Bank: qualquer redesenho precisa de turma e conteúdo novos, nunca edição dela.
2. A Zaya e a página do clube prometem "Marco Zero e 7 pilares, 43 aulas": mudar a estrutura da mentoria exige revisar o texto da Zaya (recurso ativo, só com aprovação).
3. Existem duas gerações anteriores da Mentoria 360° (Biblioteca Z/D/F e Trilha 1 em 7 pilares) e um Blueprint Mestre novo: o plano deve dizer o que de cada geração é reaproveitado.
4. Zaios é a única ferramenta com persistência por associado; as fichas do GitHub Pages salvam só no aparelho.
5. Vendedor ClickMax pendente: a venda continua pelo Asaas.
