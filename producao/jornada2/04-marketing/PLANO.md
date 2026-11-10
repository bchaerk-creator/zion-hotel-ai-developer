# Jornada 2 · Gestão · Módulo 4 · Marketing e vendas · Plano da lição (G04)

Status: produzido em 10/11/2026 para revisão de Bruno. Entregável: **Marca e Captação** (página 4 do Plano de Gestão): a marca em uma folha, a lista própria de contatos com autorização e o custo por reserva de cada canal, com a meta de venda direta. Nada publicado no ClickMax, nada ativado. Não altera outros módulos nem o Kit de Mensagens (Ferramenta 11): aponta para ele e lê, sem gravar, a meta de venda direta do Painel de Gestão (Módulo 1) e o nome deixado pelos módulos anteriores no aparelho.

## 1. A lição em uma frase
Aprenda o passo a passo para dizer por que alguém escolheria a sua hospedagem, começar a sua lista própria de contatos com autorização e saber quanto custa cada reserva em cada canal.

## 2. Públicos e jornadas
- **Desenvolvedor (vai abrir):** escreve a promessa e a frase de autorização antes do primeiro hóspede; usa números previstos nos canais; a ficha avisa para refazer a tela de canais no primeiro mês aberto.
- **Gestor (dono que opera):** público central; usa o último mês.
- **Operador (cuida para outro dono):** usa a folha de marca para alinhar o tom com o dono e o custo por reserva para prestar contas.
- Jornada A (quero começar) e B (já opero) tratadas na abertura (situação, nível) e pela regra "zero vale" na lista e nos canais.

## 3. Fontes Zion (mapa completo fora do repositório)
- **Panorama, Trilha B, Pilar G1 · Marca e Narrativa** (espinha da folha de marca): "O hóspede não compara quartos. Compara motivos."; marca "não é logotipo nem paleta"; quatro passos (promessa em uma frase sem adjetivo; teste em cinco pessoas de fora; a promessa na primeira foto; repetir em todos os pontos de contato); erro comum "confundir identidade visual com marca"; entregável "a promessa de uma linha e os pontos de contato mapeados".
- **Panorama, Trilha B, Pilar G4 · Captação de Hóspede** (espinha da lista e do custo por reserva): "Audiência alugada não é audiência."; seguidor × contato; quatro passos (lista com autorização explícita fora do celular; quem já veio × quem nunca veio; um canal bem feito; custo por reserva "quanto você gastou dividido por quantas reservas vieram daquele esforço"); erro comum "trocar a lista própria por seguidores"; entregável "o Plano de Captação com a base própria iniciada e o custo por reserva calculado".
- **Panorama, G2** (meta de venda direta "um número, não uma intenção. E o prazo") e **G7** (venda direta é um dos cinco indicadores do Painel).
- **Jornada do COMO, Etapa 05 "Criar uma marca"**: três decisões (promessa, para quem, o que nunca faz); Frase de Promessa Zion™ (ocasião, experiência, elemento; quatro testes; cortar adjetivos genéricos); Guia de Tom de Voz™ (três decisões e lista de banidos); Marca em Uma Folha Zion™ (nove linhas; a folha deste módulo usa quatro obrigatórias e uma opcional e remete às nove).
- **Jornada do COMO, Etapa 07 "Como eu encho"**: quatro fontes de ocupação; pergunta "como você chegou até nós?" (canal de reserva × fonte real); Base de Hóspedes Zion™ (oito campos, frase de autorização no check-in, "quem não aceita fica na base de registro, para histórico, e não recebe nada", planilha fora do canal com cópia); Plano de Recorrência™ (quatro contatos por ano, sempre com o caminho de reserva direta).
- **Referência de estrutura (sem conteúdo):** "Arquivo · Trilha 4 · Aceleração de vendas" no ClickMax (sete módulos vazios: identidade e marca; produto e experiência; anúncio e canais; preço; reserva direta e sistemas; marketing; plano de 90 dias). Aqui ficam só marca, lista e custo por reserva; preço e canais estão no Módulo 3.
- **Reaproveitado sem alterar:** Ferramenta 11 · Kit de Mensagens de Chegada e Saída (`docs/p/adbc67069af26ae0/kit-mensagens-11/`): M04 boas-vindas e M08 agradecimento com pedido de avaliação honesta são pontos de contato da promessa e o primeiro dos quatro contatos do ano.

## 4. Objetivos (verbos observáveis)
1. Explicar por que marca é motivo e não logotipo, e as três decisões que a formam (compreender).
2. Escrever a promessa em uma frase sem adjetivo genérico e avaliá-la pelos quatro testes e pelo teste das cinco pessoas (criar, avaliar).
3. Escolher a prova e o tom, e mapear em quais pontos de contato a promessa falta (aplicar, analisar).
4. Montar o começo da lista própria: frase de autorização, lugar fora do celular com cópia, um canal e uma meta com ritmo (criar).
5. Calcular o custo por reserva de cada canal e a venda direta do último mês (aplicar).
6. Conferir a meta de venda direta contra a de hoje e contra o Painel (Módulo 1), e o que ela pede num mês com a mesma receita (analisar).

## 5. As seis etapas
| Etapa | Peça | Duração |
|---|---|---|
| Diagnosticar | Abertura da ficha: situação e 4 perguntas Sim/Não → nível 1 a 4 | 1 min |
| Compreender | Aula em vídeo (12 cenas, cerca de 5 min) + resumo em PDF (8 páginas) | 6 min + leitura |
| Observar | Tutorial da ficha com o exemplo Cabanas do Vale | cerca de 4 min |
| Executar | Ficha "A minha Marca e Captação" (5 telas) + planilha "Plano de Captação" | 20 a 25 min |
| Validar | Resultado em cinco partes + critério de conclusão (selo) | 2 min |
| Entregar | PDF (página 4 do Plano de Gestão) + próxima etapa (Módulo 5) + prompt de IA | 2 min |

## 6. Regras da ferramenta (testáveis, `src/logic.js`)

### 6.1 Entradas
- Abertura: `nome`, `email`, `hospedagem`, `situacao` (abrir, dono, operador), `diag` {promessa, lista, canal, custo} Sim/Não.
- Marca: `publico` (3 letras ou mais), `naoPublico` (opcional, aviso), `promessa` (10 letras ou mais), `testes` {recusa, cumprimento, diferenca, memoria} Sim/Não, `cinco` ("nt" = ainda não testei, ou 0 a 5).
- Prova: `prova`, `tom` (obrigatórios), `banidas` (aviso se vazio), `nunca` (opcional), `pontos` {anuncio, site, redes, whatsapp, boasvindas, placa} = sim, nao ou na (não tenho), todos obrigatórios.
- Lista: `contatos` e `autorizados` (inteiros ≥ 0, autorizados ≤ contatos), `onde` (nuvem com cópia, sem cópia, celular, plataforma, caderno), `acesso` (aviso), `frase` (10 letras ou mais), `canalLista` (WhatsApp ou E-mail), `metaLista` (inteiro ≥ 1 e ≥ autorizados), `estadiasMes` (1 a 9999).
- Canais (até 6): `nome`, `tipo` (plataforma ou direto), `reservas` (inteiro ≥ 0), `receita` (≥ 0), `comissao` (0 a 99%, vazio = 0, aviso em plataforma), `gasto` (≥ 0, vazio = 0); linha com número e sem nome bloqueia; receita sem reserva bloqueia; total de reservas e de receita maior que zero; `mesCanais` obrigatório; aviso se não há canal direto.
- Meta: `metaDireta` (0 a 100, maior que zero), `prazoMeta` (data válida).
- Números aceitam "1.234,56", "8.120" (ponto de milhar = oito mil), "4.7" (ponto decimal) e "R$"/"%" (função `num` corrigida no Módulo 1).

### 6.2 Cálculo
- Por canal: `comissão = receita × comissão% ÷ 100` (só plataforma); `custo = comissão + gasto`; `custo por reserva = custo ÷ reservas` (sem reserva: vazio); `custo ÷ receita do canal`.
- Totais: receita, reservas, custo, custo médio por reserva, captação sobre a receita.
- `venda direta = receita direta ÷ receita` (definição do Módulo 1) e também pela parte das reservas (Etapa 07).
- `comissão média das plataformas = comissão das plataformas ÷ receita das plataformas`.
- `receita direta que a meta pede = receita × meta ÷ 100`; `comissão que deixaria de sair = max(0, pedida − atual) × comissão média das plataformas` (conta, não previsão).
- Lista: `faltam = max(0, meta − autorizados)`; `por mês = faltam ÷ 12`; `parte das estadias = por mês ÷ estadias do mês`.
- Marca: testes com Sim, adjetivos genéricos encontrados (aconchegante, único, especial, exclusivo, inesquecível, incrível, perfeito, sem acento e sem maiúscula), pontos de contato com e sem a promessa.
- Nível de abertura: número de "sim" nas 4 perguntas → 1 Audiência alugada, 2 Começando, 3 Quase lá, 4 Captação com número (elaboração declarada).

### 6.3 Leituras (sem régua de mercado)
1. Custo por reserva do mais barato ao mais caro, a média e a parte da receita.
2. Venda direta hoje, a meta com prazo, o que ela pede e a comissão que deixaria de sair (conta).
3. Ritmo da lista: autorizações por mês e parte das estadias.
4. Marca: testes, cinco pessoas e pontos de contato onde a promessa falta.

### 6.4 Atenção (ordem)
1. `semAutorizacao`: nenhum contato com autorização. 2. `guardada`: lista no celular, só na plataforma, sem cópia ou no caderno. 3. `adjetivo`: promessa com adjetivo genérico. 4. `testes`: algum dos quatro testes com Não. 5. `cinco`: não testada ou menos de 5 de 5. 6. `caroDireto`: canal direto com gasto e custo por reserva maior que a plataforma mais barata. 7. `gastoSemReserva`: gasto sem reserva. 8. `metaAbaixo`: meta que não passa da venda direta de hoje. 9. `painel`: meta diferente da meta de venda direta do Painel (Módulo 1). 10. `ritmo`: a meta da lista pede mais autorizações que estadias. Sempre: o erro comum do G4.

### 6.5 O que fazer e como verificar
- Plano sugerido (editável): pedir a autorização no próximo check-in com a frase e registrar na aba Lista própria; perguntar a todo hóspede como chegou e recalcular o custo por reserva no fim do mês; levar a promessa aos pontos de contato que faltam (com o Kit 11); testar a promessa com cinco pessoas (se ainda não foi 5 de 5); fazer bem um canal (os quatro contatos do ano); não aumentar o gasto do esforço mais caro antes de medir (se houver); olhar a venda direta na reunião semanal do Painel.
- Como verificar: em 30 dias, a aba Lista própria tem uma linha por estadia com a autorização registrada e a aba Captação do mês tem o canal de cada reserva e o custo por reserva; a promessa aparece nos pontos de contato que faltavam; todo mês, a aba Captação 12 meses compara a venda direta com a meta.

### 6.6 Critério de conclusão (selo)
Ficha completa (situação, marca, prova, lista, canais e meta válidos), plano com 10 letras ou mais, data do primeiro check-in com o pedido de autorização e PDF baixado.

## 7. Telas da ficha "A minha Marca e Captação"
0 Abertura → 1 Para quem e a promessa → 2 A prova e o tom (com o link do Kit 11) → 3 A lista própria → 4 Os canais e o custo por reserva (um canal na tela, botão "Adicionar outro canal" até 6) → 5 A meta de venda direta (com o botão "Usar a meta do meu Painel" quando o Módulo 1 foi feito no aparelho) → Resultado: venda direta e meta, marca em uma folha, tabela de canais, lista; leituras; atenção; erro comum; plano editável com data; critério de conclusão; PDF; próxima etapa (Módulo 5). Chave local `zion-t2-marketing`.

## 8. Planilha "Plano de Captação" (openpyxl, em branco e exemplo)
Abas: Comece aqui · Marca em uma folha (para quem, promessa, quatro testes, cinco pessoas, prova, tom, banidas, o que nunca fazemos, seis pontos de contato; conferência de testes, adjetivo genérico e pontos que faltam; "Situação da folha") · Captação do mês (8 canais com tipo, comissão, gasto, reservas e receita; comissão, custo, custo por reserva e custo ÷ receita; totais; venda direta pela receita e pelas reservas; comissão média das plataformas; meta e prazo; o que a meta pede; comissão que deixaria de sair; menor e maior custo por reserva; "Situação dos dados") · Lista própria (frase, lugar, acesso, canal, contatos antigos, meta, estadias; contatos, autorizados, faltam, ritmo, leitura e situação; 200 linhas com os oito campos da Etapa 07 mais "voltou?") · Captação 12 meses (receita, receita direta, reservas, custo, contatos autorizados; venda direta, custo por reserva e "Na meta / Abaixo da meta") · Definições e rotina (termos, os quatro contatos do ano, a rotina).

## 9. Exemplo didático (dados fictícios, conferidos duas vezes)
Cabanas do Vale, 4 unidades na serra, a Ana opera sozinha. Mesmo mês dos módulos 0, 1, 2 e 3: outubro de 2026, 25 reservas, R$ 16.240,00 de hospedagem, mix do Módulo 3 (Plataforma A 50%, Plataforma B 20%, venda direta 30%) e comissão de 11,0% da receita total (Módulo 2).
- Marca: para quem "casais que vêm de carro, de até três horas de distância, para duas ou três noites"; não é para "grupos, festas e quem procura agito à noite"; promessa "Duas noites a dois, com a lareira acesa e o vale na janela da cama, sem vizinho à vista." (sem adjetivo genérico; quatro testes com Sim; 4 de 5 pessoas entenderam); prova: a foto de capa com a cama de frente para a janela e a lareira acesa; tom "próximo, concreto, calmo"; banidas "aconchegante, único, inesquecível, refúgio, experiência única"; nunca "festas nem mais de duas pessoas por cabana". A promessa aparece no anúncio e nas redes; falta no site, na resposta de WhatsApp, na mensagem de boas-vindas e na placa (4).
- Canais: Plataforma A 12 reservas, R$ 8.120,00, 16% → R$ 1.299,20, **R$ 108,27** por reserva; Plataforma B 5, R$ 3.248,00, 15% → R$ 487,20, **R$ 97,44**; Instagram com impulsionamento 2, R$ 1.120,00, gasto R$ 150,00 → **R$ 75,00**; Hóspede que volta (WhatsApp) 3, R$ 1.848,00 → R$ 0,00; Indicação 3, R$ 1.904,00 → R$ 0,00. Total 25 reservas, R$ 16.240,00, custo R$ 1.936,40, **R$ 77,46** por reserva, 11,9% da receita. Comissão das plataformas R$ 1.786,40 = 11,0% da receita total; comissão média das plataformas 15,7%.
- Venda direta: R$ 4.872,00 = **30,0%** da receita (8 de 25 reservas, 32%). Meta **40% até 30/06/2027** (a mesma dos Módulos 1 e 3): pede R$ 6.496,00 num mês com a mesma receita; deixariam de sair **R$ 255,20** de comissão (R$ 1.624,00 × 15,71%, igual ao Módulo 3).
- Lista: 64 contatos no celular, 0 com autorização; acesso só da Ana; canal WhatsApp; meta 120 em 12 meses → **10 autorizações por mês, 40% das 25 estadias**.
- Atenção no exemplo: lista sem autorização; lista só no celular; 4 de 5 entenderam. Plano com 6 passos; primeiro check-in com o pedido de autorização: 20/11/2026.
- Planilha, aba Captação 12 meses (fictício): outubro de 2026 30,0%, R$ 77,46 por reserva, abaixo da meta; novembro de 2026 R$ 12.950,00 de receita, R$ 4.144,00 direta (32,0%), 21 reservas, R$ 1.533,80 de custo (R$ 73,04 por reserva), 18 contatos autorizados, abaixo da meta.

## 10. Versão autônoma e acompanhada
Mesmo conteúdo. No acompanhamento Zion 360°, a equipe Zion revisa a folha de marca e a frase de autorização no marco da semana 6 e confere, em 30 dias, se a aba Lista própria tem uma linha por estadia.

## 11. Decisões e lacunas declaradas
- **Folha de marca com quatro linhas obrigatórias** (para quem, promessa, prova, tom) e uma opcional (o que nunca fazemos), como pede o entregável; a Etapa 05 tem nove linhas e o resumo remete a ela.
- **"Prova"** = a foto que prova a promessa (G1, passo 03 e item 3 do exercício). A fonte fala em foto; a ficha aceita "a foto ou a prova".
- **Custo por reserva com a comissão dentro** (elaboração a partir do G2, "cada canal tem um custo de aquisição diferente"); taxa de cartão e imposto ficam na Folha Única do Módulo 2.
- **Venda direta pela receita** (definição do Módulo 1); a planilha mostra também pela parte das reservas (Etapa 07).
- **Meta de venda direta com data** (como o Módulo 3), não em meses; o exemplo segue a correção de coerência do integrador (30% → 40% até 30/06/2027).
- **Sem régua de mercado:** os percentuais de "composição saudável" da Etapa 07 não entram (poderiam ser lidos como promessa). A ficha só confere coerência (meta acima da atual, ritmo da lista dentro das estadias).
- **Autorização e regras das plataformas:** as fontes falam em "autorização explícita"; não tratam de lei de proteção de dados. A ficha e o resumo pedem conferir as regras da plataforma e procurar profissional habilitado. Mesma cautela do Kit 11 (não leva conversa da plataforma para outro canal por conta própria).
- **Lista na planilha de exemplo:** as linhas de hóspedes ficam vazias para os números baterem com a ficha (64 contatos antigos, 0 autorizados).
- **Nível de abertura** e ordem das regras de atenção são elaboração.
- **Interface com o Módulo 1:** a ficha lê `zion-t2-planejamento` (meta de venda direta) e oferece usar a mesma meta; não grava nada na chave do Módulo 1.
