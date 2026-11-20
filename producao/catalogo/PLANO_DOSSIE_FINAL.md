# Plano · Dossiê final do curso "Transforme seu terreno em um destino turístico"

Status: **para aprovação de Bruno. Nada foi produzido nem alterado.** (20/11/2026)

## 1. O que já existe (conferido nos arquivos)
- Fichas "Faça agora" que salvam no aparelho do aluno: Marco Zero, Território (aula 1), Mercado, Produto, e Pilares 4, 5, 6 e 7 (`docs/trilha1/`).
- **Pilar 7 · "O seu Dossiê de Desenvolvimento"** (`docs/trilha1/pilar7/`): já lê as fichas anteriores no aparelho, mostra "as sete páginas, lado a lado", pontos fortes, ponto mais frágil, decisão, 90 dias, compromisso de 7 dias, e exporta PDF (jsPDF).
- Planilhas em branco e com exemplo: Orçamento de Abertura (CAPEX orientativo: Premissas, Infraestrutura, FF&E, OS&E, Resumo) e Estudo de Massas e Viabilidade.
- Kit do Investidor: modelo de pitch deck (.pptx) e de teaser/one-pager (.docx).
- Correção: na conversa de 20/11 eu disse que não havia dossiê único; **há uma versão no Pilar 7**. O que falta está na seção 2.

## 2. Lacunas (a confirmar na auditoria da Fase 1)
1. O CAPEX da planilha Orçamento de Abertura **não entra** no dossiê: o aluno preenche a planilha à parte.
2. Não há capa e acabamento "documento para levar a sócio/investidor" (identidade Zion, índice, página de premissas e avisos).
3. Não há seção "Caminhos para o capital" (sócio, parceria, financiamento) comparada lado a lado, com os números do aluno.
4. O dossiê vive só no aparelho do aluno: se trocar de celular, perde. Não há versão guardada na conta.
5. Não há análise por IA. O "mentor virtual" do Pilar 7 é regra programada, não IA (confirmar na auditoria).

## 3. O que o dossiê final entrega (proposta)
PDF "Seu projeto, do terreno ao investimento", com:
1. Capa e índice (logo oficial, cores Zion).
2. Resumo de uma página: terreno, vocação, tipologia, fases, o que construir primeiro.
3. Território e mercado (da ficha, sem dado inventado).
4. Modelo de negócio e masterplan faseado.
5. **CAPEX orientativo**: totais do Orçamento de Abertura (aluno importa um arquivo ou digita os totais por bloco), com "dados do aluno, não da Zion".
6. Pré-viabilidade com premissas explícitas e o ponto mais frágil.
7. **Caminhos para o capital**: sócio, parceria com proprietário e financiamento com garantia, com prós, contras e "o que preparar" de cada um. Sem promessa de aprovação.
8. Plano de 30 e de 90 dias, perguntas em aberto e próximos passos.
9. Aviso final fixo: material educativo; não garante reservas, ocupação, renda, crédito, captação nem valorização; não substitui advogado, engenheiro, contador, estudo ambiental, licença ou alvará.

## 4. Decisões que preciso de você
- **A. Escopo**: (1) só evoluir o Pilar 7 existente, com CAPEX e capital (recomendado, menor risco); (2) criar página nova separada.
- **B. IA**: (1) sem IA, por regras e textos prontos, grátis e previsível (recomendado agora); (2) com IA, exige conta/chave e tratamento de dados pessoais: fica para uma segunda etapa.
- **C. Guardar na conta**: (1) não, só no aparelho + PDF (recomendado agora); (2) sim, exigiria banco de dados e login.
- **D. Próxima reunião** (decidido por Bruno em 20/11): usar a agenda pública do ClickMax, a mesma do Pilar 7, com UTM `utm_source=dossie&utm_medium=pdf&utm_campaign=reuniao`. Ficam de fora o Calendly antigo e `diagnostico/agendar/`.

## 5. Fases e entregas
- **Fase 1 · Auditoria (somente leitura)**: ler Pilar 6 e 7 e planilhas, mapear campos e lacunas. Entrega: lista de campos e o que falta.
- **Fase 2 · Lógica testada**: cálculo e regras do dossiê em `src/logic*.js`, testadas em Node. Entrega: resultado dos testes.
- **Fase 3 · Interface e PDF**: nova versão do Pilar 7 em pasta nova, sem mexer na atual. Revisão visual no celular. Entrega: prévia e PDF de exemplo com dados fictícios, marcado como tal.
- **Fase 4 · Teste de ponta a ponta com Playwright**: preencher as fichas, gerar o PDF e conferir o conteúdo.
- **Fase 5 · Publicação** (só com "aprovado"): trocar a aula no ClickMax, registrar em OFERTA.md e no MAPA_DAS_SESSOES.

## 6. Riscos e limites
- Cálculos usam só números do aluno; exemplos marcados "dados fictícios".
- Sem foto gerada por IA como se fosse real; fotos reais Zion só na capa, com legenda.
- Dados pessoais: ficam no aparelho do aluno; nada é enviado a servidor.
- O curso já está à venda; mudar a aula do Pilar 7 só entra depois de testado, para não quebrar o acesso de quem comprar.
- Tempo: estimativa só depois da Fase 1.
