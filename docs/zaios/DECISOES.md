# ZAIOS · Registro de decisões

## Visão (Bruno Chaerk, 07/11/2026)
A ZAIOS será a maior plataforma de desenvolvimento, gestão e operação hoteleira do mundo, com sistema de inteligência, para profissionalizar o setor: de quem quer aprender a ter uma hospedagem a quem já opera e quer se profissionalizar. A plataforma vai reunir planilhas, agentes de IA, aulas e ferramentas. Ordem combinada: terminar o MVP atual (consolidação e lançamento) e depois seguir para o restante.

Documento de visão: "ZAIOS · Mapa de ativos e visão de integração" (Claude Docs privado do Bruno, 07/11/2026). Não foi copiado para este repositório porque traz detalhes internos (endereços de entregáveis pagos, dados de funil e da Zaya). Resumo do que importa para o roadmap depois do MVP:
- Seis camadas de ativos: conteúdo e trilhas (Trilha 1 com 58 aulas; trilhas 2 a 4 com estrutura sem aulas), 31 ferramentas interativas e 2 planilhas, 23 vídeos, páginas, comunicação (templates, fluxos e a Zaya no ClickMax), dados do lead e a fábrica de peças.
- Quatro blocos da inteligência: registro de ferramentas, base de conhecimento, modelo único do lead e orquestrador por dor.
- Ordem sugerida: (1) registro de ferramentas e base de conhecimento; (2) captura do progresso das fichas no servidor e chave única do lead; (3) orquestrador por dor; (4) conteúdo das trilhas 2 a 4 pela fábrica; (5) medição.
- O MVP do ZAIOS já resolve parte do passo 2: as respostas dos pilares e o Dossiê ficam no servidor, por associado.
- Regras de produção a herdar: identidade Zion com Cormorant e Aventa e o logo oficial; nenhuma promessa de renda, retorno ou parceria; exemplos marcados como fictícios; "equipe Zion" e "ecossistema" no lugar de consultoria, curso ou comunidade.

| Data | Decisão | Quem decidiu |
|---|---|---|
| 05/11/2026 | O MVP atende as jornadas Desenvolvimento e Operação desde o lançamento | Bruno Chaerk |
| 05/11/2026 | A base do projeto é o prompt mestre, o Super Prompt das 4 trilhas e o adendo v2. O PDF "Zion AI Operating System" fica fora do escopo | Bruno Chaerk |
| 05/11/2026 | O MVP sai sem IA generativa: as fichas funcionam como exercícios guiados, com cálculos determinísticos e veredito por regras. A IA entra na fase seguinte, começando por P5 (CAPEX) e P6 (Viabilidade) | Bruno Chaerk |
| 06/11/2026 | Seguir para a Etapa 2 com as fórmulas como "Versão 0, a validar pela Zion" | Bruno Chaerk |
| 06/11/2026 | Iniciar a Etapa 3 por P1, P2 e P3, que não dependem das planilhas | Bruno Chaerk |
| 06/11/2026 | Fazer o Dossiê preliminar antes da Jornada Operação | Bruno Chaerk |
| 07/11/2026 | Construir P5 e P6 com a metodologia dos planos F01 a F03 como versão 0 | Bruno Chaerk ("pode começar") |
| 08/11/2026 | Premissas financeiras decididas para a versão 0, com material e ZAIOS iguais: referências editáveis, sem taxa de desconto sugerida, Zion Score fora da ZAIOS, taxa de limpeza fora da receita de hospedagem (detalhe em PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md) | Claude, por delegação do Bruno ("você decide, tem que estar em harmonia") |

## Regras de linguagem e marca para a ZAIOS (contexto do Bruno, 07/11/2026)
- Nunca prometer renda, retorno, rentabilidade, ocupação, crédito, investimento, investidor, parceria ou sociedade. Usar "possibilidade", "a Zion avalia cada caso", "cenários, não promessas".
- Dizer "equipe Zion", "ecossistema", "trilha", "acompanhamento", "membros". Não dizer consultoria, curso, comunidade, mentoria, sócios (dos membros) nem Airbnb.
- Identidade: preto #040605, musgo #1B2117, creme #FEF5F0, areia #DED6BF, terra #8B714E, dourado #C9B37E; fontes Cormorant e Aventa; logo oficial de docs/brand/; só fotos reais da Zion.
- Exemplos sempre marcados como "dados fictícios".
- Prioridade 1 depois do MVP: ligar os resultados que a ZAIOS já guarda no servidor ao lead (chave única por e-mail e telefone). Os ids e endereços de integração ficam no documento de contexto do Bruno, não neste repositório público.

## Ordem de trabalho (Bruno, 08/11/2026)
1. Teste fechado da ZAIOS em https://zaios.lovable.app (com o Bruno e 2 ou 3 membros).
2. Protótipo da Zion Hotel Academy (prompt do GPT), como camada de aprendizado da ZAIOS, em cópia isolada. Pendente: aprovar o formato e definir a grade oficial.
3. Integração com o ClickMax, depois: webhooks de compra, cancelamento e reembolso para liberar e bloquear acesso; API v0 para gravar o progresso no lead; botões "Fazer no ZAIOS" nas aulas; MCP só para agentes de IA.

## Depois do MVP (pedido do Bruno, 07/11/2026)
- Consumir o documento de visão aos poucos, na ordem do roadmap.
- Construir a identidade própria da ZAIOS: logo, narrativa e linguagem, dentro do padrão da marca Zion.

## Decisões pendentes
- Fonte oficial das fórmulas financeiras (planilhas e simuladores Zion de referência).
- P5 e P6 foram construídos sobre a metodologia dos planos F01, F02 e F03 (ainda marcados para revisão do Bruno). Validar as faixas e regras de referência quando os planos forem aprovados.

## Andamento
| Data | Etapa | Resultado | Créditos |
|---|---|---|---|
| 05/11/2026 | Etapa 1 · Fundação | Login por link, lista de associados, cadastro, Pasta, admin. 8 testes passaram. Projeto Lovable "Zion Empreendimentos" (id 51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc), não publicado | 12 |
| 06/11/2026 | Etapa 2 · Motor | Ajustes da Etapa 1, motor de cálculo (versão 0), motor de exercícios, exercício-modelo "Potencial de faturamento", base de custos | 13,4 |
| 06/11/2026 | Etapa 2 · Correções | Revisão do código encontrou 4 defeitos (leitura de reais com ponto, campos sem limite, concluído voltando a rascunho, recálculo com valor antigo). Corrigidos. 74 testes passaram e o fluxo foi conferido em 390px | 3,9 |
| 06/11/2026 | Etapa 3 · Parte 1 | Motor com blocos, escolha múltipla, listas, veredito e aba Pendências. P1 Território com semáforo por tema. 139 testes | 8,7 |
| 06/11/2026 | Etapa 3 · Parte 2 | Ajustes no P1 (servidão e faixa de rodovia em amarelo; frase por tema). P2 Mercado e P3 Produto. Faixa dos concorrentes no exercício de faturamento. 198 testes | 7,2 |
| 06/11/2026 | Etapa 3 · Parte 3 | Dossiê preliminar: aba Dossiê, 12 seções, selo de qualidade, versões imutáveis no banco, PDF A4 com texto selecionável. CAPEX e viabilidade como "Em breve" | 8,9 |
| 06/11/2026 | Etapa 4 · Parte 1 | Jornada Operação: V1 Raio-X da casa (nota por critério, 5 correções) e V2 Posicionamento. Dossiê de Operação. 227 testes | 9,3 |
| 06/11/2026 | Etapa 4 · Parte 2 | G1 Maturidade da gestão e Plano de Melhoria (sincronizado com as pendências). 260 testes | 13,3 |
| 06/11/2026 | Etapa 4 · Parte 3 | INCOMPLETA. G2 Finanças e G3 Indicadores construídos, mas com erro de build: a prévia não abre. Testes desta parte não escritos. Parou porque o workspace ficou sem créditos | 8,8 |
| 07/11/2026 | Etapa 4 · Parte 3 (continuação) | Testes de G2 e G3 escritos (50 de cálculo e dossiê, 18 de segurança, todos passando) e FORMULAS.md atualizado. Ainda resta 1 erro de compilação na tela de Finanças (campo opcional id). Parou de novo por falta de créditos | 5,0 |
| 07/11/2026 | Etapa 4 · Parte 3 (fechamento) | Erro de compilação corrigido, prévia abrindo. 315 testes passando (inclui segurança). Finanças e Indicadores conferidos em 390px. PDF do Dossiê de Operação baixado e conferido (seções 8, 9, 10 e Plano) | 3,4 |
| 07/11/2026 | Etapa 5 · P5 CAPEX | Sete linhas com evidência, contingência por perfil, giro mínimo, necessidade total, cronograma de desembolso, faixas de referência Zion (F01). Caso de referência F01 conferido (CAPEX 1.237.400). 332 testes | 12,3 |
| 07/11/2026 | Etapa 5 · P6 Receitas | Cascata F02 (receita bruta até geração de caixa), retirada do dono, régua de margem, ponto de equilíbrio, primeiro ano com rampa, capital de giro pelas duas regras. Caso conferido à mão. 352 testes | 10,6 |
| 07/11/2026 | Etapa 5 · P6 Viabilidade | Fluxo de 10 anos, paybacks, VPL e TIR com e sem saída, três cenários, sensibilidade, estresse, curva de caixa de 36 meses, regra de decisão Zion em 5 passos (selo Redesenhar). Casos do F03 conferidos. Dossiê seção 10. 361 testes | 18,4 |
| 07/11/2026 | Etapa 6 · Consolidação, parte 1 | Auditoria de segurança (acessos públicos às funções revogados; análises básica e profunda sem problemas), limite de tentativas no link, Termos e Privacidade (versão 0, revisão jurídica pendente) com aceite obrigatório, baixar e excluir dados do membro, exportação do Admin com alerta de 7 dias. 394 testes | 19,4 |
| 07/11/2026 | Etapa 6 · Consolidação, parte 2 | Identidade oficial Zion (cores, Cormorant e Aventa locais, logo oficial, favicon, PDF com as fontes). Linguagem: associado virou membro, sem Airbnb/mentoria/curso/comunidade/consultoria, "Exemplo com dados fictícios", "Cenários, não promessas.", voz "nós". 394 testes | 6,7 |
| 07/11/2026 | Publicação para teste fechado | Publicado em https://zaios.lovable.app (autorizado pelo Bruno: "vamos provar"). Origem do link de acesso ajustada para o endereço publicado; Lovable Cloud confirmado. 396 testes | 1,3 |
| | **Total até aqui** | | **162,6** |

## Validação das premissas e dos recursos (08/11/2026)
- Teste fechado de 15 itens aprovado para execução. A plataforma só conta como validada depois do teste humano registrado.
- Premissas de F01, F02 e F03 apresentadas em `PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md`, nenhuma aprovada ainda. A taxa de desconto é a mais sensível: 12% muda a decisão do caso F03 2.
- Proposta (não autorizada): tabela "Parâmetros Zion" editável pelo admin, com versões.
- 10 ferramentas e 5 vídeos verificados: todos os testes passaram. Os vídeos mostram "Zion Collection Club" (confirmar o nome).
- Planilha por imóvel suspensa. O G2 atende em parte; ampliar só se o teste confirmar a necessidade.
- Bíblia Operacional: só referência interna, depois de revisão e anonimização.
- Sem produção de e-books, aulas ou POPs e sem alteração de plataformas até o resultado do teste e a validação das premissas.

## Fábrica Educacional · Comando 01 (08/11/2026)
- Auditoria e arquitetura em `docs/academy/COMANDO_01_AUDITORIA_FABRICA.md`. Ciclo de trabalho: GPT define, Claude executa e testa, Bruno encaminha, GPT avalia, Bruno aprova.
- Achado: R$ 270 e R$ 2.900 já são preços de planos do Club Zion Collection (o de R$ 2.900 com acompanhamento semanal). Aguarda decisão antes de qualquer oferta nova.
- Recomendação: 2 agentes novos (arquiteto de módulo, curador de fontes), 1 ampliado e 2 scripts; piloto O03.

## Comando 04 · Reestruturação estratégica (08/11/2026)
- Plano em `docs/academy/comando-04/` (PLANO_REESTRUTURACAO, TECH_STACK_E_FORNECEDORES, PESQUISA_JURIDICA_E_MERCADO). Nada implementado.
- Achado: "Jornada R$ 270" e "Acompanhamento R$ 2.900" já existem como Club Base e Club Pro/Mentoria. Recomendação: uma escada só (Club como marca, Academy como conteúdo). Aguarda decisão do Bruno.
- Primeiro experimento sugerido: experiência gratuita "Venda pelo WhatsApp" para operadores, testada com convidados, sem anúncio.
- Limite: fontes externas lidas por busca indexada (sites bloqueados na rede da sessão); conferir antes de produzir aulas.

## Comando 05A · Arquitetura comercial (09/11/2026)
- **Decisão do Bruno:** arquitetura C, ecossistema integrado com ofertas independentes (Academy marca educacional; Club assinatura por plano; produtos digitais avulsos; Mentoria de Desenvolvimento Zion 360° premium e independente; ZAIOS com permissão por produto). Integração comercial não é unificação.
- Matriz, sobreposições, regras de acesso e impacto em `docs/academy/comando-05a/ARQUITETURA_COMERCIAL.md`. Sobreposições principais: Club Pro x Mentoria (ambos R$ 2.900); "Trilha + Clube R$ 490" x Consultoria prévia R$ 490.
- Blueprint Mestre da Mentoria ainda não recebido. Nada implementado.
- Diretriz da linha B (09/11): B03, B05, B06, B07 e B09 seguem candidatos à venda individual; B01, B02, B04, B08 e B10 sem novas campanhas pagas, uso interno ou como benefício; comparar B06 x Ferramenta 05; novos nomes para B01, B08 e B10; criativos preservados. Matriz final com a sessão Zion Arsenal.

## Comando 05B · Consolidação comercial e financeira (09/11/2026)
- Decisões do Bruno: linha B (venda individual B03, B06, B07, B09; uso interno B01, B02, B04, B05, B08, B10); B06 e F05 como duas soluções distintas; nomes aprovados para B01, B08 e B10 (revisão futura); ZAIOS como referência financeira central, sem homologação automática.
- Auditoria em `docs/academy/comando-05b/`: com premissas idênticas, ZAIOS e B08 coincidem até o centavo (VPL −103.917,01; TIR 7,24%; payback 6,95). Divergências são de premissa e rótulo (D1 a D14), não de fórmula. Dicionário financeiro v0.1 e plano de testes propostos. Nada alterado.

## Dicionário financeiro · decisões metodológicas (09/11/2026, Bruno)
- **D1:** separar retorno anual sobre o investimento e retorno acumulado em 10 anos ("ROI" sem qualificador deixa de ser usado).
- **D4:** diferenciar pró-labore (custo fixo), distribuição de resultados (depois de custos e reservas, não é custo) e caixa disponível.
- **D2-C:** reserva de reposição de 4% provisórios sobre a receita bruta efetivamente realizada, faixa ajustável de 3% a 6%; separada da reserva de emergência; sem descontar o mesmo custo duas vezes; validar o percentual por tipo de hospedagem.
- Efeito futuro (só após homologação): ZAIOS hoje usa 3% da receita bruta; Folha Única J2 usa 4% da receita real; B08 trata a reserva como dedução; A09 não tem reserva. Nenhuma ferramenta alterada.
- **D7-C:** valor de saída por três métodos (múltiplo do EBITDA, avaliação patrimonial, valor estimado informado), sempre com o método identificado, o cenário sem venda ao lado e o valor líquido de custos de venda, tributos e obrigações. Efeito futuro: o B08 hoje usa residual em % do investimento (até 100%); a ZAIOS usa só o múltiplo. Nenhuma ferramenta alterada.
- **D3-A** (correção de registro: já estava aprovada): quebra e perdas são custo variável operacional sobre a receita realizada com hospedagem; referência provisória 1%; prioridade para valores medidos; rótulo quando a ferramenta não calcular; sem dupla contagem com deduções ou reservas.
- **D11-A:** Régua Única de Viabilidade com cinco critérios (geração de caixa, resistência ao conservador, prazo de recuperação, criação de valor com e sem saída, colchão). Ferramentas simples mostram "X de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto." Avançar, Ajustar e Redesenhar só com os cinco critérios e após homologação. Metas do A09 separadas. Limites provisórios, a validar por tipo, porte e perfil. Nenhuma classificação garante viabilidade, financiamento ou retorno.
- Consolidação: dicionário v0.4, `docs/academy/comando-05b/DECISOES_METODOLOGICAS.md` (registro, aderência, pendências, sequência) e plano de testes v0.2. Nenhuma ferramenta alterada.

## Comando 05C · Testes financeiros (09/11/2026)
- Suíte em `testes/financeiro/` (separada da produção): 139 casos T1 a T12, rastreados por teste, indicador, decisão e ferramenta.
- Execução de referência com o motor da ZAIOS (cópia local lida do Lovable, sem créditos, não versionada): 96 OK, 25 divergências confirmadas (metodologia aprovada não implementada), 3 limitações (D5, D6, D8 pendentes), 15 parâmetros pendentes de validação econômica, 0 falhas de fórmula.
- Achado novo: na ZAIOS a faixa da reserva é 3–5% (RESERVA_FAIXA); a D2-C aprovou 3–6%.
- Nenhuma fórmula, ferramenta ou plataforma alterada; nada homologado.

## Comando 05D · Parecer de homologação matemática condicionada (09/11/2026)
- Revisão dos 139 casos: íntegros, categorias exclusivas, 0 falhas. Verificação independente em Python (sem ler o código das ferramentas) confere 79 de 79 valores numéricos com o plano e com as ferramentas; 17 casos lógicos conferidos por definição.
- Proposta (para revisão do Bruno): H1 para os grupos principais da ZAIOS (primitivas de `src/calc`, commit Lovable ec21ad5), núcleo de B08 e A09 e orçamento da F05; H2 para EBITDA com custos do modelo, B08 fora do cenário testado, A09 (360 dias, payback), B06 e Folha J2; nenhum H3; parâmetros e limites da régua em H4.
- Ressalvas: camada de exercícios e G2/G3 da ZAIOS não executadas; cópia da ZAIOS transcrita (confirmar por hash); telas não testadas.
- Observações novas: A09 lança gestão como dedução; B08 calcula o equilíbrio com a reserva dentro das deduções; convenção do payback a registrar.
- Nada corrigido, nada homologado em definitivo; implementação bloqueada.

## Comando 05E · Integridade e testes complementares (09/11/2026)
- Integridade: três transcrições dos 4 arquivos de `src/calc` (commit ec21ad5) são idênticas byte a byte, e a cópia reproduz os valores dos testes da própria ZAIOS. Não há hash calculado na origem (sem GitHub sincronizado). **Integridade não comprovada; ressalva aberta.**
- 98 casos novos (ZAIOS: custos do modelo, outras receitas, estadia, sazonalidade, composição de `src/exercicios`, G2/G3; B08 com rampa e residual; A09 com gestão e contingência; 3 perfis do B06; F05; Folha J2): 93 OK, 2 divergências (veredito sem trava; equilíbrio do B08 com reserva), 3 limitações (gestão no A09, 372 dias no A09, impostos na G2). 0 falhas. Os 139 casos anteriores não mudaram.
- Proposta (para revisão do Bruno): EBITDA da ZAIOS, G2/G3, VPL/TIR do B08, payback do A09 e indicadores da Folha J2 passam a H1; composição da ZAIOS em H2 (cenário único); B06 segue H2 (independência parcial).
- Observações novas: O6 (Folha J2 recebe custos do modelo em R$, o dicionário usa % da receita); O7 (G2 trata impostos como despesa variável). Correção: o A09 aceita até 372 dias/ano, não "no máximo 360".
- Nada corrigido, nada homologado em definitivo; implementação bloqueada.

## Comando 05F · Composição em 3 cenários (09/11/2026)
- 3 cenários (conservador, intermediário com sazonalidade e outras receitas, maior porte) mais o estresse do 3º, executados na cópia da composição (commit ec21ad5) e comparados com cálculo independente em Python: 288 campos, 0 divergências matemáticas, 32 divergências metodológicas (base de gestão e royalties sobre a receita bruta; capital de giro calculado em vez de informado), 7 não aplicáveis (payback e TIR inexistentes, mostrados sem número).
- Observações novas, para classificar: O8 (régua de margem e selo do P6 antes dos custos do modelo); O9 (valor de saída negativo com EBITDA negativo); O10 (horizonte de 36 meses no colchão e no atraso); O11 (base de gestão e royalties); O12 (giro A sem aluguel); O13 (sem campo de capital de giro informado); O14 (outras receitas como % das diárias).
- Proposta: a composição segue H2; a mecânica (demonstrativo, giro, fluxo, VPL, TIR, payback simples, curva, cenários) passa a H1 proposto, condicionado à integridade. Integridade não comprovada. Nada corrigido, nada homologado.

## Comando 05G-A · Decisões O8 a O14 (09/11/2026)
- Aprovadas pelo Bruno, não implementadas: O8 (P6 só com indicação preliminar, sem selo de aprovação, subordinado à análise completa, conflitos explícitos); O9 (saída por múltiplo = MAX(0, EBITDA × múltiplo)); O10 (horizonte de 10 anos: mensal até o mês 36 e anual do 4º ao 10º; alertas de caixa negativo, capital adicional, atraso explicado); O11 (bases independentes de gestão e royalties: hospedagem ou receita bruta, conforme o contrato; hipótese marcada); O12 (giro com fixos, aluguel e obrigações recorrentes, sem duplicidade; 6 meses não aprovados como regra universal); O13 (giro necessário x disponível, déficit ou excedente, sem dupla contagem); O14 (receitas complementares por categoria: ocupação, consumo, independentes).
- Matriz de impacto (arquivos e linhas no commit ec21ad5), plano em 8 etapas, 20 testes de aceite + 1 de integração com esperados independentes; linha de base: 10 de 11 verificações falham hoje, como esperado.
- Pendências anteriores continuam abertas; perguntas novas P-O8 a P-O14 para o Bruno. Nada implementado, nada homologado.

## Ainda não verificado
- Entrada real pelo link no e-mail (teste do Bruno).

## Ao publicar
- Revisão jurídica de Termos e Privacidade e e-mail de contato da Zion (Bruno).
- Revisar os e-mails automáticos de acesso (texto e remetente com domínio Zion), que ficam nas configurações do Lovable Cloud, fora do código.
