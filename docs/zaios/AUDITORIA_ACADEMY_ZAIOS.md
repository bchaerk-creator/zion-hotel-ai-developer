# Auditoria e plano · ZAIOS + Zion Hotel Academy + ClickMax

Data: 08/11/2026 · Responsável: Bruno Chaerk · Status: planejamento. Nenhuma alteração foi executada nesta etapa e nenhum crédito Lovable foi gasto.

Como esta auditoria foi feita: leitura do repositório (ramo `main`), da fila de produção do Método Zion 360° (`producao/fila.json`), da área de membros do ClickMax (somente leitura, via MCP) e do código da ZAIOS. Os status abaixo vêm desses registros e da estrutura dos arquivos. Os e-books e vídeos não foram lidos página por página nesta etapa: onde a qualidade não foi conferida, isso está dito.

Legenda de classificação:
- **Pronto**: existe, funciona e pode ser reaproveitado como está.
- **Adaptar**: existe, mas precisa de revisão, aprovação ou ajuste para entrar na Academy.
- **Estrutura**: só existe o esqueleto (módulo vazio, plano, título).
- **Falta**: ainda não existe.

---

## 1. Teste fechado da ZAIOS (Fase 1)

Situação: a ZAIOS está publicada em https://zaios.lovable.app, mas **ainda não foi testada por uma pessoa**. O ambiente do Claude Code não consegue abrir o endereço publicado (bloqueio de rede) e não recebe o e-mail de acesso. Os testes automáticos (396) e as conferências de tela feitas pelo Lovable na prévia não substituem este teste.

Roteiro de teste (Bruno e 2 ou 3 membros; anotar o resultado de cada linha):

| # | O que testar | Como | Resultado esperado |
|---|---|---|---|
| 1 | Login | Pedir o link com um e-mail liberado | E-mail chega em poucos minutos; o link abre a ZAIOS publicada |
| 2 | Bloqueio | Pedir o link com um e-mail não liberado | Mensagem "ainda não tem acesso"; nenhum e-mail enviado |
| 3 | Consentimento | Primeiro acesso | Exige aceite dos Termos e da Privacidade |
| 4 | Cadastro | Criar um empreendimento com dados incompletos | Salva e aparece no painel |
| 5 | Jornada Desenvolvimento | Fazer P1, P2, P3, P5, P6 Receitas, P6 Viabilidade | Cada pilar salva, retoma, calcula e mostra o veredito |
| 6 | Jornada Operação | Fazer V1, V2, G1; lançar 3 meses no G2; ocupação no G3 | Painéis e indicadores coerentes com a conta à mão |
| 7 | Cálculos | Conferir um caso simples à mão (ex.: 3 unidades, R$ 680, 38%) | Mesmos números |
| 8 | Recálculo | Mudar unidades no cadastro | Exercícios afetados aparecem como "Desatualizado" |
| 9 | Pendências e Plano | Marcar uma ação como feita | A pendência de origem fica resolvida |
| 10 | Dossiê | Gerar versão, baixar PDF, mudar um dado, gerar nova versão | PDF legível; versões antigas preservadas |
| 11 | Permissões | Membro A tenta abrir o link de um empreendimento de B | Não vê nada |
| 12 | Admin | Liberar, suspender, exportar dados | Funciona; suspenso perde acesso na hora |
| 13 | Meus dados | Baixar meus dados; excluir conta de teste | Arquivo completo; exclusão apaga tudo |
| 14 | Celular | Repetir 4, 5 e 10 no celular | Sem rolagem lateral; tudo clicável |
| 15 | Erros | Campos absurdos (ocupação 150%, diária com ponto) | Mensagem clara, sem quebrar |

Pendências já conhecidas antes do teste: e-mail de contato da Zion nos Termos; revisão jurídica de Termos e Privacidade; texto e remetente do e-mail automático de acesso.

---

## 2. Inventário técnico (o que já existe)

| Item | Quantidade | Onde | Classificação |
|---|---|---|---|
| ZAIOS: login por link, lista de liberados, papéis, segurança por linha, consentimento, exportar e excluir dados, backup | 1 plataforma | zaios.lovable.app | Pronto (falta teste humano) |
| ZAIOS: motor de exercícios (blocos, "Não sei", veredito, pendências, recálculo) | 1 | ZAIOS | Pronto |
| ZAIOS: motor de cálculo determinístico com testes (centavos, origem do dado, fórmulas versão 0) | 1 | ZAIOS `src/calc` | Pronto (fórmulas aguardam validação da Zion) |
| ZAIOS: exercícios e ferramentas | 13 (P1, P2, P3, P5, P6 Receitas, P6 Viabilidade, Potencial, V1, V2, G1, G2, G3, Plano de Melhoria) | ZAIOS | Pronto |
| ZAIOS: Dossiê em PDF com versões imutáveis | 1 | ZAIOS | Pronto |
| ZAIOS: painel administrativo | 1 | ZAIOS | Pronto |
| Fichas "Faça agora" da Trilha 1 (HTML, salvamento local, PDF) | 8 (+ versões antigas das aulas 4 a 6) | docs/trilha1 | Adaptar (resultado fica só no aparelho; parte duplica a ZAIOS) |
| Mini mentorias interativas (40 telas, ECROI, 7 pilares, PDF) | 20 (A01 a A10, B01 a B10) | docs/p/…/zar-* | Pronto como produto de entrada; Adaptar para a Academy |
| Utilitários prontos (planilha + guia + PDF) | 6 (Planilha Diária Mínima, Kit de Mensagens 11, Enxoval 13, Ocorrências 14, Checklist de Limpeza 17, Custos de Experiências 29) | producao/utilitarios, low-ticket | Pronto |
| Catálogo de 30 ferramentas utilitárias | 30 planejadas, 6 prontas | producao/catalogo/CATALOGO.md | Estrutura (24 a fazer) |
| Planilhas da Trilha 1 (Orçamento de Abertura; Estudo de Massas e Viabilidade) | 2 | docs/trilha1/materiais | Pronto |
| Kit do Investidor, Mapa de direcionamento (43 tarefas) | 2 | docs/trilha1/materiais | Pronto |
| Vídeos (tutoriais, trailers, institucional, série por objeção) | 24 arquivos | docs/trilha1 | Pronto |
| Geradores (planilha, ficha, tutorial em vídeo, trailer, landing, e-book, aula) | 8 famílias | producao/ e skill zion-learning-design | Pronto |
| Exercícios de aula ao vivo (Trilha 1, aulas 1 a 12) | 12 | projeto Lovable "Zion Dossie Aulas" | Adaptar |
| Liberação de acesso por pagamento (Asaas → ClickMax, idempotente) | 1 | projeto Lovable "Zion Hospitality Platform" | Pronto como referência |

---

## 3. Inventário curricular

### 3.1 Método Zion 360° (52 unidades: Z00 a Z02 + 7 dimensões com 7 unidades)

| Dimensão | Unidades | E-book e aula (40 slides) produzidos | Status na fila | Classificação |
|---|---|---|---|---|
| Z · Base | Z00, Z01, Z02 | Sim (3) | pronto para revisão | Adaptar (aguarda aprovação do Bruno) |
| D · Desenvolver | D00 a D06 | Sim (7) | pronto para revisão | Adaptar |
| F · Financiar | F00 a F06 | Sim (7) | pronto para revisão | Adaptar |
| E · Implantar | E00 a E06 | Não | pendente | Estrutura |
| M · Marca e Experiência | M00 a M06 | Não | pendente | Estrutura |
| L · Vender | L00 a L06 | Não | pendente | Estrutura |
| G · Gerir | G00 a G06 | Não | pendente | Estrutura |
| O · Operar | O00 a O06 | Não | pendente | Estrutura |

Resumo: **17 de 52 unidades produzidas** (todas aguardando revisão do Bruno), **35 pendentes**. Gestão e Operação, as duas trilhas que a Academy quer ampliar, têm **zero unidades produzidas**.

### 3.2 ClickMax (área de membros, 11 cursos)

| Curso | Módulos | Aulas | Classificação |
|---|---|---|---|
| Trilha 1 · Transforme Seu Terreno (Marco Zero, Pilares 1 a 7, Bônus) | 9 | 58 ativas | Pronto |
| Panorama · Marco Zero (aula aberta) | 2 | 12 (10 ativas) | Pronto |
| Bônus Gestão, Operação, Aceleração de Vendas, Identidade e Branding | 1 cada | 2 a 3 cada | Pronto |
| Arquivo · Biblioteca (Z00 a Z02, D00 a D06, F00 a F06) | 18 | 36 | Adaptar (arquivada) |
| Arquivo · Trilha 2 · Gestão | 7 | 0 | Estrutura. Atenção: os 7 módulos são CAPEX, receitas, P&L, viabilidade, jurídico, capital e lançamento, ou seja, conteúdo de Financiar e não de Gestão |
| Arquivo · Trilha 3 · Operação hoteleira | 7 | 0 | Estrutura |
| Arquivo · Trilha 4 · Aceleração de vendas | 7 | 0 | Estrutura |
| Arquivo · Aula gratuita de entrada | 3 | 13 | Adaptar (arquivada) |

### 3.3 ZAIOS (4 trilhas de 7 pilares)

| Trilha | Pilares construídos | Pilares só planejados |
|---|---|---|
| Desenvolvimento e Captação | P1, P2, P3, P5, P6 | P4, P7 |
| Gestão | G1, G2, G3 | G4 a G7 |
| Operação | nenhum | O1 a O7 |
| Aceleração de Vendas | V1, V2 | V3 a V7 |

Observação: três estruturas diferentes usam nomes parecidos para coisas diferentes ("Trilha 2 · Gestão" no ClickMax é Financiar; "G" no Método 360° é Gerir; "G" na ZAIOS também é Gestão, mas com outros recortes). A matriz abaixo resolve isso.

---

## 4. Matriz de equivalência (42 assuntos × Método 360° × ZAIOS × ClickMax)

Regra adotada: o **Método 360°** é a referência pedagógica; a **ZAIOS** organiza a navegação e a aplicação; os **42 assuntos** são a matriz de cobertura. Nada substitui as 52 unidades.

### 4.1 Desenvolvimento (10 assuntos)

| Assunto | Unidade 360° | Pilar ZAIOS | ClickMax | Conteúdo existente | Ferramenta | Falta | Prioridade |
|---|---|---|---|---|---|---|---|
| Planejamento da jornada | Z00, Z01, Z02, D00 | Porta de entrada | T1 Marco Zero; Panorama | E-books e aulas Z00 a D00; Marco Zero | Ficha Marco Zero | Aprovação dos e-books | Média |
| Terreno e território | D01 | P1 | T1 Pilar 1 | E-book D01; e-book do Pilar 1; aulas | P1; ficha aula1; B05 | Aprovação | Baixa |
| Análise de mercado | D02 | P2 | T1 Pilar 2 | Idem | P2; ficha aula2 | Aprovação | Baixa |
| Produto | D03 | P3 | T1 Pilar 3 | Idem | P3; ficha aula3; B07 | Aprovação | Baixa |
| Conceito e modelo de negócio | D04, D05 | P4 | T1 Pilares 4 e 5 | E-books D04, D05; aulas | Fichas pilar4 e pilar5; B07 | Pilar P4 na ZAIOS | Média |
| Orçamento (CAPEX) | F01 | P5 | T1 Pilar 6 (parcial); T2 Aula 1 (vazia) | E-book F01; Planilha 1 | P5; B06 | Aula no ClickMax | Baixa |
| Viabilidade | F02, F03 | P6 | T1 Pilar 6; T2 Aulas 2 a 4 (vazias) | E-books F02, F03; Planilha 2 | P6 Receitas e Viabilidade; A09; B08 | Aulas no ClickMax | Baixa |
| Investimento e captação | F04, F05, F06 | P7 | T1 Pilar 7; T2 Aula 6 (vazia) | E-books F04 a F06; Kit do Investidor | B01, B02, B04, B10 | Pilar P7 na ZAIOS | Média |
| Jurídico e Land Bank | D06 | Linha de corte de P4 e P7 | T2 Aula 5 (vazia) | E-book D06 | Nenhuma | Checklist de documentos (catálogo 04) | Média |
| Implantação | E00 a E06 | O1 Pré-opening (planejado) | Nenhum | Nenhum | B09 (planejador progressivo) | Unidades E inteiras | Alta |

### 4.2 Gestão (16 assuntos)

| Assunto | Unidade 360° | Pilar ZAIOS | ClickMax | Existente | Ferramenta | Falta | Prioridade |
|---|---|---|---|---|---|---|---|
| Planejamento estratégico | G00, G01 | G1, G5 | Nenhum | Nenhum | G1 Maturidade | E-book e aula | Alta |
| Administração | G03, G05 | G5 | Nenhum | Nenhum | Nenhuma | E-book, matriz de delegação | Alta |
| Finanças | G04, F04 | G2 | Bônus Gestão | E-book F04 (parcial) | G2; A03; Planilha Diária Mínima | E-book G04 | **Alta (módulo do protótipo)** |
| Controladoria | G04 | G2, G3 | Nenhum | Nenhum | G2, G3 | Fechamento mensal, conciliação | Alta |
| Reservas | L03 | G4 | T4 Aula 5 (vazia) | Nenhum | A07 | E-book L03 | Média |
| Revenue management | L05, F04 | G3, V6 | T4 Aula 4 (vazia) | Nenhum | A02; G3 | E-book, calendário de preço | Alta |
| Vendas | L01, L02 | V1, V5 | T4 Aula 3 (vazia) | Nenhum | A01, A04, A07; V1 | E-book | Média |
| Marketing | L05, M01 | V2, V3, V5 | T4 Aula 6 (vazia) | Nenhum | V2; A04 | E-book | Média |
| Pessoas e RH | G02 | O2, O3 | T3 Aula 4 (vazia) | Nenhum | Nenhuma | E-book, descrições de cargo | Alta |
| Compras | G03 | O5 | T3 Aula 6 (vazia) | Nenhum | Catálogo 15 (a fazer) | Comparador de fornecedores | Média |
| Estoques | G03, O05 | O5 | Nenhum | Nenhum | Enxoval 13 | E-book | Média |
| Manutenção | O05 | O5 | Nenhum | Nenhum | Ocorrências 14 | E-book, plano preventivo | Média |
| Alimentos e bebidas | O04 | O6 | Nenhum | Nenhum | Nenhuma | Tudo | Baixa (público inicial é pequeno) |
| Qualidade | G06 | O7, G3 | Nenhum | Nenhum | A06 Auditor | E-book, auditoria interna | Média |
| Tecnologia | L03 | G4 | T4 Aula 5 (vazia) | Nenhum | Nenhuma | Mapa de sistemas | Média |
| Conformidade | G01, E01 | Linha de corte (T4) | Nenhum | Nenhum | Nenhuma | Checklist de exigências | Média |

### 4.3 Operação (16 assuntos)

| Assunto | Unidade 360° | Pilar ZAIOS | ClickMax | Existente | Ferramenta | Falta | Prioridade |
|---|---|---|---|---|---|---|---|
| Reservas | O02 | O4 | T3 (vazia) | Nenhum | A07 | POP de reserva | Alta |
| Pré-chegada | O02, M04 | O6 | Nenhum | Nenhum | Kit de Mensagens 11 | POP | Alta |
| Check-in | O02 | O4 | Nenhum | Nenhum | Kit 11 (parcial) | POP e checklist | Alta |
| Atendimento | O02 | O4 | Nenhum | Nenhum | A07 | POP de recuperação de serviço | Alta |
| Check-out | O02 | O4 | Nenhum | Nenhum | Kit 11 | POP | Alta |
| Governança (arrumação) | O03 | O5 | Nenhum | Nenhum | Checklist de Limpeza 17 | E-book O03 | **Alta (checklist do protótipo)** |
| Lavanderia | O03 | O5 | Nenhum | Nenhum | Enxoval 13 | POP | Média |
| Inspeção | O03 | O5 | Nenhum | Nenhum | Checklist 17 | — | Média |
| Manutenção preventiva | O05 | O5 | Nenhum | Nenhum | Ocorrências 14 (parcial) | Plano preventivo | Média |
| Manutenção corretiva | O05 | O5 | Nenhum | Nenhum | Ocorrências 14 | POP | Média |
| Recebimento | O05 | O5 | Nenhum | Nenhum | Nenhuma | POP | Baixa |
| Almoxarifado | O05 | O5 | Nenhum | Nenhum | Enxoval 13 (parcial) | Controle de estoque mínimo | Baixa |
| Alimentos e bebidas | O04 | O6 | Nenhum | Nenhum | Nenhuma | Tudo | Baixa |
| Áreas externas | O03, O05 | O5 | Nenhum | Nenhum | Nenhuma | Checklist | Baixa |
| Segurança | O05 | O1, O5 | Nenhum | Nenhum | Nenhuma | Checklist (com linha de corte para bombeiros) | Média |
| Pós-estadia | O02, L04 | V7 | Nenhum | Nenhum | A06 | POP de avaliação e recompra | Média |

### 4.4 Identidade e Vendas (transversal, preservada)

Unidades M00 a M06 (Marca e Experiência) e L00 a L06 (Vender): todas pendentes. Na ZAIOS: V1 e V2 prontos; V3 a V7 planejados. No ClickMax: Trilha 4 com 7 módulos vazios e o bônus Identidade e Branding (A04, A05). A identidade própria da ZAIOS (logo, narrativa) também está anotada para depois do MVP.

---

## 5. Lacunas principais

1. **Gestão e Operação não têm conteúdo didático**: as 14 unidades G e O do Método 360° estão pendentes, e as trilhas 2 e 3 do ClickMax estão vazias.
2. **Implantação (E00 a E06)** não tem conteúdo e é a ponte entre Desenvolver e Operar.
3. **POPs e manuais operacionais** não existem; só há checklists e planilhas soltas.
4. **Os 17 e-books produzidos aguardam revisão** do Bruno; nenhum pode ser tratado como aprovado.
5. **Fichas e mini mentorias guardam resultados só no aparelho**; a ZAIOS resolve isso para os pilares que já tem.
6. **ZAIOS sem P4, P7 e sem a trilha de Operação.**
7. **Nomes conflitantes** entre as três estruturas (seção 3.3).

---

## 6. Materiais a produzir, em ordem

Critério: maior lacuna para o público inicial (aluguel por temporada, cabanas, glampings e pequenas pousadas), reaproveitando a fábrica.

1. **Revisão e aprovação dos 17 e-books já produzidos** (Z, D, F). Não custa produção; destrava a Trilha 1 completa na Academy.
2. **G04 Fechamento financeiro e gestão financeira** (e-book + aula), ligado ao G2 e à Planilha Diária Mínima. É o módulo demonstrativo do protótipo.
3. **O03 Limpeza, arrumação e lavanderia** + POPs de arrumação e inspeção, ligados ao Checklist 17 e ao Enxoval 13.
4. **O02 Recepção, reservas e atendimento** + POPs de pré-chegada, check-in, check-out e recuperação de serviço, ligados ao Kit de Mensagens 11.
5. **L05 Marketing digital, preço e sazonalidade**, ligado ao A02 Precificador e ao G3.
6. **G00 a G03 e G05, G06** (completar Gerir).
7. **O00, O01, O05, O06** (completar Operar), incluindo o Manual Operacional.
8. **E00 a E06** (Implantar).
9. **M e L restantes** (Identidade e Vendas).
10. **O04 Alimentos e bebidas** (por último, pelo público inicial).

Cada unidade nova segue o padrão já aprovado: e-book com ECROI na abertura e no fechamento, aula de 40 slides, ferramenta ou checklist, exercício e avaliação. Nada duplicado: se a ferramenta já existe, a unidade aponta para ela.

---

## 7. Componentes reutilizáveis

| Componente | De onde | Uso na Academy |
|---|---|---|
| Login, membros, permissões, consentimento | ZAIOS | O mesmo aluno, sem novo cadastro |
| Pilares, jornada, progresso | ZAIOS | Navegação das trilhas |
| Motor de exercícios e cálculo | ZAIOS | Exercícios e avaliações das aulas |
| G2 Finanças | ZAIOS | Ferramenta do módulo de Gestão |
| Dossiê em PDF com versões | ZAIOS | Relatório final do módulo |
| Pendências e Plano de Melhoria | ZAIOS | "O que fazer depois da aula" |
| E-books HTML e aulas de 40 slides | docs/escola | Leitor de e-book e aula |
| Vídeos | docs/trilha1 | Visualizador de vídeo |
| Checklist de Limpeza 17 | producao/utilitarios | Checklist do protótipo (convertido em checklist interativo) |
| Identidade oficial (cores, Cormorant, Aventa, logo) | ZAIOS | Já aplicada |

---

## 8. Arquitetura da Academy dentro da ZAIOS

Princípio: **a Academy ensina, as ferramentas aplicam, o ClickMax vende, a ZAIOS conecta.** Uma conta, um membro, um progresso.

Estrutura nova (entidades):
- **Trilha**: Desenvolvimento, Gestão, Operação (+ Identidade e Vendas transversal).
- **Módulo**: ligado a uma ou mais unidades do Método 360° e a um pilar da ZAIOS.
- **Aula**: tipo (vídeo, e-book, ferramenta ZAIOS, checklist, POP, exercício, avaliação), ordem, duração, fonte.
- **Progresso da aula**: membro, aula, status, data.
- **Matriz de equivalência**: unidade 360° ↔ pilar ZAIOS ↔ módulo ClickMax ↔ assunto.
- **Permissão por produto** (preparada para a integração da Fase 6, sem ligar ainda).

Navegação: Início da Academy → Painel do aluno (o que estudar e o que aplicar) → Trilhas → Módulo → Aula (vídeo, e-book, exercício) → "Aplicar no meu empreendimento" (abre o pilar da ZAIOS já ligado ao empreendimento) → Relatório.

Conteúdo: vídeos e e-books continuam hospedados onde já estão (GitHub Pages e ClickMax); a Academy só aponta e registra o progresso. Nada de duplicar arquivos.

---

## 9. Escopo mínimo do protótipo (Fase 5)

Em uma **cópia isolada (remix) da ZAIOS**, com banco próprio, sem credenciais de produção e sem integrações:
1. Página inicial da Academy.
2. Painel do aluno.
3. Três trilhas visíveis (Desenvolvimento com conteúdo real da Trilha 1 apontado; Gestão e Operação com o catálogo planejado marcado "em produção").
4. Catálogo de módulos (a partir da matriz).
5. **Um módulo demonstrativo de Gestão: "Finanças da operação"** com aula (visualizador de vídeo e leitor de e-book com conteúdo fictício identificado), exercício, **G2 reaproveitado**, **checklist operacional** (a partir do Checklist 17) e **relatório em PDF**.
6. Registro de progresso por aula.
Tudo com "dados fictícios".

Antes de começar o remix, conferir que a cópia não compartilha banco, segredos nem integrações com a ZAIOS publicada.

---

## 10. Créditos e dependências

| Item | Estimativa |
|---|---|
| Remix e conferência de isolamento | 1 a 3 créditos |
| Estrutura da Academy (trilhas, módulos, aulas, progresso, navegação) | 6 a 10 |
| Módulo demonstrativo (aula, G2 ligado, checklist, relatório) | 5 a 8 |
| Correções após revisão | 2 a 4 |
| **Total** | **14 a 25 créditos** |

Saldo aproximado: 28 créditos. Cabe, mas sem folga para imprevistos; decidir recarga só depois de aprovar o escopo.

Dependências: aprovação desta matriz; aprovação do formato (Academy dentro da ZAIOS, protótipo em cópia); resultado do teste fechado (Fase 1), porque falhas encontradas lá têm prioridade; texto do e-book demonstrativo (pode ser fictício no protótipo).

---

## 11. Plano futuro da integração ClickMax (Fase 6)

Conferido na documentação oficial do ClickMax (08/11/2026). Não presumir que está pronto.
- **Webhooks de saída** (ClickMax → ZAIOS): SALE_MADE (compra e renovação), REFUND_MADE, SALE_CANCELLED, SUBSCRIPTION_STARTED, SUBSCRIPTION_CANCELLED, REFUSED_CARD, TRANSACTION_FAILED, PIX_OR_BOLETO_EXPIRED_OR_OVERDUE, CHARGEBACK_REQUESTED. Autenticação por token fixo no cabeçalho cm-token; o corpo não traz o nome do evento (uma URL por evento); até 3 tentativas; desativa após 15 falhas; idempotência por transactionId. Não há evento de "compra pendente" nem de "conciliação".
- **API pública v0** (ZAIOS → ClickMax): chave do workspace só no servidor; 100 requisições a cada 10 segundos; versão instável. Uso: gravar progresso do aluno como tags e campos do lead; consultar transações para conciliação.
- **MCP** (OAuth): só para agentes de IA.
- Sequência: liberação e revogação de acesso → histórico e permissões por produto → progresso no lead → conciliação periódica → botões "Fazer no ZAIOS" nas aulas.
- Bloqueio atual: conta de vendedor em análise; nenhum checkout vende. Testes de compra só com o botão de teste do webhook.

---

## 12. Decisões pendentes de aprovação do Bruno

1. Aprovar o roteiro do teste fechado (seção 1) e executá-lo.
2. Aprovar a matriz de equivalência (seção 4), inclusive o 10º assunto de Desenvolvimento (Jurídico e Land Bank).
3. Renomear a "Trilha 2 · Gestão" do ClickMax, que na prática é Financiar (decisão de nomenclatura; nada será mudado no ClickMax sem aprovado).
4. Prioridade de produção (seção 6), começando pela revisão dos 17 e-books já produzidos.
5. Aprovar o escopo do protótipo (seção 9) e autorizar o remix.
6. Confirmar o módulo demonstrativo: "Finanças da operação" (Gestão).
7. Recarga de créditos: decidir depois do item 5.
8. Pendências antigas: e-mail de contato nos Termos, revisão jurídica, e-mail automático de acesso, validação das fórmulas versão 0 e da metodologia F01 a F03.
