# Briefing de pesquisa · Slide 16 · faixas públicas de custo

Objetivo: preencher a tabela do slide 16 com faixas de preço de **serviços profissionais comparáveis** aos entregáveis orientativos do Clube. Nenhum número entra no deck sem os cinco campos abaixo preenchidos e conferidos por uma segunda pessoa.

Este briefing não traz valores. As fontes abaixo são **candidatas**: a existência, a vigência e o escopo de cada uma precisam ser verificados na hora da pesquisa.

## 1. Regras (valem para todas as linhas)
1. **Cinco campos obrigatórios por faixa:** faixa (mínimo e máximo, em R$), fonte (documento e link), data de publicação e de consulta, escopo do que a faixa cobre, e nota de comparabilidade.
2. **Só fonte pública e citável.** Orçamento recebido por telefone ou e-mail não vale como faixa pública. Pode ir para uma pasta de apoio, nunca para o slide.
3. **Comparável é o que entrega algo equivalente ao entregável do Clube** (orientativo, preliminar). Projeto executivo, laudo com responsabilidade técnica ou obra **não** são comparáveis: se a única fonte for desse tipo, a linha fica "sem referência comparável" e sai do slide.
4. **Não somar** serviços que se sobrepõem. Cada linha vale sozinha. Nenhum total, nenhum "economia", nenhum desconto.
5. **CAPEX da obra não é preço dos estudos.** Custo de construir (m², infraestrutura, mobiliário) fica fora desta tabela. Só entra o preço de **estimar** o CAPEX.
6. **Dados de cenário.** O terreno de 10.000 m² e as seis suítes de 45 m² do slide 15 são hipotéticos. A faixa deve valer para o tipo de serviço, não para um município ou uma obra específica. Se a fonte varia por região ou área, citar a região e a área da faixa.
7. **Anotar a data.** Preços envelhecem: no slide, escrever "referência de [mês/ano]". Revisar a cada seis meses.
8. **Sem promessa.** A tabela mostra o que serviços parecidos custam no mercado. Não diz que o Clube substitui esses serviços, nem que o proprietário "economiza".

## 2. Linhas da tabela e onde procurar
| # | Serviço comparável | Entregável do Clube que ele se parece | Tipos de fonte candidatos (verificar) |
|---|---|---|---|
| 1 | Levantamento topográfico | Roteiro de verificação territorial (só como contexto; o Clube não faz topografia) | Tabelas ou referenciais de entidades de agrimensura e topografia; conselhos profissionais (CREA, CFT); tabelas de preço de órgãos públicos, se houver |
| 2 | Estudo de mercado / viabilidade | Modelo de pesquisa de concorrência, matriz de posicionamento | Entidades de economia e administração; SEBRAE (materiais sobre estudo de viabilidade); editais públicos de contratação de estudo de viabilidade turística |
| 3 | Estudo preliminar de arquitetura e masterplan | Diretrizes de produto, exercício de implantação conceitual | Tabela referencial de honorários do conselho de arquitetura e urbanismo (CAU/BR); referenciais de entidades de projetistas (por exemplo SINAENCO) |
| 4 | Estimativa preliminar de CAPEX (orçamento paramétrico) | Planilha de CAPEX Zion | Referenciais de honorários de engenharia de custos; editais públicos de orçamento. Para **custo de obra** (não entra na tabela): CUB (Sinduscon) e SINAPI, só como contexto |
| 5 | Modelagem econômico-financeira | Simulador econômico-financeiro Zion | Referenciais de entidades de economia e finanças; editais públicos de consultoria de modelagem |
| 6 | Consulta e due diligence fundiária | Checklist de documentos, roteiro regulatório | Tabela de honorários da seccional da OAB do estado escolhido (advocacia); emolumentos de certidões em cartórios, que são taxas públicas e estão em tabelas oficiais |

Fontes mais fortes: tabelas publicadas por conselho ou entidade de classe e **editais públicos** (preço de referência de contratação). Fontes mais fracas: sites de empresas e blogs. Estes só servem para localizar uma fonte melhor, não para citar.

## 3. Modelo de registro (uma linha por faixa encontrada)
| Campo | Preencher |
|---|---|
| Serviço | (uma das 6 linhas) |
| Faixa | R$ ___ a R$ ___ (e a unidade: por projeto, por hora, por m²) |
| Fonte | nome do documento + entidade + link |
| Data da fonte / data da consulta | ___ / ___ |
| Escopo coberto | o que está incluído e o que não está |
| Região e porte | estado, área ou tamanho a que a faixa se refere |
| Comparável ao Clube? | sim, parcial ou não, e por quê |
| Conferido por | nome e data (segunda pessoa) |

## 4. Como entra no slide 16
- Colunas: serviço, faixa, fonte, data, escopo, comparável.
- Linha com "não" em comparável ou sem fonte: sai do slide.
- Rodapé fixo: "Referências públicas de [mês/ano]. Serviços diferentes do Clube, que é orientativo e não substitui projeto, laudo nem licença. Valores variam por região e escopo."
- Atualizar o `index.html` do deck (slide 16) e rodar `tests/test_deck.js`.

## 5. Quem faz e quanto tempo
Pesquisa e preenchimento: pessoa indicada por Bruno (ou uma sessão de pesquisa com acesso à web, com a conferência final humana). Estimativa de esforço, sem prazo prometido: um dia de trabalho para seis linhas, mais a conferência.

## 6. Perguntas para Bruno antes de começar
1. Quem pesquisa e quem confere?
2. Estado ou região de referência: Santa Catarina (onde a Zion opera) ou faixa nacional?
3. Quantas linhas manter no slide, se algumas ficarem sem fonte comparável?

## 7. Decisões de Bruno (16/11/2026)
- Referência: **Santa Catarina**.
- Linha sem fonte comparável **sai do slide**. Se nenhuma linha tiver fonte, o slide 16 sai do deck (a ordem dos 20 slides só muda com nova autorização).

## 8. Resultado da 1ª rodada (16/11/2026): nenhuma faixa qualificada ainda
Busca na web feita; as páginas das entidades **não puderam ser abertas** (a rede da sessão bloqueou `portal.crea-sc.org.br` e `honorario.caubr.gov.br`). Nenhum valor foi tirado de memória. Estado das seis linhas:

| # | Serviço | Estado | O que a busca indicou (a verificar abrindo a fonte) |
|---|---|---|---|
| 1 | Levantamento topográfico | sem faixa qualificada | O CREA-SC tem uma página "Tabelas de Honorários registradas" (IBAPE, ACEST, AEAO, SENGE). Não vi se alguma cobre topografia. Um orçamento de contrato em Goiás (2021) citou R$ 0,43 a R$ 0,49 por m² no levantamento planialtimétrico: é de outro estado e de um contrato específico, **não serve** para o slide |
| 2 | Estudo de mercado / viabilidade | sem faixa qualificada | Nenhum edital catarinense com preço de referência foi achado. Pistas: Portal de Compras SC, Compras.gov.br, chamamento de Itapema (estudos em cadernos) |
| 3 | Estudo preliminar de arquitetura | sem faixa qualificada | A Tabela de Honorários do CAU/BR existe (Resoluções 64/2013 e 76/2014, segundo um documento do TRT-3), mas é **fórmula** (área, valor-base por m², fator), não faixa em R$. Para virar faixa seria preciso aplicar a fórmula a um caso, o que é cálculo nosso e não fonte pública pronta |
| 4 | Estimativa preliminar de CAPEX | sem faixa qualificada | Nada localizado |
| 5 | Modelagem econômico-financeira | sem faixa qualificada | Nada localizado |
| 6 | Consulta e due diligence fundiária | sem faixa qualificada | A tabela da OAB/SC existe (TJ-SC já a aplicou em 2022; uma página não oficial cita versão de 2025). Não achei item de due diligence imobiliária com valor. Tabelas de outros estados não valem para SC |

## 9. Próximos passos possíveis
1. Liberar a rede da sessão para `portal.crea-sc.org.br` e `honorario.caubr.gov.br` (e o site da OAB/SC e do CAU/SC) e refazer a leitura; ou
2. Bruno (ou quem ele indicar) baixa os PDFs (tabelas registradas no CREA-SC, Tabela CAU/BR, tabela OAB/SC) e coloca em `producao/metodo-zion-360/fontes/`; eu extraio as faixas com os cinco campos; ou
3. Aceitar que o slide 16 sai do deck por falta de fonte (regra acordada).
Em qualquer caso, a conferência por uma segunda pessoa continua obrigatória.

## 10. Resultado da 2ª rodada (16/11/2026, rede liberada, leitura direta)
Lidas as 11 tabelas da página "Tabelas de Honorários Registradas no Crea-SC" (`portal.crea-sc.org.br/profissional/honorarios/`). Não abriram: `honorario.caubr.gov.br` e `causc.gov.br` (403), `caubr.gov.br` (sem resposta). A tabela da OAB/SC fica numa calculadora online (`calculadora-honorarios.oab-sc.org.br`), sem documento para baixar; não extraída.

### Faixa que passou nas regras (1 de 6 linhas), conferência humana pendente
| Campo | Registro |
|---|---|
| Serviço | 1 · Levantamento topográfico |
| Faixa | **R$ 630,00 por hectare** (valor **mínimo**), levantamento topográfico planialtimétrico |
| Fonte | AGESC (Associação Profissional de Geólogos de Santa Catarina), "Tabela de Honorários Profissionais para Geólogos ou Engenheiros Geólogos 2024 2025", item 11 "Trabalhos Específicos". Registrada no CREA-SC. Cópia em `fontes/AGESC_tabela_honorarios_2024-2025.pdf`; origem: `portal.crea-sc.org.br/download/tabela-de-honorarios-da-agesc/` |
| Data | Aprovada em assembleia de 20/05/2024; valores "atualizados até maio de 2024", com reajuste anual previsto por IGP-M (não aplicado). Consulta: 16/11/2026 |
| Escopo | Valor mínimo; exclui encargos fiscais, viagens, hospedagem, alimentação e diárias de campo. Não inclui mobilização |
| Região e porte | Santa Catarina; por hectare (o terreno hipotético de 10.000 m² tem 1 ha, mas a faixa vale para o serviço, não para o cenário) |
| Comparável ao Clube? | **Parcial.** É tabela de associação de geólogos, não de agrimensores, e o Clube não faz topografia; serve só como referência de um serviço que o proprietário contrata à parte |
| Conferido por | **pendente** (segunda pessoa) |

### Linhas sem fonte comparável (saem do slide pela regra)
- **2 Estudo de mercado / viabilidade:** as tabelas registradas só trazem viabilidade ambiental (AEFsul: R$ 2.000 a R$ 15.000) e viabilidade de água mineral/balneário (AGESC: R$ 12.500). Nenhuma é viabilidade econômica de empreendimento de hospedagem.
- **3 Estudo preliminar de arquitetura / masterplan:** nenhuma tabela de arquitetura entre as registradas; a do CAU/BR não abriu (e é fórmula).
- **4 Estimativa de CAPEX, 5 Modelagem financeira, 6 Due diligence fundiária:** nada nas tabelas lidas; OAB/SC não extraída.

### Achados fora das 6 linhas (não usar sem decisão de Bruno)
- AREA/IT (Itajaí, 04/11/2024): hora técnica de consultoria R$ 375 (júnior), R$ 600 (sênior), R$ 750 (máster); mínimo de 8 horas por consulta.
- AEFsul (dez/2025): avaliação de imóvel rural de 0,05% a 3% do valor do imóvel; parecer a R$ 400 por matrícula.
- SEAGRO: topografia em SMP por km/ha (precisa do valor do SMP vigente para virar R$).

### Efeito no slide 16
Com a regra "linha sem fonte sai", sobra **uma** linha (topografia, comparabilidade parcial). Uma tabela de uma linha não sustenta o slide. Opções em aberto para Bruno: (a) tirar o slide 16 e seguir com 19; (b) manter com 1 linha e a nota de parcial; (c) ampliar a busca (OAB/SC, CAU/SC, editais) antes de decidir.
