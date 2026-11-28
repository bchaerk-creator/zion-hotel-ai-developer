# Auditoria somente leitura · Dossiê e landing da Zion Collection (R$ 47)

Data: 28/11/2026. Método: leitura de código e arquivos do repositório. Nada foi alterado, publicado, testado em navegador nem enviado. Onde não achei prova, está escrito "não comprovado".

## 0. Leitura rápida: qual é "o dossiê"?

Não existe um único dossiê. O repositório tem três coisas com esse nome. Esta auditoria trata das três e diz qual é qual:

| Sigla | O que é | Arquivo | Gera PDF? |
|---|---|---|---|
| **D1** | **Dossiê de Desenvolvimento** (Pilar 7): junta a página 0 (Marco Zero) e as páginas 1 a 6 salvas nas fichas e acrescenta a página 7 (capital e decisão). É o PDF da plataforma da Trilha 1 / Plataforma de estruturação. | `docs/trilha1/pilar7/index.html` (lê as outras fichas pelo `localStorage`) | Sim, jsPDF 2.5.1 (cdnjs) |
| **D1b** | **Dossiê do Produto** (Aula 6, versão mais antiga, 6 páginas) | `docs/trilha1/aula6/index.html` | Sim, jsPDF |
| **D2** | **Dossiê prévio** do Land Bank (≈ 45 perguntas, uma por tela, com envio de arquivos ao servidor) | `docs/dossie/index.html` | **Não gera PDF** |
| **D3** | **Gerador de Dossiê** do Produto 01 Terra/Capital (produto separado) | `producao/produto-01-terra-capital/src/app.html` (publicado em `docs/p/adbc67069af26ae0/terra-capital/`) | Sim, jsPDF |

Conclusão curta: o PDF que a landing vende como "relatório" é o D1. O D2 é o que realmente manda dados e arquivos para a equipe, mas não faz PDF. O D1 não envia nada.

---

## 1. Tabela de recursos

| Recurso | O que é | Onde está (arquivo) | Funciona (comprovado?) | Pendência |
|---|---|---|---|---|
| Fichas "Faça agora" (Marco Zero, Pilares 1 a 6) | 7 ferramentas, uma pergunta por tela, salvam no aparelho | `docs/trilha1/marco-zero`, `aula1..3`, `pilar4..6` | Teste Playwright de 25/11 (8 fichas): "DEPOIS: APROVADO (0 falhas)", 0 envio indevido, sem erro de JS. Fonte: `zion-sales-engine/15-correcoes-produto/testes/RESULTADO_ANTES_DEPOIS.txt`. Não rodei de novo hoje. | O teste serviu o jsPDF do npm; o PDF com o jsPDF do cdnjs no navegador do aluno não foi provado aqui. |
| Dossiê de Desenvolvimento (D1) | PDF A4 com capa, sumário, páginas 0 a 7, alertas, 3 caminhos, 90 dias, fecho | `docs/trilha1/pilar7/index.html` (função `gerarDossiePDF`, linhas ~1430 a 1495) | Está no teste acima (ficha `pilar7`). Conteúdo do PDF não foi aberto por mim. | Depende do `localStorage` do mesmo aparelho e navegador; sem foto, sem logo. |
| Dossiê do Produto (D1b) | Versão antiga de 6 páginas | `docs/trilha1/aula6/index.html` | Entrou no mesmo teste? A lista do teste cobre marco-zero, aula1, aula2, aula3, pilar4..7. **aula4..6 não estão na lista: não comprovado.** | Duplica a promessa do D1. |
| Dossiê prévio (D2) | Perguntas + upload (matrícula, fotos, localização, planta) + consentimento + envio | `docs/dossie/index.html` | Código lido. Envio ao endpoint **não testado** (a inspeção de 27/11 também não chamou). | Aceita só `.pdf,.jpg,.jpeg,.png`. Não aceita vídeo. Não gera PDF. |
| Hub de progresso das ferramentas | Lista com "Não começada / Em andamento / Feita" lendo o `localStorage` | `docs/trilha1/index.html` | Código lido. Lista só `aula1..aula6` (as ferramentas antigas), não o Marco Zero nem o Pilar 7. | Não é "Meu Projeto Hoteleiro". Não comprovado se está ligado a alguma aula no ClickMax. |
| Tela Terra/Capital "Dossiê" (D3) | Campos de texto + cálculos + PDF | `producao/produto-01-terra-capital/src/app.html` | `RELATORIO.md`: 60 testes, e-book 60 páginas. Não rodei. | É outro produto (R$ 47 × R$ 67, rascunho). |
| Landing | Página estática de 10 blocos | `docs/p/adbc67069af26ae0/landing-zc47/pagina.html` (28.626 bytes) | Código lido. Script de UTM testado em 27/11 (Playwright), em `producao/zion-collection/club-97/zc47-frio/RASTREAMENTO_AUDITORIA.md`. | Ver seção 4. |
| Cópias da landing | `index.html` (prévia, 27.961 bytes) e `checkout.html` (prévia do checkout) | mesma pasta | Não comparei linha a linha. A `pagina.html` é a que o relatório de rastreamento cita como a servida em `/inscricao`. | Não comprovei que a `index.html` é igual à `pagina.html`. |
| Servir `/inscricao` pelo Lovable | Projeto Lovable que busca a página no GitHub Pages | Fora do repositório (citado em `RASTREAMENTO_AUDITORIA.md`: "busca a cada 30 s", `paginaEstatica.server.ts`) | **Não comprovado por mim.** Domínio bloqueado aqui; só a documentação diz isso. | Confirmar ao vivo. |

---

## 2. Auditoria do dossiê (tarefa 1)

### 2.1 D1 · Dossiê de Desenvolvimento (PDF da plataforma)

**Como é gerado.** `gerarDossiePDF(L)` em `docs/trilha1/pilar7/index.html`. Usa `jspdf` (`<script src=".../jspdf/2.5.1/jspdf.umd.min.js" defer>`), fontes **internas do jsPDF** (Helvetica e Times) e A4. O nome do arquivo é `Dossie-de-Desenvolvimento-<nome-do-aluno>.pdf`.

**Tudo que o PDF contém hoje (na ordem):**
1. **Capa:** "MÉTODO ZION · O DOSSIÊ COMPLETO", "Dossiê de Desenvolvimento", frase com a decisão e "N de 7 páginas prontas neste aparelho", nome do curso, **ALUNO (nome)**, "Terreno em cidade/UF", "Gerada em data" e o aviso legal. Se a página 7 foi ajustada no simulador, entra uma tarja "PÁGINA 7 AJUSTADA NO SIMULADOR".
2. **Sumário "O que está nesta pasta":** tabela Página, Nome, Situação, Veredito; caixas "Os vereditos" e "Como ler".
3. **Página 0 · Marco Zero (Diagnóstico prévio):** 4 números, "Onde você começou" (motivo e dor), "O ponto mais frágil", "A primeira ação de 7 dias".
4. **Páginas 1 a 6** (uma por ficha: Território, Mercado, Produto, Modelo de Negócio, Masterplan, Pré-viabilidade). Cada uma traz: até 4 números, "O veredito" (Avançar, Testar, Ajustar ou Pausar), "O ponto mais frágil", "O critério para parar", "O Compromisso de 7 dias" (ação, responsável, prazo, evidência), as tabelas da ficha, "Leitura do mentor virtual" (se o aluno pediu) e "As quatro perguntas" (completa? veredito? o que faria parar? maior lacuna?). Página não feita aparece como "A fazer".
5. **Página 7 · Capital e decisão:** números, "Ajustado no simulador" (se houver), "A decisão" (Avançar, Ajustar ou Parar), "O que as páginas sugerem", "A frase do Dossiê", "O ponto mais frágil", "As três perguntas do capital", "O pedido, linha por linha" (investimento da fase um, giro, terreno a pagar, custo de buscar dinheiro, recursos próprios, pedido, limite de perda), "As seis fontes" (próprio, banco, investidor, sócio, pré-venda, parceria com quem opera, mais garantia e aval), "Dinheiro ou sócio", "As sete páginas, lado a lado", "O caminho e os 90 dias", "O Compromisso de 7 dias", "Os alertas", "As contas e as leituras" e "Leitura do mentor virtual".
6. **Fecho "O caminho Zion":** três caminhos (sozinho, banco/investidor, conversar com a Zion), Sessão de diagnóstico estratégico "sujeita à análise e à agenda", exemplo da Marina como ilustração e aviso de que tudo é conta de referência.

**Campos abertos (texto livre).** Nas fichas há perguntas de texto (`tipo: "texto"`), por exemplo: público principal, público de domingo a quinta, quem fica de fora, momento assinatura, frase em três partes, provas da promessa (aula3); zonas "onde nunca construir" (pilar5); "ponto mais frágil", "critério para parar" e campos do Compromisso de 7 dias em todas. Na página 7: frase do Dossiê e plano de 90 dias (dias 1 a 30, 31 a 60, 61 a 90). Perfil: nome, e-mail, cidade, UF (campos de texto).

**Upload de foto ou documento.** **Não existe no D1 nem em nenhuma ficha atual.** Busca por `type="file"` e `FileReader` em `docs/trilha1/*/index.html`: zero. Busca por `addImage` (imagem dentro do PDF): zero. O PDF **não leva foto, nem logo, nem mapa**. O arquivo `docs/trilha1/_anexos.js` (carregado só nas fichas dos Pilares 1 e 5) diz no cabeçalho que "NÃO envia nada: sem fetch, sem upload, sem formulário" e só mostra texto sobre a Sessão de diagnóstico. Antes da correção de 25/11 havia upload (o teste ANTES registra `upload 1` na aula1).

**Salvamento local.** Sim. Chaves `zion-t1-marco-zero`, `zion-t1-aula1..3`, `zion-t1-pilar4..7` no `localStorage`, com `try/catch`. O D1 lê essas chaves. Efeito prático: se o aluno trocar de aparelho ou navegador, as páginas somem do Dossiê (o PDF mostra "A fazer"). O próprio texto das fichas avisa: "As respostas ficam salvas só neste aparelho". Não vi backup/restauração em JSON no D1 (o D3 tem).

**Download.** Sim, `doc.save(arq)`. Não achei botão de imprimir no D1 (o D3 tem).

**Compartilhamento ou envio à equipe Zion.**
- **D1 não envia.** `ZION_WEBHOOK_URL = ""`, `enviarParaZion()` devolve `{enviado:false, local:true}`, e `_reuniao.js` termina com: "Esta ferramenta não envia as suas respostas nem arquivos para a Zion: guarde o PDF do seu Dossiê."
- Único envio possível no D1: o botão "mentor virtual" (`pedirMentor`) faz POST das respostas e dos cálculos (inclui nome e e-mail) para `https://zion-dossie-aulas.lovable.app/api/feedback`, **só se o aluno tocar no botão**. Não testei o endpoint.
- Não há `navigator.share`, `mailto:` nem link de WhatsApp no D1 (busca feita). Só o Marco Zero tem um link `wa.me/554861371061`.
- **D2 envia:** `POST` multipart para `https://www.zionhotelgroup.com/api/public/dossie-landbank` com `resolved` (respostas e status), `answers`, perguntas e os arquivos. Exige caixa de consentimento marcada. Texto do consentimento: "A Zion avalia cada caso e não garante investidor, financiamento nem aprovação."
- `docs/trilha1/territorio/index.html` ("Leitor de Território") tem dois `fetch`: `https://www.zionhotelgroup.com/api/public/territorio` e `https://zion-dossie-aulas.lovable.app/api/dossie`. Não analisei o que envia nem se está ligado à plataforma de R$ 47.

**Identidade visual.**
- **D1 e todas as fichas:** cores `#16261C` (verde), `#F5F1E8` (creme), `#E0BE5E` (dourado), `#7A5E12`; fontes da página **Playfair Display e Inter** (Google Fonts); no PDF, **Helvetica e Times** do jsPDF. **Não segue** a paleta e as fontes oficiais do `CLAUDE.md` (`#040605`, `#1B2117`, `#FEF5F0`, `#DED6BF`, `#8B714E`, `#C9B37E`; Cormorant e Aventa). Sem logo oficial no PDF.
- **D2:** fundo `#0f1a12`, dourado `#c9a96a`, Georgia e Arial. Também fora da paleta oficial.
- **D3:** usa a paleta oficial e embute Cormorant e Aventa (`@font-face` com base64). O PDF dele também usa Helvetica (jsPDF).
- **Landing:** Cormorant Garamond e Inter, verde `#19291F`/`#20352A`, dourado `#D5BE91`, creme `#F4EFE5`. Usa o logo oficial `zion-logo-claro.png`, mas a paleta e a fonte de texto (Inter) também não são as do `CLAUDE.md` (que pede Jost no ClickMax).

### 2.2 D2 · Dossiê prévio do Land Bank (`docs/dossie/index.html`)

- **Blocos:** 1 Você e o projeto, 2 A sua área, 3 Documentos, 4 Mercado, 5 Produto e investimento, 6 Valor da terra, 7 Fechamento, 8 Operação atual (só para quem opera).
- **Perguntas:** identificação (nome, e-mail, WhatsApp com DDD); papel; objetivo; cidade e estado (texto); tamanho; urbana/rural; acesso; distância; infraestrutura existente; restrições; situação jurídica; ônus; cadastros; zoneamento; topografia; **envio de 4 tipos de arquivo** (matrícula, fotos da área com `multiple`, print de localização, planta/levantamento); demanda; concorrência; público; produto imaginado; unidades; investimento estimado; capital; prazo; valor da terra (texto livre numérico); base do valor; estrutura existente; interesse em parceria (terra + infraestrutura × cabanas da Zion); aporte da terra; 7 perguntas de operação (tempo, unidades, ocupação, canais, diária, nota, equipe); dores; resultado em 12 meses; o que já tentou; trava; quando decide; quem decide; como prefere avançar; o que faria decidir agora; dúvida (texto longo); consentimento.
- **Resultado na tela:** "O seu raio-x" (Área, Documentos, Mercado, Produto e capital, Valor da terra, cada um "Em ordem", "Atenção" ou "Crítico") e até 5 correções. **Não gera PDF.**
- **Salvamento local:** `localStorage` chave `zlb_dossie_v1`. Os **arquivos não são salvos** localmente (ficam só na memória da página até o envio).
- **Envio:** sim, ao endpoint acima. Mensagem de erro avisa que as respostas ficam no aparelho.
- **Observação sobre dados:** pede WhatsApp e e-mail e envia arquivos como matrícula (documento com dados pessoais). Pela regra "não colete dados desnecessários", vale decidir se a matrícula inteira é necessária. Não coleta CPF diretamente.

### 2.3 D3 · Terra/Capital (para referência de molde)

Tem salvamento, backup `.json`, impressão e PDF, com campos: nome do projeto, cidade e UF "sem endereço", projeto e público, escopo piloto, comparáveis, alternativas de capital, riscos e pendências, pedido e destinação, decisão. Serve de molde para campos livres e para backup. Não tem upload.

---

## 3. Comparação com as 20 seções propostas (tarefa 2)

Legenda: **Existe** = já cobre; **Parcial** = cobre em parte, com o que falta; **Não existe**. "Onde" aponta para D1 (PDF da plataforma) e, quando útil, D2.

| # | Seção proposta | Situação | Onde e o que falta |
|---|---|---|---|
| 1 | Capa personalizada | **Parcial** | D1: capa com nome, "Terreno em cidade/UF", data, aviso legal. **Falta:** nome do projeto, logo oficial, foto, versão/código do documento. |
| 2 | Identificação do empreendedor | **Parcial** | D1: nome, e-mail, cidade/UF (perfil; no PDF só nome e cidade). D2: nome, e-mail, WhatsApp, papel (dono, herança, investidor, opera). **Falta:** papel e contato no PDF, forma de decisão (sozinho ou com sócio: existe em D2, não em D1). |
| 3 | Apresentação da oportunidade | **Parcial** | D1: página 0 (motivo, dor) e "A frase do Dossiê". **Falta:** um texto de apresentação em 1 parágrafo, montado dos dados. |
| 4 | História e visão do projeto | **Parcial** | D1: Marco Zero (visão), aula3 (momento assinatura, frase em três partes). D2: "maior dúvida" (texto livre). **Falta:** campo de história (por que o terreno, de quem é, quanto tempo) e de visão em 3 a 5 anos. |
| 5 | Características do terreno | **Existe** | D1 página 1 (aula1): área da matrícula, preservação, reserva legal, encosta, recuos, serviço, valor, limites físico/infra/experiência, documentos. D2 bloco 2 e 3 (tamanho, urbana/rural, infra, restrições, situação jurídica, ônus, cadastros, zoneamento, topografia). |
| 6 | Fotografias da propriedade | **Não existe no PDF** | Nenhum `addImage`, nenhum `FileReader`. D2 aceita foto (JPG/PNG) e envia ao servidor, mas a foto não entra em PDF nenhum. A tela de mockup da landing mostra upload de fotos e vídeos que o código atual **não tem** (ver seção 4). |
| 7 | Localização e acessibilidade | **Parcial** | D1: cidade/UF. D2: acesso (asfalto, terra boa, terra difícil) e distância (até 15 min, 15 a 45, mais de 45). **Falta no PDF:** acesso e distância; coordenadas ou link de mapa (D2 pede só um print de mapa, como arquivo). |
| 8 | Atributos naturais | **Parcial** | Só o lado das restrições: preservação, reserva legal, encosta, nascente/mata (D2). **Falta:** atrativos naturais positivos (vista, água, mata, clima) e fotos. Não achei campo para isso. |
| 9 | Atributos turísticos | **Parcial (fraco)** | D2: "há atrativos, mas pouca hospedagem" como uma opção de demanda. **Falta:** lista de atrativos próximos, distâncias, sazonalidade qualitativa. Não achei campo próprio. |
| 10 | Características do destino | **Parcial** | D1 página 2 (aula2): ocupação de fim de semana e de semana, diárias, amplitude de preço, meses de alta e fracos, crescimento da procura, unidades em obra. São números autodeclarados. **Falta:** descrição qualitativa do destino (perfil do turista, infraestrutura da cidade). |
| 11 | Informações de mercado | **Existe** | D1 página 2 e D2 bloco 4 (demanda, concorrência, público). Observação: as fichas pedem "fonte" nos números, o que ajuda a distinguir dado de palpite. |
| 12 | Visão do empreendimento idealizado | **Existe** | D1 páginas 3 e 5: tipologia, unidades, área, masterplan faseado, fase um e projeto completo. |
| 13 | Modelo de hospedagem pretendido | **Existe** | D1 página 4: alugar, hospedar ou vender; degrau do produto; quem opera; modelo de venda. D2: produto imaginado. |
| 14 | Experiência que deseja oferecer | **Parcial** | D1 página 3: momento assinatura (horário e quem prepara), frase em três partes, provas da promessa. **Falta:** campo livre "experiência do hóspede do chegar ao partir". |
| 15 | Diferenciais percebidos | **Parcial** | D1 página 3: "provas da promessa", teste do vizinho, teste dos cinco segundos. **Falta:** campo explícito "diferenciais" e a distinção entre diferencial percebido e diferencial provado. |
| 16 | Perspectivas de investimento declaradas | **Existe** | D1 páginas 6 e 7: investimento da fase um, giro, reserva, pedido linha por linha, limite de perda, recursos próprios, terreno a pagar. D2: faixa de investimento, capital, valor da terra e a base do valor. Já saem como "declarado pelo aluno" e "conta de referência". |
| 17 | Necessidades de parceria | **Parcial** | D1 página 7: "Dinheiro ou sócio" (dinheiro, mão, conhecimento, mercado, gestão, expansão) e "As seis fontes". D2: interesse em parceria com terra e infraestrutura. **Falta:** campo livre de "que tipo de parceiro eu procuro" separado de "quero que a Zion invista". |
| 18 | Informações ainda desconhecidas | **Existe (ponto forte)** | D1: "Não sei" é resposta válida e vira alerta; "Em branco", "A fazer", "maior lacuna", "ponto mais frágil", "quantos Não sei". D2: conta de pontos "sem resposta ou crítico". |
| 19 | Direcionamento preliminar | **Existe** | D1: veredito por página (Avançar, Testar, Ajustar, Pausar), "O que as páginas sugerem", decisão final (Avançar, Ajustar, Parar), "a página mais fraca". D2: raio-x e correções. |
| 20 | Próximos passos | **Existe** | D1: Compromisso de 7 dias, plano de 90 dias, "O caminho Zion". |

**Resumo da comparação:** 7 existem, 12 existem parcialmente, 1 não existe (fotografias). O que mais pesa: **foto no PDF**, **atrativos naturais e turísticos**, **história e visão em texto** e **capa com nome do projeto, logo e foto**.

### 3.1 Separa "declarado", "orientação da plataforma" e "verificado"?

- **Não separa nos três rótulos.** Não achei o estado "verificado" em nenhum dos dossiês (a palavra aparece uma vez em `aula1`, na opção de resposta "Seguir: está tudo verificado e a conta cabe", que é uma autoavaliação do aluno, não um status de dado).
- **O que existe de separação parcial:**
  - "Declarado" aparece só como "Não sei declarado" e "linha em branco declarada" (D1), nunca como etiqueta de dado do empreendedor.
  - "Orientação da plataforma" aparece como blocos visualmente distintos: "Por que perguntamos" (D2), "O que as páginas sugerem" e "Apoio automático" (D1 e D3), "Leitura do mentor virtual" (D1, vem do servidor Lovable). Eles estão rotulados, mas a separação é por título de caixa, não por regra do documento.
  - O aviso "Toda conta é de referência e é ilustrativa" e "A Marina... exemplo ilustrativo" separa exemplo de dado real.
- **Recomendação de estrutura (não implementada):** três rótulos fixos em todo campo do PDF: "Declarado pelo empreendedor", "Orientação da plataforma" e "Verificado" (hoje o terceiro estaria sempre vazio, e isso deve ser dito no documento).

### 3.2 Há texto que prometa investimento ou parceria? (proibido)

Não achei promessa direta nos dossiês. Achei **linguagem de risco** que depende do asterisco:

| Onde | Texto | Avaliação |
|---|---|---|
| `docs/trilha1/_anexos.js` e `_reuniao.js` | "É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*" com nota "Parceria e investimento não são garantidos" | Tem ressalva. "Oportunidade de buscar" é aceitável, mas o título "Depois do Dossiê: solicite a Sessão..." já liga dossiê a sessão. Risco **baixo a médio**. |
| `docs/dossie/index.html`, pergunta `aporte` | "Terras bem documentadas podem entrar como ativo em estruturas de projeto com a Zion. Cada caso é avaliado, sem garantia de aprovação." | Sugere que a Zion pode receber a terra como ativo. Tem ressalva. Risco **médio**: não prometer, mas também não insinuar. |
| `docs/dossie/index.html`, pergunta `parceria_infra` | "É um modelo possível para quem já tem estrutura... Cada caso é avaliado, sem garantia" | Mesma avaliação. |
| `docs/dossie/index.html`, `infra_exist` | "a Zion pode entrar com os produtos, como as cabanas, e você com o terreno e a estrutura" | **Mais forte:** descreve um modelo de parceria sem ressalva na própria frase (a ressalva está na pergunta seguinte). Risco **médio a alto**. |
| D1 (PDF) | "Não é oferta de investimento... não promete renda, retorno, crédito, investidor, sócio ou parceria" no rodapé de toda página | Conforme. |
| D1, fecho | "parceria e investimento não são garantidos" | Conforme. |

---

## 4. Auditoria da landing `pagina.html` (tarefa 3)

### 4.1 Seções atuais (na ordem do arquivo)

| # | Comentário no código | Conteúdo |
|---|---|---|
| 1 | HERO | Foto `store/hero.webp`, logo, kicker "Zion Collection / Novos destinos", H1, subtítulo, lead, CTA, nota com asterisco, link "Entenda como funciona" |
| 2 | VIDEO INSTITUCIONAL | "Você tem o terreno. Nós temos a experiência." + vídeo `assets/video/expansao-zion.mp4` (15,9 MB) |
| 3 | NARRATIVA | "Todo grande empreendimento começa com uma visão." + comparação de 2 fotos (op09 e op08) + frase "Não nos apresente apenas um terreno. Apresente sua visão." |
| 4 | PLATAFORMA + VÍDEO DEMONSTRATIVO | Texto da plataforma, mockup de notebook (`tela-painel.jpg`) e celular (`tela-ficha.jpg`), vídeo `plataforma-v02.mp4` (20 MB) |
| 5 | COMO FUNCIONA (`#como-funciona`) | "Queremos te conhecer.", lista de 4 itens e 6 etapas com imagem `etapa-1..6.jpg` |
| 5b | RESULTADO DO PROCESSO | "Ao final, você tem a apresentação ideal do seu projeto." em 4 passos |
| 6 | OFERTA + CHECKOUT | Cartão com R$ 47, botão e 4 condições |
| 7 | AUTORIDADE | Foto e texto de Bruno Chaerk (Founder & CEO) |
| 8 | MÉTODO ZION 360° | Desenvolvimento, Gestão, Operação; "Fase de Desenvolvimento é a disponível hoje" |
| 9 | OFERTA FINAL | Fundo `store/noturna.webp`, "Seu terreno pode ser o próximo destino Zion.", lista, R$ 47, botão |
| 10 | PERGUNTAS | 5 perguntas frequentes |
| — | Rodapé | Logo, aviso "Material educativo", suporte WhatsApp +55 48 6137-1061 |

### 4.2 Itens pedidos

- **Headline (H1):** "Seja um parceiro Zion e inscreva seu terreno ou projeto, de forma estruturada, pela nossa plataforma.*" (asterisco: "Parceria e investimento sujeitos à análise técnica e comercial. Não são garantidos.")
- **Subtítulo:** "Transforme seu terreno em um destino turístico."
- **Lead:** "Inscreva-se na plataforma e aprenda o passo a passo para começar a criar um projeto."
- **CTA do topo:** "Quero fazer parte da Zion e inscrever meu terreno ou projeto" (rola para `#como-funciona`, **não compra**). CTAs de compra: "Quero iniciar minha jornada na Zion" (seções 6 e 9).
- **Preço exibido:** "R$ 47", "Pagamento único" (bloco 6) e "R$ 47, pagamento único" (bloco 9). Condições: Pix ou cartão à vista, reembolso em até 7 dias, acesso liberado após a confirmação do pagamento, formação e novidades durante o período de acesso. Acesso de 12 meses no FAQ. Sem preço "de" falso.
- **Link do checkout:** `https://infoprodutos-zion.clickmax.space/checkout-zion-47` nos dois botões (`a[data-buy]`). Nenhum outro link externo de compra.
- **UTMs:** o script no fim da página copia `utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_id, fbclid` da URL da landing para os botões, sem duplicar e sem apagar o que já existe. Testado em 27/11 (relatório citado acima). A página **não tem** `fbq`, `gtag` nem `dataLayer` (busca: zero); o pixel do site fica no projeto Lovable e não pude ver aqui.
- **O que já mostra do produto:**
  - Imagens: 6 telas das etapas (`etapa-1..6.jpg`, 640×640), painel (`tela-painel.jpg`) e ficha (`tela-ficha.jpg`) em moldura de notebook e celular, com a legenda "Telas reais da plataforma. Dados fictícios de exemplo."
  - Vídeos: institucional (`expansao-zion.mp4`) e demonstrativo (`plataforma-v02.mp4`).
  - Existem também `tela-aula`, `tela-agenda`, `tela-bemvindo`, `tela-perguntas`, `tela-pilar` na pasta, **não usadas** na página.
  - **Não mostra** um exemplo de dossiê ou prévia do PDF.

### 4.3 O que vi nas imagens do mockup (abri `tela-painel.jpg` e `tela-ficha.jpg`)

- `tela-painel.jpg`: barra "zion-land-bank · inicio", "Olá, Maria", "ZION LAND BANK · MARCO ZERO", texto "Faça o Marco Zero, comece o seu dossiê e agende a sua reunião estratégica com a equipe Zion", trilhas "Desenvolvimento Hoteleiro", "Marco Zero", "Pilar 1", "Pilar 2". É o portal **Land Bank**, com o nome "Land Bank" visível, não o portal "Zion Collection". Também tem aba "Agenda" e "Comunidade".
- `tela-ficha.jpg`: mostra o bloco **"Anexos do seu terreno"**: "Envie fotos, vídeos e documentos do terreno... Aceitamos fotos (JPG, PNG, WEBP, HEIC, até 15 MB), vídeos (MP4, MOV, até 100 MB) e documentos (PDF, DOCX, XLSX, KML, até 20 MB). No máximo 10 arquivos", botão "Enviar arquivos".
  - **Divergência importante:** esse bloco foi **removido do código em 25/11** (`_anexos.js` hoje só mostra texto estático). A imagem é de antes da correção. Se o portal ao vivo já não tem o upload, a landing mostra uma função que não existe.

### 4.4 Afirmações que podem violar as regras do projeto

| Gravidade | Trecho | Problema |
|---|---|---|
| **Alta** | "Anexe fotos e vídeos" (bloco 5, lista) e o mockup `tela-ficha.jpg` com envio de fotos e vídeos | O código atual das fichas **não tem upload**. O D2 aceita só PDF/JPG/PNG (**sem vídeo**). Pode existir o formulário do Airtable da aula do Pilar 7 (citado em `producao/zion-collection/club-97/mini-mentoria/INVENTARIO.md`), mas não comprovei que ele aceita vídeo nem que está liberado para quem compra o R$ 47. **Não comprovado.** |
| **Alta** | "Seu relatório chega completo à nossa equipe" (blocos 5 e 5b, 4 vezes) | O D1 diz, em texto, que **não envia nada** e manda o aluno guardar o PDF. O único caminho que envia é o D2 e o formulário externo. Entrega automática do "relatório completo" à equipe: **não comprovada**. |
| **Alta** | H1 "Seja um parceiro Zion" e CTA "Quero fazer parte da Zion" | "Parceiro Zion" no título afirma um estado. Há asterisco, mas o asterisco está em fonte pequena abaixo do botão. A seção 9 ("Seu terreno pode ser o próximo destino Zion.") **não tem asterisco** e repete a ideia de seleção. Risco de ser lido como promessa de parceria. |
| **Média** | Etapa 04 "Entre para a Zion Land Members" e "torne-se um Land Member"; bloco 5b "Esteja dentro da área de membros" | Afirma uma entrada no Land Bank ligada ao R$ 47. A entrada no banco de áreas, o critério e se é automática: **não comprovados**. Tem asterisco. |
| **Média** | Subtítulo "Transforme seu terreno em um destino turístico." e meta description "Transforme seu terreno..." | É promessa de resultado em forma de imperativo. A regra pede "Aprenda o passo a passo para...". O lead logo abaixo já está correto. |
| **Média** | "Ao final, você tem a apresentação ideal do seu projeto" | "Ideal" promete qualidade do resultado. Melhor: "uma apresentação organizada". |
| **Média** | "Vinte anos de hotelaria internacional" (Bruno) | A frase aparece em outros materiais do repositório (por exemplo `producao/clube/video-2min/ROTEIRO.md`, `zion-sales-engine/06-criativos/...`), mas **não achei confirmação de Bruno como número canônico**. O mapa das sessões já alerta para números da Zion usados sem confirmação. Verificar. |
| **Baixa** | "Hoje a Zion opera glampings e leva a rotina dessas operações para dentro do método" | Está dentro da autorização do `CLAUDE.md` ("quando for verdade para o produto"). Verdade operacional **não comprovada por mim**. |
| **Baixa** | "Zion Glamping Collection" (etapa 6) | Soluções não descritas na página; sem conteúdo para comprovar. |
| **Baixa** | Reunião "gratuita, só para projetos qualificados e sujeita à análise e à agenda" | Conforme, com ressalva. "Projetos qualificados" cria critério que a página não explica. |
| **Conforme** | Depoimentos, números de mercado, urgência, escassez, preço "de" | **Nenhum encontrado** na página. As fotos têm a legenda "Imagens ilustrativas. Fotos reais de operações da Zion." |
| **Conforme** | Reembolso de 7 dias, Pix e cartão à vista | Batem com o padrão do `CLAUDE.md`. O boleto não é citado. |

**Divergência de preço e recorrência:** a landing e `producao/zion-collection/club-97/lt47/LANDING_CHECKOUT.md` falam em **pagamento único de R$ 47 com 12 meses de acesso**. Já o `docs/MAPA_DAS_SESSOES.md` descreve criativos para "R$47/mês por assinatura". Não sei qual é a versão vigente fora da landing. A landing e a oferta aprovada (`668391e7…`, "sem recorrência") concordam entre si.

### 4.5 O que preservar e o que falta para as 10 seções comerciais propostas

| # | Seção proposta | Já existe na landing? | O que preservar | O que falta |
|---|---|---|---|---|
| 1 | Gancho emocional | **Sim** (blocos 1 a 3) | Foto real sem pessoas (`hero.webp`), "Você tem o terreno. Nós temos a experiência.", "Não nos apresente apenas um terreno. Apresente sua visão." | Trocar "Seja um parceiro Zion" por texto que não sugira estado de parceiro. |
| 2 | Como funciona | **Sim** (bloco 5, 6 etapas) | As 6 etapas e a imagem de cada uma | Trocar "anexe fotos e vídeos" e "relatório chega completo" pelo que o produto realmente faz. |
| 3 | Entregável campeão "Meu Projeto Hoteleiro" | **Não** | — | Mostrar o Dossiê (capa, sumário, 2 páginas) como prévia. **O nome "Meu Projeto Hoteleiro" não existe em nenhum arquivo do repositório** (busca em html, md, js, py, json). Hoje o entregável se chama "Dossiê de Desenvolvimento". |
| 4 | Tudo que você recebe | **Parcial** (FAQ e bloco 4) | A frase do FAQ "aulas, vídeos, fichas guiadas e ferramentas..." | Lista concreta e contável. A inspeção de 27/11 cita **9 módulos e 70 aulas** na Plataforma de estruturação (`INSPECAO_PLATAFORMA_DESENVOLVIMENTO.md`), mas a landing não traz números. |
| 5 | Antes e depois | **Parcial** | Bloco 3 (área × empreendimento, 2 fotos) | É um "antes e depois" do terreno, não do projeto do aluno. Falta "dados soltos × Dossiê organizado" com exemplo fictício marcado. |
| 6 | Para quem é | **Não** | — | Bloco não existe (só aparece implícito). Faltam também "para quem não é". |
| 7 | Não precisa saber tudo | **Parcial** | Dado do próprio produto: "Não sei" é resposta válida e vira alerta no D1 | A landing não diz isso. É um ativo real do produto, comprovado no código. |
| 8 | Valor independente | **Parcial** | "A formação é educativa" (FAQ), "O valor refere-se ao acesso à formação digital" (rodapé) | Falta dizer, perto do preço, que o valor não depende de parceria, reunião ou investimento. |
| 9 | Oferta R$ 47 | **Sim** (blocos 6 e 9) | Preço, Pix e cartão, 7 dias, suporte | Duas ofertas seguidas; manter uma só pode ficar mais limpo (decisão de Bruno). |
| 10 | Perguntas frequentes | **Sim** (5 perguntas) | Todas | Faltam: "Preciso enviar documentos?", "Meus dados vão para a Zion?" (relevante, pois D1 não envia e D2 envia), "Funciona no celular?", "E se eu trocar de aparelho?" (o salvamento é local). |

---

## 5. Existe uma área tipo "Meu Projeto Hoteleiro"? (tarefa 4)

**Não, não com esse nome nem com essa função.** O que existe, em ordem de proximidade:

| O que | Onde | O que faz | O que não faz |
|---|---|---|---|
| Hub das ferramentas da Trilha 1 | `docs/trilha1/index.html` | Lista as ferramentas com status "Não começada / Em andamento / Feita", lendo `localStorage` | Só cobre `aula1..aula6` (série antiga). Não cobre Marco Zero nem Pilar 7. Sem barra de progresso, sem prévia do documento. |
| Sumário do D1 | dentro do PDF do Pilar 7 | Tabela de páginas "feita / a fazer" com veredito | Só aparece depois de gerar o PDF. Não há tela de prévia antes do PDF. |
| Mapa de 7 pilares e "Pilares prontos %" | D3 (Terra/Capital), `src/app.html`: abas Início, Jornada, Ferramentas, Dossiê, Materiais; mapa mental "Meu projeto" no centro; barra "N de 20 aulas" | O mais parecido com "meu projeto + progresso" | É de **outro produto** e reutilizável como molde. |
| Painel do portal | mockup `tela-painel.jpg` | "Olá, Maria", trilhas | É do portal Land Bank no ClickMax, não achei código dele no repositório. |
| Progresso nativo do ClickMax | `member_users_get_progress` (ferramenta existe) | — | **Não consultei.** A inspeção de 27/11 diz que nenhum formulário do ClickMax está ligado a aula e que não há critério de conclusão registrado. |

Não achei no repositório: tela de prévia do dossiê antes do PDF; barra de progresso unificada Marco Zero a Pilar 7; backup/restauração das respostas das fichas (o D3 tem).

---

## 6. Ativos reutilizáveis para mockup e página (tarefa 5)

**Fotos reais sem pessoas** (lista do `CLAUDE.md`; conferi só que os arquivos existem e seus tamanhos, não olhei cada um):

| Arquivo | Observação |
|---|---|
| `docs/assets/operacoes/op04.webp`, `op05`, `op07`, `op08`, `op09`, `op10`, `op11`, `op12` | Existem (62 a 152 KB). op08 e op09 já estão na landing. `op01`, `op02`, `op13`, `op14` têm pessoas (não usar sem autorização). `op03` e `op06` existem, mas **não estão na lista oficial**: não usar sem conferir. |
| `docs/assets/store/hero.webp`, `noturna.webp`, `noite.webp`, `deck.webp`, `dentro.webp`, `ceu.webp` | Existem. `hero` e `noturna` já estão na landing. Também há `premium-foto`, `premium-planta`, `suite-foto`, `suite-planta` (plantas e fotos de produto, fora da lista do CLAUDE.md). |
| `docs/zion-collection/club/fotos/bolha-aerea.jpg`, `bolha-interior.jpg` | Existem. Não vinculadas ao CLAUDE.md; conferir origem. |

**Logos oficiais:** `docs/brand/zion-logo-claro.png` (fundo escuro) e `docs/brand/zion-logo-escuro.png` (fundo claro). Já usados na landing (a versão clara).

**Vídeos:**
- `docs/assets/video/expansao-zion.mp4` (15,9 MB) e `expansao-zion-poster.jpg`: na landing.
- `docs/zion-collection/club/video/plataforma-v02.mp4` (20 MB), `plataforma-v02-whatsapp.mp4` (14,5 MB), `poster.jpg`: o demonstrativo da landing.
- `docs/p/adbc67069af26ae0/zc47-videos/zc47-v06.mp4`, `zc47-v12b.mp4`, `zc47-v14.mp4` e capas: criativos de anúncio, não usados na landing.
- `docs/trilha1/trailer/Trailer-Trilha-1-web.mp4` e capas de dor (`capa-dor-*.jpg`): trailers da trilha.
- Não abri nenhum vídeo; conteúdo e narração não verificados (a inspeção de 27/11 também registra narração sintética sem licença registrada nos tutoriais).

**Telas reais da plataforma (para mockup):**
- Em `docs/p/adbc67069af26ae0/landing-zc47/`: `tela-painel`, `tela-ficha`, `tela-aula`, `tela-agenda`, `tela-bemvindo`, `tela-perguntas`, `tela-pilar` (752×496) e `etapa-1..6.jpg` (640×640).
- Em `docs/zion-collection/club/telas/`: `agendar`, `aula`, `diagnostico`, `implantacao`, `mapa`, `previab`, `raiox`.
- **Atenção:** `tela-ficha` mostra o upload que foi removido; `tela-painel` mostra "Land Bank". Antes de reusar, refazer ou conferir.

**Capas e identidade do portal:** `docs/zion-collection/club/capa-club.jpg`, `banner-club.jpg`; `docs/zion-collection/club/membros/` (banner de portal, capas de curso e módulos 01 a 10, horizontal e vertical); `docs/trilha1/capas/` (capas por aula e Marco Zero, 36+ arquivos).

**Fontes oficiais:** `docs/assets/fonts/cormorant.woff2`, `cormorant-italic.woff2`, `aventa.woff2`.

**Código reaproveitável:** o D3 (`producao/produto-01-terra-capital/src/app.html`) já embute as fontes oficiais, usa a paleta oficial, tem backup `.json` e impressão; a lógica do PDF do D1 (`criarPDF`, `capa`, `caixa`, `tabela`) é reaproveitável para a capa personalizada, mas hoje não aceita imagem.

**Fotos de Bruno** (pessoa autorizada por ser o fundador): `docs/assets/bruno/bruno-bubble-urubici.webp` (na landing) e outras da mesma pasta.

---

## 7. Resumo em 10 linhas

1. O "dossiê" tem três versões: D1 (PDF da plataforma, Pilar 7), D2 (Land Bank, envia ao servidor, sem PDF) e D3 (Terra/Capital, outro produto).
2. O D1 cobre bem terreno, mercado, produto, modelo, masterplan, capital, decisão e próximos passos; falha em foto, capa personalizada, atrativos naturais e turísticos e história do projeto.
3. Das 20 seções propostas: 7 existem, 12 são parciais, 1 não existe (fotografias).
4. O PDF não leva foto nem logo; o upload de fotos só existe no D2 e vai ao servidor, não ao PDF; **não há upload de vídeo em lugar nenhum do código**.
5. O D1 salva só no aparelho e não envia nada à equipe; a landing promete "seu relatório chega completo à nossa equipe". Essa promessa não está comprovada.
6. O dossiê não separa "declarado", "orientação" e "verificado"; o terceiro estado não existe.
7. A landing tem 10 blocos, R$ 47 em pagamento único, checkout único e UTMs testadas, sem depoimento, número de mercado ou urgência falsa.
8. Riscos altos na landing: "Anexe fotos e vídeos", "relatório chega completo" e "Seja um parceiro Zion" (sem asterisco no bloco final); o mockup da ficha mostra um upload removido em 25/11.
9. "Meu Projeto Hoteleiro" não existe no repositório; o mais próximo é o hub `docs/trilha1/index.html` e a aba Dossiê/mapa do D3.
10. Identidade: o D1 e as fichas usam Playfair, Inter e Helvetica/Times, fora da paleta e das fontes oficiais; a landing usa Cormorant Garamond e Inter; só o D3 segue a marca.

---

## 8. O que NÃO consegui comprovar

- Que a página `/inscricao` ao vivo é igual a `pagina.html` e que o Lovable a serve agora (domínio bloqueado; só a documentação interna afirma).
- Se `landing-zc47/index.html` é cópia de `pagina.html` (não comparei).
- Se o formulário do Airtable da aula do Pilar 7 (e o de "Cadastro do terreno") aceita fotos e vídeos e está liberado a quem compra os R$ 47.
- Se o portal ao vivo no ClickMax ainda mostra o bloco de upload da `tela-ficha.jpg`.
- Se o "relatório" chega à equipe por algum fluxo automático (D2, Airtable, Lovable `/api/dossie`): não chamei nenhum endpoint e não li o código do servidor Lovable.
- O que `docs/trilha1/territorio/index.html` envia e se está ligado à plataforma de R$ 47.
- Se as fichas `aula4`, `aula5` e `aula6` (Dossiê do Produto antigo) passaram no teste de 25/11 (o teste lista só 8 fichas).
- Que o PDF do D1 abre e fica correto com o jsPDF carregado do cdnjs no navegador do aluno (o teste usou o pacote npm); não gerei nenhum PDF nesta auditoria.
- Se a função de PDF mostra todos os campos listados na seção 2.1 com dados reais (li o código, não abri um PDF).
- A versão vigente do preço (pagamento único de R$ 47 com 12 meses x "R$ 47/mês" do mapa das sessões).
- Origem e confirmação de "vinte anos de hotelaria internacional" por Bruno.
- Aparência e ausência de pessoas em cada foto (conferi existência e nomes, não olhei todas; só abri `tela-painel.jpg` e `tela-ficha.jpg`).
- Conteúdo, duração e licença de narração dos vídeos.
- Progresso nativo do ClickMax (`member_users_get_progress`): não consultei.
- Que o pixel `903918118859018` está ligado ao checkout (a auditoria de rastreamento de 27/11 diz que a Etapa B ainda dependia de Bruno).
