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
- Definição de "receita de hospedagem": inclui ou não a taxa de limpeza; antes ou depois dos impostos. Hoje a taxa de limpeza está fora.
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

## Ainda não verificado
- Entrada real pelo link no e-mail (teste do Bruno).

## Ao publicar
- Revisão jurídica de Termos e Privacidade e e-mail de contato da Zion (Bruno).
- Revisar os e-mails automáticos de acesso (texto e remetente com domínio Zion), que ficam nas configurações do Lovable Cloud, fora do código.
