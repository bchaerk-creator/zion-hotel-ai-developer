# Vistoria independente dos entregáveis · Mini Mentoria de Estruturação Zion

ZION AUDITOR · 25/11/2026 · somente leitura. Nada foi alterado no ClickMax, no Meta, nas mensagens nem no repositório de produção. Este arquivo é o único commit.
Método: leitura direta de `classrooms_details`, `lessons_get`, `portals_get`, `offers_get` (turma `087479a3…`, portal `3ef7a340…`, oferta `0c71eeba…`); `curl` pelo proxy em cada URL; `ffprobe`, `pdfinfo`, `openpyxl` e recálculo no LibreOffice; Playwright (390×844) com jsPDF servido do pacote npm. Marcações: [E] evidência, [NC] não conferível daqui.
Sem dados pessoais e sem números de vendas. As requisições de saída das fichas (POST) foram bloqueadas no teste; nenhum dado saiu.
Tabela completa dos 70 itens: `itens.csv` (fora do repositório, na pasta de trabalho da sessão).

## 1. Veredito em uma linha
O que existe é grande e abre quase tudo, mas o cartão anunciado tem **2 números que não fecham** ("10 fichas" são 8; "6 modelos" são 6 peças guiadas com só 2 arquivos-modelo) e **3 achados de coerência** que contradizem a oferta (vídeo de boas-vindas com Land Bank, botão "Enviar ao Land Bank" nas fichas e envio automático de dados ao clicar no PDF).

## 2. Resumo por módulo e tipo (70 itens, todos `enabled` = true)
| Módulo | Itens | Vídeo-aula (YouTube) | Tutorial mp4 | Boas-vindas mp4 | Aula interativa | Ficha Faça agora | E-book PDF | Aprofund. (e-book + 40 slides) | Planilha | Outros |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Onboarding | 3 | - | - | 1 | - | - | - | - | - | dossiê prévio, chat de suporte |
| 2 Marco Zero | 10 | 2 | 1 | - | 1 | 1 | 1 | - | - | guia PDF, mapa, kit de prompts, formulário Airtable |
| 3 Pilar 1 | 8 | 2 | 1 | - | 1 | 1 | 1 | 2 | - | - |
| 4 Pilar 2 | 8 | 2 | 1 | - | 1 | 1 | 1 | 2 | - | - |
| 5 Pilar 3 | 8 | 2 | 1 | - | 1 | 1 | 1 | 2 | - | - |
| 6 Pilar 4 | 9 | 3 (2 + 1 extra) | 1 | - | 1 | 1 | 1 | 2 | - | - |
| 7 Pilar 5 | 8 | 2 | 1 | - | 1 | 1 | 1 | 2 | - | - |
| 8 Pilar 6 | 8 | 2 | 1 | - | 1 | 1 | 1 | - | 2 | - |
| 9 Pilar 7 | 8 | 2 | 1 | - | 1 | 1 | 1 | - | - | Kit do Investidor, cadastro Airtable |
| **Total** | **70** | **17** | **8** | **1** | **8** | **8** | **8** | **10** | **2** | **9** |

Situação dos 70: ENTREGUE 49, PARCIAL 2, NÃO VERIFICÁVEL 19 (17 vídeos no YouTube e 2 formulários Airtable, hosts bloqueados pelo proxy). Nenhum QUEBRADO. Nenhum item vazio.

## 3. Evidência por tipo
- **Vídeos mp4 (9, GitHub Pages):** todos HTTP 200, `video/mp4`, h264+aac. Boas-vindas 1280×720, 516 s (8 min 36). Tutoriais: Marco Zero 103 s; Pilares 1 a 7: 216, 218, 219, 207, 218, 224, 233 s (total dos 8 tutoriais ≈ 27 min). Coerentes com os rótulos "2 min", "3 min", "4 min" dos anexos.
- **17 vídeo-aulas (youtu.be):** [NC] `youtu.be` e `www.youtube.com` retornam 403 do proxy. Não foi possível confirmar que existem, são públicos/não listados nem a duração. O ClickMax guarda `duration` 0 para eles (a plataforma não mostra duração).
- **E-books PDF (8):** 200, `application/pdf`, abrem no `pdfinfo`: Marco Zero 28 p., Pilar 1 55, Pilar 2 48, Pilar 3 67, Pilar 4 83, Pilar 5 75, Pilar 6 66, Pilar 7 62 (484 páginas). Guia "Comece aqui" 3 p.
- **Planilhas (2):** 200, xlsx. Orçamento de Abertura: 6 abas (Comece aqui, Premissas, Infraestrutura, FF&E, OS&E, Resumo), 479 fórmulas. Estudo de Massas e Viabilidade: 7 abas (Comece aqui, Massas, Investimento, Modelo de venda, Modelo de renda, Comparativo, Glossário), 172 fórmulas. Recálculo no LibreOffice: 0 erros nas duas. "Em branco" aqui quer dizer sem projeto e sem valores em R$: a planilha 1 traz lista de referência de itens com quantidades 1 a 3 e contingência 10%; a 2 só tem 365 dias/ano. As versões EXEMPLO existem no host (200) mas **não estão ligadas** a nenhuma lição.
- **Fichas Faça agora (8):** diagnóstico prévio (Marco Zero) e Pilares 1 a 7 (o 7 é o Dossiê). Todas carregam em 390×844, sem erro de JS, salvam no navegador (localStorage), calculam e geram PDF: diagnóstico 1 p.; Pilar 1 4 p.; P2 3 p.; P3 4 p.; P4 4 p.; P5 6 p.; P6 6 p.; Dossiê 14 p. Teste automatizado com respostas de teste ("dados fictícios").
- **Dossiê completo:** em sequência no mesmo navegador, o PDF final saiu com 14 páginas, capa, resumo, páginas 0 a 7 e decisão (avançar/ajustar/parar). Ressalva: reconheceu só 3 de 7 páginas como "prontas" e marcou as outras como "começada, sem página gerada / em branco"; a ficha do Pilar 5 não concluiu no meu robô (etapa de anexos). Não sei se é falha real ou limite do robô: **Bruno deve fazer um teste manual de ponta a ponta** (as 8 fichas em sequência no mesmo navegador, depois o Dossiê).
- **Kit de prompts:** 9 comandos (Página 0 a 7 + Fechamento "Dossiê completo"), botão Copiar. Confirmado.
- **Kit do Investidor:** uma página HTML (200) com 6 peças (teaser, one-pager, pitch de 12 slides, masterplan de viabilidade, plano conceitual, direcionamento de marca) + ficha de números, data room e roteiro de 4 semanas. Existem 2 arquivos-modelo no host: `Pitch-Deck-Zion-MODELO.pptx` e `Teaser-e-One-Pager-Zion-MODELO.docx` (200), **mas a lição tem `attachments: []` e a página não linka os arquivos**, enquanto a descrição promete "Na aba Materiais: o modelo do Pitch deck e o modelo Teaser + One-pager". Ou seja, o aluno não encontra os arquivos.
- **Aulas interativas (8), mapa de direcionamento, slides e e-books de aprofundamento (10), dossiê prévio:** todos 200. Não exercitei a fundo cada um.
- **Anexos das fichas:** as 8 lições Faça agora têm 4 anexos cada (tutorial mp4, e-book PDF, apresentação interativa, "Abrir o Faça agora"); URLs conferidas, 200. As lições de e-book, planilhas, Kit e Kit de prompts têm `attachments: []` (amostra lida: e-book P1, 2 planilhas, Kit, Kit de prompts, boas-vindas; as demais lições `document` não foram lidas uma a uma).
- **Oferta:** `status` approved, R$ 47 (`originalPrice` 4700), pix + cartão 1x, boleto off, `isRecurrent` false, `limitToRefund` 7, 1 entrega `internal_membership` (portal e turma corretos). Turma: `accessTime` 12 `month` (`defaultAccessDuration` 12). A oferta não tem campo `accessDays`; o prazo está na turma. Portal publicado (24/11), `firstAccessWithoutPass` true.

## 4. Frase por frase do carrossel
| Frase | Veredito | Evidência e ressalva | Redação segura |
|---|---|---|---|
| 9 módulos | CONFIRMADA | Onboarding, Marco Zero, Pilares 1 a 7 | "9 módulos" |
| 70 aulas e materiais | CONFIRMADA COM RESSALVA | 70 itens habilitados, mas incluem o chat de suporte, 2 formulários externos, 8 aulas interativas que reapresentam os mesmos vídeos e 10 itens de aprofundamento | "70 conteúdos entre vídeos, fichas, e-books, planilhas e kits" |
| 26 aulas gravadas em vídeo | CONFIRMADA COM RESSALVA | 26 itens `video`: 17 vídeo-aulas (16 numeradas + 1 extra, YouTube [NC]), 8 tutoriais de preenchimento, 1 boas-vindas. A boas-vindas contradiz a oferta (item 5) | "17 vídeo-aulas e 8 tutoriais em vídeo" (só depois de conferir o YouTube; o boas-vindas fica fora da conta até ser regravado) |
| 10 fichas interativas Faça agora | NÃO CONFIRMADA | São **8** (diagnóstico prévio + Pilares 1 a 7). Dá 9 contando o "Monte o seu dossiê inicial" (dossiê prévio) | "8 fichas interativas Faça agora" |
| 8 e-books, um por pilar (PDF) | CONFIRMADA COM RESSALVA | 8 PDFs abrem (Marco Zero + 7 pilares). "Um por pilar" fica impreciso: são 7 pilares + Marco Zero. Há ainda 5 e-books de aprofundamento em HTML | "8 e-books em PDF: Marco Zero e um por pilar" |
| 2 planilhas de cálculo em branco | CONFIRMADA | 2 xlsx abrem, com abas e fórmulas, 0 erros no recálculo. Ressalva menor: a planilha 1 traz lista de referência de itens; versão EXEMPLO prometida não está ligada | "2 planilhas de cálculo com fórmulas, para você preencher" |
| Kit do Investidor: 6 modelos | CONFIRMADA COM RESSALVA | São 6 peças com estrutura passo a passo; só 2 têm arquivo-modelo (pitch pptx, teaser + one-pager docx) e esses 2 **não estão anexados** | "Kit do Investidor: guia das 6 peças (teaser, one-pager, pitch, masterplan, plano conceitual e marca)" e acrescentar "e modelos de pitch e teaser" só depois de anexar os arquivos |
| 9 comandos de IA prontos | CONFIRMADA | Kit de prompts lista 9 comandos | "9 comandos de IA prontos (ChatGPT ou Claude, com a sua conta)" |
| Dossiê de Desenvolvimento em PDF | CONFIRMADA COM RESSALVA | A ficha do Pilar 7 gera PDF de 14 p. Reúne as páginas geradas no mesmo navegador/aparelho; páginas não geradas saem em branco; reconhecimento das 8 páginas não provado em teste manual | "monte o seu Dossiê de Desenvolvimento e baixe em PDF" |
| Telas reais: diagnóstico prévio e Pré-viabilidade | CONFIRMADA | As duas fichas existem com esses nomes e carregam | usar print da tela inicial e das perguntas; evitar a tela de resultado (tem botão Land Bank, item 5.2) |
| Cada ficha vira uma página do Dossiê | CONFIRMADA | PDFs de cada ficha vêm como "Página N do Dossiê" (0 a 7) | "cada ficha vira uma página do seu Dossiê" |
| 12 meses de acesso | CONFIRMADA | turma `accessTime` 12 mês | "acesso por 12 meses" |
| Garantia 7 dias | CONFIRMADA | `limitToRefund` 7 | "reembolso em até 7 dias" |

## 5. Conteúdo que contradiz a oferta (sem reunião, sem acompanhamento, Land Bank fora, investimento só como possibilidade)
1. **Vídeo de boas-vindas** `fcf20da1-0475-4a04-b9fd-11553eb74d6a` (módulo 1, `plataforma-v02.mp4`): quadros mostram "Zion Land Bank", "Seu terreno pode ser uma dessas oportunidades", "Possíveis parcerias e investimentos", "Diagnóstico e direcionamento… você agenda com a equipe Zion" e "banco de áreas". É a primeira coisa que o comprador assiste.
2. **Botão "Enviar ao Land Bank" nas 8 fichas** (`_landbank.js`; resultado da tela mostra o bloco "Banco de áreas da Zion" com caixa de autorização): lições `5cd29135-ae6f-48f7-8ed4-fae2f0ea3f8e`, `0481b040-5162-43a9-a4ff-d0ca35d33d07`, `d159ed5d-6340-49e0-9ffd-d4e400166ab6`, `1ca99475-f688-48b5-bf1e-9d44b09286f0`, `182d507a-b0b2-4e30-8c1e-1b4d3a03043a`, `9895ce66-e280-4201-87e3-aaad9495d4f2`, `b94b3b56-66ef-4ed0-a8b2-9cf86f05ef60`, `01ced15d-26f6-465c-ba1d-8921eef99d76`.
3. **Envio de dados ao baixar o PDF:** a tela inicial do diagnóstico diz "As respostas ficam só neste aparelho. Nada é enviado.", mas ao clicar "Baixar PDF" a ficha tentou POST para `zion-dossie-aulas.lovable.app` e `api.clickmax.io` (bloqueados no meu teste; conteúdo do envio não inspecionado). Mesmo sem marcar a caixa de autorização. Texto e comportamento divergem (LGPD).
4. **Anexos "para a equipe Zion montar o seu estudo com você"** (`_anexos.js`) nas fichas do Pilar 1 `0481b040…` e do Pilar 5 `9895ce66…`: promete trabalho da equipe, contrário a "sem acompanhamento individual".
5. **Dossiê prévio** `b12e98f3-07f0-4f23-ac28-02211d6dd992` (`/dossie/`): "O seu dossiê vai para a equipe Zion… a equipe Zion conhece o seu projeto"; contém "agendar" (2x; trecho exato não inspecionado). Descrição da lição: "envie as páginas do seu dossiê para a Zion".
6. **Descrições "enviar ao banco de áreas da Zion"**: `90ccd3db` (Comece aqui) e as 8 aulas interativas (`49320a7a`, `1bdba655`, `1cdb4a5c`, `d5255480`, `9325cb47`, `cb87b90f`, `8df647ec`, `423f4a95`); `b625a0e6` (mapa: "…até o cadastro no banco de áreas da Zion"); lição `6a3d7c71` (cadastro, Airtable) e `e9274de1` ("Use o mesmo e-mail da inscrição… análise pela equipe Zion").
7. **E-books PDF** citam o Land Bank Zion: Marco Zero `6063c501`, Pilar 1 `475d900d`, Pilar 2 `09e8eac4`, Pilar 3 `da5c67ec`, Pilar 4 `09ea86f8`, Pilar 5 `8abb60e2`, Pilar 6 `e620975e`, Pilar 7 `d2cc48fd` (6 menções, incluindo "A reunião e a lista do Land Bank Zion são caminhos possíveis, não promessas" e uma questão de quiz sobre estar na lista). Todos com "a Zion avalia cada caso", mas Land Bank e reunião aparecem.
8. **Vídeo 16** `73b47479…` (descrição): "…ou conversar com a Zion. A Zion avalia cada caso."
9. **Tutorial do Pilar 7** (mp4, `f3cdce4a…`/anexo da ficha): cartão final "o cadastro no Zion Land Members".
10. **E-books de aprofundamento** (`escola/d01..d05`) remetem ao "D06 · Estruturação Jurídica, Societária e Land Bank", unidade que não faz parte do produto.
11. **"R$ 97":** nome da turma `087479a3-9d6f-4e1f-a542-c47b347bf5ed` = "Plataforma de estruturação (R$ 97)" [NC se o aluno vê esse nome]. As ocorrências de "R$ 97" nos e-books de aprofundamento são só exemplos numéricos (R$ 97.200), não o preço. "R$ 270": nenhuma ocorrência.
12. **"Simulador" e "mentor de IA"** são citados nas descrições Faça agora (`0481b040`, `d159ed5d`, `182d507a`, `9895ce66`, `b94b3b56`) e há botão "Pedir a leitura do mentor virtual" nas fichas; não exercitei (chamada externa bloqueada). Não anunciar.
13. **Promessas de Materiais que não existem como anexo:** Kit do Investidor `78a3f24f-0392-4d48-94e8-6cae4b51c72b` (pptx e docx), Planilha 1 `d3ae8d55-c339-4241-aa70-ec1dc4252894` e Planilha 2 `05c0bdc1-7d00-48f8-a8d3-58b6bb973576` (versão EXEMPLO): `attachments: []`.

## 6. Terminologia: como o aluno vê e o que chamar
- A plataforma rotula a lista de "**Aulas**" e a segunda aba de "**Materiais**", com os botões "Próxima aula", "Concluir aula", "Aula concluída" e "Assistida" para os 70 itens, inclusive e-book e planilha. Cada módulo se chama "Comece aqui · Onboarding", "Marco Zero · …" e "Pilar N · …". Os itens usam prefixos nos títulos: "Vídeo N", "Faça agora", "E-book", "Tutorial em vídeo", "Aula interativa", "Aprofundamento", "Planilha", "Kit". Ícones por tipo (vídeo, documento, link externo): deduzido do `type`, não visto na tela [NC].
- Só 26 dos 70 são vídeo (17 vídeo-aulas de conteúdo). "70 aulas" seria enganoso; "70 aulas e materiais" é defensável por causa do rótulo da plataforma, mas "aulas" faz o comprador esperar vídeo.
- **Recomendação:** "**conteúdos**" para o total (neutro e exato), "**vídeo-aulas**" só para os 17 vídeos, "**fichas**" para as 8 interativas, "**e-books**", "**planilhas**", "**kits**". Evitar "lições" (termo escolar que o aluno não vê) e "aulas" sem qualificar.

## 7. O que existe e não está anunciado (diferenciais reais citáveis)
- 8 **aulas interativas** (vídeos + exercícios + gera a página do Dossiê em PDF).
- 5 **e-books de aprofundamento** (8 capítulos, com ferramenta e exercícios) e 5 **aulas de 40 slides** (cerca de 60 min cada), Pilares 1 a 5.
- 8 **tutoriais em vídeo** de preenchimento (≈ 27 min).
- **Mapa de direcionamento** (10 etapas, tarefas marcáveis) e guia "Comece aqui".
- Kit do Investidor com **data room** e **roteiro de 4 semanas**; ficha de números que alimenta os comandos de IA.
- **Primeiro acesso sem criar senha** (`firstAccessWithoutPass`).
- Tudo salva no aparelho (sem cadastro na ficha) — mas ver item 5.3 antes de citar privacidade.

## 8. Anunciado, mas não existe (ou não como dito)
- "10 fichas" (existem 8).
- "6 modelos" do Kit como arquivos (existem 2 arquivos-modelo e eles não estão anexados).
- "26 aulas gravadas" como se todas fossem aula (são 17 + 8 tutoriais + 1 boas-vindas).
- "Um e-book por pilar" literal (8 e-books para 7 pilares + Marco Zero).
- Prometido nas lições e ausente: pitch pptx, teaser/one-pager docx e versões EXEMPLO na aba Materiais.
- Não verificável daqui: "e-mail com o acesso" (já [NC] no documento anterior).

## 9. Texto recomendado para o cartão "O que você recebe"
> **O que você recebe**
> 9 módulos · 70 conteúdos
> 8 fichas interativas "Faça agora" · cada ficha vira uma página do seu Dossiê
> 17 vídeo-aulas + 8 tutoriais em vídeo
> 8 e-books em PDF (Marco Zero e um por pilar)
> 2 planilhas de cálculo com fórmulas, para você preencher
> Kit do Investidor: guia das 6 peças (teaser, one-pager, pitch, masterplan, plano conceitual e marca)
> 9 comandos de IA prontos (ChatGPT ou Claude)
> Dossiê de Desenvolvimento para baixar em PDF
> 12 meses de acesso · reembolso em até 7 dias
> Material educativo. Sem reunião e sem acompanhamento individual.

Condições para publicar o cartão: (a) conferir os 17 vídeos no YouTube, (b) tirar ou regravar o boas-vindas, (c) teste manual do Dossiê. Se (a) não for feita, trocar por "vídeo-aulas e tutoriais em vídeo" sem número.

## 10. O que corrigir (não corrigido por esta vistoria; tudo exige "aprovado" de Bruno)
1. Regravar ou ocultar o vídeo de boas-vindas `fcf20da1…` (Land Bank, parcerias/investimentos, agenda com a equipe).
2. Decidir sobre o botão "Enviar ao Land Bank" e o envio automático ao baixar PDF nas 8 fichas (`_landbank.js`, `enviarParaZion`); corrigir o texto "Nada é enviado" ou o comportamento. Mexe em arquivos do site, fora desta vistoria.
3. Remover/ajustar "equipe Zion montar o seu estudo com você" (`_anexos.js`), "o dossiê vai para a equipe Zion" (`/dossie/`) e "reunião/Land Bank" no e-book do Pilar 7 e nos demais.
4. Anexar à lição do Kit do Investidor o `.pptx` e o `.docx`, e às planilhas as versões EXEMPLO (ou trocar o texto "na aba Materiais" das descrições).
5. Renomear a turma "(R$ 97)" e conferir se o aluno vê o nome.
6. Confirmar no YouTube os 17 vídeos (existem, públicos/não listados, duração) e preencher `duration`.
7. Teste manual do Dossiê consolidado (8 fichas em sequência, mesmo navegador) e abrir as lições `document`/xlsx pela visão do aluno para ver como a plataforma exibe PDF e planilha.
8. Ajustar descrições que citam "simulador" e "mentor de IA" ou comprovar que funcionam.
9. Abrir o chat de suporte e os dois formulários Airtable como aluno (não conferidos).

## 11. Limites desta vistoria
Não vi a área de membros pela tela do aluno (só dados e URLs). YouTube e Airtable bloqueados. Fichas testadas com respostas fictícias e saída de rede bloqueada. A ficha do Pilar 5 não gerou PDF na rodada encadeada (gerou na rodada isolada, 6 p.). Aulas interativas, slides e e-books de aprofundamento: só carregamento e busca de termos, não leitura integral.
