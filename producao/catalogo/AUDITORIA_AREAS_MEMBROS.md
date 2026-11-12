# Auditoria das áreas de membros (ClickMax) · 12/11/2026

Levantamento só de leitura. Nada foi criado, editado, ativado ou apagado. Sem nomes nem e-mails de alunos. Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`.

## Resumo (10 linhas)

1. Hoje há **3 portais** (Zion Hospitality Business, Zion Land Bank, Zion Collection), **13 turmas** e **15 conteúdos**. Nenhum é chamado Desenvolvimento, Gestão ou Operação.
2. O portal Hospitality tem 10 turmas, mas só 3 têm conteúdo. As outras 7 estão vazias (6 com prefixo "Arquivo", mais "Turma Fundadores", que repete o curso do Terreno).
3. **Duplicidade real:** "Transforme Seu Terreno..." (58 aulas) aparece em 3 turmas: Terreno e Fundadores (portal Hospitality) e Land Bank Candidatos (outro portal). É o mesmo conteúdo (mesmo id), não uma cópia.
4. "Biblioteca · Método Zion 360°" (36 aulas, 18 módulos) tem 0% de aulas com o mesmo nome ou o mesmo link que o curso do Terreno. É outro material (e-books Z/D/F), do mesmo tema.
5. **De onde vêm os números do Bruno:** Land Bank ~70 = Panorama Marco Zero (12) + Terreno (58). "Terreno ~50" = as 47 aulas de Marco Zero e Pilares 1 a 7, sem as 11 de bônus. A turma do Terreno mostra 94 porque soma a Biblioteca (36).
6. O conteúdo **mais completo para Desenvolvimento** é o Terreno (`fa9a6c54`): 17 vídeos, 8 "Faça agora", 11 PDFs e 11 ferramentas de bônus. Falta certificado, e só 8 dos 17 vídeos têm duração cadastrada.
7. Gestão (`f1d16209`) está completa: 8 módulos de 4 aulas (vídeo, "Faça agora", resumo em PDF, planilha). **Operação não tem aulas**: só o conteúdo "Arquivo · Trilha 3" desabilitado, com 7 módulos vazios.
8. Nenhuma aula habilitada está sem vídeo/arquivo/link. As únicas aulas vazias são as 7 do "Arquivo · Aula gratuita" (desabilitadas) e 1 aula de texto com conteúdo no Land Bank.
9. Das 156 URLs de aula, 134 responderam 200 no HEAD; 22 o proxy bloqueou (YouTube, Gamma, Airtable, wa.me, clickmax.space), então não foi possível checar. Nenhuma deu erro 4xx/5xx.
10. Das 10 ofertas que entregam área de membros, só 2 estão aprovadas (Zion Collection 06 e o complemento). 5 estão arquivadas e 3 incompletas ou com correções. Proposta de 3 portais no fim.

## 1. Portais, turmas e conteúdos

Alunos: só contagem (`totalMemberUsers` da turma; o mesmo aluno pode estar em mais de uma turma).

### Portal Zion Hospitality Business (`6d1b8c4d-05b0-4bf8-b3ba-5e8e1d0b2b79`, subdomínio `mentoria-zion`, 12 alunos no portal)

| Turma | id | Alunos | Conteúdos ligados (aulas) | Produtos/ofertas ligados |
|---|---|---|---|---|
| Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso | `a490c3c8` | 3 | Terreno (58) + Biblioteca (36) = 94 | Trilha 1 · Desenvolvimento (R$ 970, incompleta); Combo 3 trilhas (arquivado) |
| Turma Fundadores · Mentoria em grupo | `2c33680d` | 1 | Terreno (58) + Biblioteca (36) = 94 | nenhum |
| Jornada 2 · Gestão | `294be538` | 1 | Gestão (32) + Bônus Gestão (3) = 35 | Trilha 2 · Gestão (R$ 297, arquivada); Combo (arquivado) |
| Club Zion Collection · Kit de Captação | `8cd230af` | 1 | Kit Inicial · Como captar recursos (4) | Kit de Captação + sessão (R$ 97, pending_corrections) |
| Arquivo · Turma A · Quero começar (padrão) | `3149fca9` | 1 | nenhum | Mentoria Trilha A (R$ 15.900, arquivada) |
| Arquivo · Trilha 3 · Operação | `0da5717a` | 1 | nenhum | Trilha 3 · Operação (R$ 297, arquivada); Combo (arquivado) |
| Arquivo · Aula Transforme seu terreno · R$ 47 | `92920c1c` | 1 | nenhum | nenhum |
| Arquivo · Turma B · Quero crescer | `50304eb7` | 1 | nenhum | nenhum |
| Arquivo · Zion Land Society · Membro | `af41e392` | 1 | nenhum | nenhum |
| Arquivo · Fundação · Acesso Livre | `d5c94c5e` | 1 | nenhum | nenhum |

### Portal Zion Land Bank (`6d7ceb1c-8aa6-407e-b6c0-23d7b7c80294`, subdomínio `zion-land-bank`, 7 alunos)

| Turma | id | Alunos | Conteúdos ligados (aulas) | Produtos/ofertas ligados |
|---|---|---|---|---|
| Zion Land Bank · Candidatos (padrão) | `6d9cd29e` | 7 | Panorama Marco Zero (12) + Terreno (58) = 70 | Inscrição Club + Land Bank (R$ 270, incompleta, erro de gateway "Token inválido"); Inscrição no clube R$ 97 (arquivada) |

### Portal Zion Collection (`a8e2157a-4b62-40de-955e-72662d99c195`, subdomínio `zion-collection`, 2 alunos)

| Turma | id | Alunos | Conteúdos ligados (aulas) | Produtos/ofertas ligados |
|---|---|---|---|---|
| Compradores · Seu Airbnb Está Vazio? | `75cf8dc3` | 1 | Seu Airbnb Está Vazio? (6) | ZC06 R$ 47 (aprovada) |
| Compradores · Calendário comercial de 30 dias | `ecdb5762` | 1 | Calendário comercial (2) | ZC06 complemento R$ 19 (aprovada) |

## 2. Conteúdos (cursos): módulos, aulas e jornada

"Em turmas" mostra onde aparece. Aulas = soma de todos os módulos.

| Conteúdo | id | Habilitado | Módulos | Aulas | Em turmas | Jornada |
|---|---|---|---|---|---|---|
| Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso | `fa9a6c54` | sim | 9 | 58 | Terreno, Fundadores (Hospitality); Land Bank Candidatos | **Desenvolvimento** (Marco Zero + Pilares 1–7 + Bônus) |
| Panorama do Desenvolvimento Hoteleiro · Marco Zero | `03aa8ff9` | sim | 2 | 12 (2 desabilitadas) | Land Bank Candidatos | Land Bank (entrada, parte repete o Marco Zero) |
| Biblioteca · Método Zion 360° | `6ce56665` | sim (certificado ligado) | 18 | 36 | Terreno, Fundadores | Outro/Arquivo: biblioteca de e-books Z00–Z02, D00–D06, F00–F06 |
| Jornada 2 · Gestão | `f1d16209` | sim | 8 | 32 | Jornada 2 · Gestão | **Gestão** |
| Bônus · Trilha Gestão · Ferramentas Club | `a28341aa` | sim | 1 | 3 | Jornada 2 · Gestão | Gestão (ferramentas) |
| Bônus · Trilha Operação · Ferramentas Club | `2036a7b8` | sim | 1 | 2 | nenhuma | Operação (ferramentas, sem turma) |
| Bônus · Trilha Identidade e Branding · Ferramentas Club | `b449ff2d` | sim | 1 | 2 | nenhuma | Ferramentas (sem turma) |
| Bônus · Trilha Aceleração de Vendas · Ferramentas Club | `f3bf41a9` | sim | 1 | 3 | nenhuma | Ferramentas (sem turma) |
| Kit Inicial · Como captar recursos | `03378be0` | sim | 1 | 4 | Club Kit de Captação | Outro/Clube |
| Seu Airbnb Está Vazio? | `5d3c9a1b` | sim | 1 | 6 | Compradores ZC06 | Outro/Zion Collection |
| Calendário comercial de 30 dias | `3edca845` | sim | 1 | 2 | Compradores Calendário | Outro/Zion Collection |
| Arquivo · Trilha 2 · Gestão | `02363489` | não | 7 | 0 | nenhuma | Arquivo (módulos vazios) |
| Arquivo · Trilha 3 · Operação hoteleira | `1d07adf7` | não | 7 | 0 | nenhuma | Arquivo (**é o único esqueleto de Operação**) |
| Arquivo · Trilha 4 · Aceleração de vendas | `1775d90d` | não | 7 | 0 | nenhuma | Arquivo (módulos vazios) |
| Arquivo · Aula gratuita de entrada | `17c64c44` | não | 3 | 13 (7 desabilitadas) | nenhuma | Arquivo |

Total: 15 conteúdos, 11 habilitados, 4 desabilitados. Aulas: 58 + 12 + 36 + 32 + 3 + 2 + 2 + 3 + 4 + 6 + 2 + 13 = **173**, das quais 156 têm URL (as outras: 7 vídeos vazios da aula gratuita, 1 texto e as 0 dos esqueletos).

## 3. Aulas por tipo e estado

| Conteúdo | Vídeo | Link externo | Arquivo/PDF | Texto | Habilitadas | Sem vídeo ou material |
|---|---|---|---|---|---|---|
| Terreno | 17 | 30 | 11 | 0 | 58/58 | 0 |
| Panorama Marco Zero | 3 | 6 | 2 | 1 | 10/12 | 0 (texto tem conteúdo) |
| Biblioteca | 0 | 36 | 0 | 0 | 36/36 | 0 |
| Gestão | 8 | 16 | 8 | 0 | 32/32 | 0 |
| Bônus (4 conteúdos) | 0 | 10 | 0 | 0 | 10/10 | 0 |
| Kit Captação | 1 | 1 | 2 | 0 | 4/4 | 0 |
| Seu Airbnb Está Vazio? | 2 | 1 | 3 | 0 | 6/6 | 0 |
| Calendário 30 dias | 0 | 0 | 2 | 0 | 2/2 | 0 |
| Aula gratuita (arquivo) | 7 | 6 | 0 | 0 | 6/13 | **7 vídeos sem URL** (desabilitados) |

- **Aulas habilitadas sem nada para o aluno: 0.** Aulas incompletas: as 7 vídeos vazios da "Aula gratuita de entrada" (desabilitados, conteúdo arquivado) e 2 e-books do Gamma desabilitados no Panorama.
- **Vídeo hospedado:** Terreno e Panorama usam YouTube (`youtu.be`, 19 links); Gestão, Land Bank, ZC06 e Kit usam arquivo `.mp4` no GitHub Pages ou raw.githubusercontent.
- **URLs (HEAD, 8 s):** 156 únicas, 134 com 200, 22 sem resposta por bloqueio do proxy (17 YouTube, 2 Gamma, 1 Airtable, 1 wa.me, 1 clickmax.space; não é prova de link quebrado). Nenhum 404.
- **Aulas de exercício/ferramenta** (palavras exercício, ferramenta, planilha, ficha, Faça agora, Bônus no nome): Terreno 29 (8 "Faça agora" + 11 "Bônus" + fichas e aulas interativas), Gestão 16 (8 "Faça agora" + 8 planilhas), Panorama 5, Bônus 10, Kit 1, ZC06 1, Calendário 1, Biblioteca 0. Todos os links de ferramenta são páginas ou planilhas no GitHub Pages.
- A Biblioteca é só e-book e aula em link (sem vídeo, sem exercício); é a única com certificado ligado.

## 4. Duplicidades

| Par | Mesmo título? | Módulos com mesmo nome | Aulas com mesmo nome | Aulas com mesmo link | Leitura |
|---|---|---|---|---|---|
| Terreno em 3 turmas (Terreno, Fundadores, Land Bank) | sim, mesmo id | 100% | 100% | 100% | **Duplicidade de acesso, não de conteúdo**: um curso só, ligado 3 vezes. Fundadores é só um segundo canal de venda do mesmo curso. |
| Terreno x Biblioteca | não | 0 de 9 | 0% | 0% | Sem sobreposição literal. Mesmo tema: Biblioteca D00–D06 e F00–F06 são e-books e apresentações dos mesmos assuntos dos Pilares 1–7. Aparecem juntos nas mesmas 2 turmas. |
| Terreno x Panorama Marco Zero (Land Bank) | parcial | 0 de 2 | 0% (nomes mudam) | 4 de 12 = **33% do Panorama** (7% do Terreno) | Os 2 vídeos YouTube, o e-book Marco Zero e a aula interativa Marco Zero estão nos dois. |
| Terreno x Gestão | não | 0 | 0% | 0% | Sem sobreposição. |
| Bônus do Terreno (11 ferramentas) x 4 conteúdos Bônus Trilha (10 ferramentas) | não | n/a | 0% | 0% | Ferramentas diferentes, mesmo padrão "Bônus · Ferramentas Zion Collection Club". |
| Trilhas 2, 3 e 4 "Arquivo" x Gestão ativa | parcial | Gestão ativa tem 8 módulos, Arquivo 7 | 0 (Arquivo vazio) | 0 | Esqueleto antigo sem aulas; Gestão ativa o substituiu. |

Taxa de sobreposição geral: 1 curso ligado 3 vezes (58 aulas) e 4 aulas repetidas entre Terreno e Panorama.

## 5. Os números que Bruno citou

- **Zion Land Bank ~70 aulas:** a única turma do portal (Candidatos) tem 2 conteúdos: Panorama Marco Zero (12 aulas) + Terreno completo (58 aulas) = **70**. O Land Bank, portanto, inclui o curso do Terreno inteiro.
- **"Transforme seu terreno... ~50 aulas":** o curso tem 58 aulas: Marco Zero (7) + Pilares 1 a 7 (5+5+5+6+5+7+7 = 40) = **47**, mais **11 de bônus**. O "~50" são as 47 aulas do curso sem os bônus. A turma Terreno e a Fundadores mostram **94** porque também ligam a Biblioteca (+36).
- Os 94 e os 70 repetem as mesmas 58 aulas; somar as turmas conta o mesmo curso mais de uma vez.

## 6. Ofertas e produtos que entregam área de membros

Preço em R$. "Portal" é o que o produto mostra como destino.

| Produto | Oferta (status) | Preço | Portal | Turma(s) |
|---|---|---|---|---|
| Zion Collection 06 · Seu Airbnb Está Vazio? | **approved** | 47 | Zion Collection | Compradores · Seu Airbnb |
| ZC06 · Calendário comercial (complemento) | **approved** | 19 | Zion Collection | Compradores · Calendário |
| Trilha 1 · Desenvolvimento · Transforme seu terreno | incomplete (falta `externalId`) | 970 | Hospitality | Terreno |
| Inscrição no Club Zion Collection + Land Bank | incomplete (erro de gateway "Token inválido") | 270 | Land Bank | Candidatos |
| Club Zion Collection · Kit de Captação + sessão | pending_corrections | 97 | Hospitality | Kit de Captação |
| Zion Collection · Inscrição no clube (R$ 97) | archived | 97 | Land Bank | Candidatos |
| Mentoria Zion 360° · Trilha A · Desenvolvimento | archived | 15.900 | Hospitality | Arquivo · Turma A |
| Trilha 2 · Gestão | archived | 297 | Hospitality | Jornada 2 · Gestão |
| Trilha 3 · Operação | archived | 297 | Hospitality | Arquivo · Trilha 3 |
| Combo · As 3 trilhas | archived | 890 | Hospitality (3 entregas) | Terreno, Gestão, Operação |

- Entregam acesso hoje e podem vender: **só as 2 de Zion Collection** (aprovadas). Nenhuma das 10 ofertas com membership relacionadas ao Hospitality/Land Bank está aprovada e ativa.
- **Efeito:** o Combo e a Trilha 2 arquivados ainda apontam para turmas com alunos; as ofertas não vendem, mas o acesso existente continua.
- Total do workspace: 47 produtos; ofertas por status: 25 incomplete, 12 approved, 9 archived, 1 pending_corrections.
- Observação: Trilha 3 · Operação está ligada a uma turma e a um conteúdo "Arquivo" **sem nenhuma aula**.

## 7. Alunos por turma (contagem)

Hospitality: Terreno 3, Fundadores 1, Gestão 1, Kit Captação 1, Arquivo Turma A 1, Arquivo Operação 1, Arquivo Aula R$ 47 1, Arquivo Turma B 1, Arquivo Land Society 1, Arquivo Fundação 1 (portal: 12). Land Bank: Candidatos 7. Collection: 1 + 1 (portal: 2). Hospitality + Land Bank + Collection somam 21 matrículas por turma; o mesmo aluno pode contar mais de uma vez.

## 8. Qual conteúdo está mais completo para a Jornada do Desenvolvimento

**Terreno (`fa9a6c54`)** é o mais completo: 9 módulos (Marco Zero, Pilares 1–7, Bônus), 17 vídeos de ~5 a 7 min no YouTube, 8 "Faça agora" (diagnóstico e fichas por pilar), aulas interativas por pilar, 11 e-books em PDF e 11 ferramentas de bônus. Todas as 58 aulas têm descrição e estão habilitadas.

O que falta nele:
1. **Certificado**: desligado (só a Biblioteca tem).
2. **Duração** cadastrada em 8 de 17 vídeos; sem prévia grátis (`freePreview` 0).
3. **Produto sem venda**: a oferta Trilha 1 (R$ 970) está incompleta (falta `externalId`).
4. **Bônus de Desenvolvimento** ainda é só link externo; não há bônus de Branding/Vendas ligados a ele (esses 2 conteúdos estão sem turma).
5. Marco Zero repete o conteúdo do Panorama (Land Bank); não há versão única.
6. A Biblioteca (36 e-books) cobre D00–D06 e F00–F06, mas está sem vídeo e sem exercício.

## 9. PROPOSTA de reorganização para exatamente 3 portais (não executada)

PROPOSTA. Nada disso foi feito. Cada passo depende de "aprovado" do Bruno, porque mexe no que já existe.

**Portal 1 · Desenvolvimento**
- Fica: Terreno (58 aulas) como curso principal; Biblioteca D00–D06 como "material de apoio"; Bônus de ferramentas de Desenvolvimento.
- Unificar: Marco Zero do Panorama (Land Bank) e do Terreno em um só; uma turma só para o Terreno (hoje 3).
- Land Bank vira **turma ou módulo** deste portal: Candidatos entra com acesso a Terreno + Panorama.

**Portal 2 · Gestão**
- Fica: Jornada 2 · Gestão (32 aulas) + Bônus Gestão (3).
- Unificar: Bônus Branding e Vendas viram módulo de bônus aqui (hoje sem turma).
- Biblioteca F00–F06 (finanças) pode ficar aqui em vez de no Desenvolvimento.

**Portal 3 · Operação**
- Hoje vazio. Fica o esqueleto de "Trilha 3 · Operação" (7 módulos) e o Bônus Operação (2 ferramentas).
- É o único portal que ainda precisa de produção (aulas, vídeos, exercícios).
- Zion Collection (ZC06, calendário, Kit de Captação) vai para cá **ou** para Gestão; decisão do Bruno. Hoje as 2 ofertas aprovadas entregam no portal Zion Collection e não devem ser movidas sem teste de entrega.

**Vira arquivo (desabilitar, não apagar):** as 6 turmas "Arquivo" vazias do Hospitality, "Turma Fundadores" (mesmo curso do Terreno), os conteúdos Arquivo Trilha 2/3/4 (esqueletos vazios) e Aula gratuita de entrada (7 vídeos sem URL).

**Ordem de risco:** (1) desabilitar turmas vazias; (2) decidir onde ficam Land Bank e Zion Collection; (3) mover cursos para turmas novas só depois de religar as ofertas (`offers_add_membership_delivery`) e testar acesso com a compra real. Três portais é o limite; hoje já existem 3, então qualquer portal novo exige apagar ou renomear um dos atuais (renomear não muda ids de turmas nem de ofertas).

## Limites do levantamento
- URLs de YouTube, Gamma, Airtable, wa.me e clickmax.space não foram checadas (proxy bloqueou); 134 de 156 deram 200.
- A página de produtos mostra o portal de destino, não a turma; a turma vem da lista de turmas de cada portal.
- Contagem de alunos por turma pode repetir a mesma pessoa em turmas diferentes.
