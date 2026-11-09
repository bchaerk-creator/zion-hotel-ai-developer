# Passagem · Estado atual de ZAIOS e Zion Hotel Academy

Atualizado em 09/11/2026 pela sessão "ZAIOS platform development" (Claude Code).
**Leia isto antes de fazer qualquer trabalho de ZAIOS, Academy, jornadas, ferramentas ou plano comercial**, para não refazer o que já existe.

Os documentos citados estão na `main` (copiados da branch `claude/zaios-planejamento` em 09/11/2026). O mapa de todas as sessões está em `docs/MAPA_DAS_SESSOES.md`.

---

## 1. ZAIOS (plataforma no Lovable)

- **Endereço:** https://zaios.lovable.app, publicado para teste fechado.
- **Projeto Lovable:** "Zion Empreendimentos".
- **Tecnologia:** TanStack Start + Lovable Cloud (Supabase), com segurança por linha.
- **Status:** **não validado.** O teste humano de 15 itens ainda não foi feito.
- **Créditos gastos:** 162,6.

**Funcionalidades:**
- Acesso e privacidade:
  - Entrada por link no e-mail, só para a lista de membros liberados.
  - Papéis de membro e admin.
  - Limite de tentativas no pedido de link.
  - Aceite de Termos e Privacidade (versão 0, revisão jurídica pendente).
  - Baixar e excluir os próprios dados; exportação pelo admin.
- **Jornada Desenvolvimento:** P1 Território (semáforo), P2 Mercado, P3 Produto, P5 CAPEX, P6 Receitas, P6 Viabilidade (regra de decisão em 5 passos).
- **Jornada Operação:** V1 Raio-X, V2 Posicionamento, G1 Maturidade, Plano de Melhoria, G2 Finanças, G3 Indicadores.
- Motor de exercícios: blocos, "Não sei", veredito (Avançar, Testar, Ajustar, Pausar, Redesenhar), pendências, recálculo.
- Motor de cálculo determinístico, em centavos e com origem do dado. Fórmulas em `src/calc/FORMULAS.md` no Lovable. 396 testes.
- Dossiê em PDF com versões imutáveis.
- Identidade Zion (cores, Cormorant e Aventa, logo oficial).

**Documentos:**

| Documento | Conteúdo |
|---|---|
| `docs/zaios/DECISOES.md` | Registro de todas as decisões, andamento e créditos |
| `docs/zaios/SUPER_PROMPT_ZAIOS_v2_adendo.md` | Adendo ao Super Prompt |
| `docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md` | 18 premissas financeiras (F01 a F03) com fórmulas, casos e sensibilidade, **decididas para a versão 0** (seção "Decisões tomadas"); verificação de ferramentas e vídeos; análise do G2 |
| `docs/zaios/teste/roteiro-teste-zaios.pdf` | Roteiro do teste fechado para imprimir (Bruno: 15 testes; membros: 11) |
| `docs/zaios/AUDITORIA_ACADEMY_ZAIOS.md` | Auditoria de 12 entregas (inventário, matriz de 42 assuntos, plano de integração com o ClickMax) |
| `docs/zaios/ENTREGAS_VALIDACAO_ACADEMY.md` | Roteiro de teste, lista de revisão dos 17 materiais, proposta curricular de 4 módulos |

**Decisões firmes (não reabrir sem o Bruno):**
- MVP sem IA generativa.
- Uma regra só: Academy e ZAIOS usam os mesmos nomes, indicadores e premissas.
- **Zion Score fora da ZAIOS.** Não criar segunda pontuação.
- Taxa de limpeza fora da receita de hospedagem.
- A Zion não sugere taxa de desconto; o membro informa.
- Referências financeiras editáveis: deduções 17%, quebra 1%, reserva 3%, múltiplo de saída 6×.
- Planilha por imóvel suspensa. O G2 atende em parte; ampliar só se o teste mostrar necessidade.
- Bíblia Operacional: só referência interna, anonimizada e validada.

---

## 2. Zion Hotel Academy (fábrica educacional)

| Documento | Conteúdo |
|---|---|
| `docs/academy/COMANDO_01_AUDITORIA_FABRICA.md` | Auditoria da fábrica: o que existe, agentes (2 novos, não 8), metodologia (ADDIE, Merrill, Kolb, andragogia, domínio, cognitive apprenticeship), **lição em 6 passos** (Diagnosticar → Compreender → Observar → Executar → Validar → Entregar), produção, hospedagem no ClickMax, compatibilidade com a ZAIOS, matriz de componentes |
| `docs/academy/comando-04/PLANO_REESTRUTURACAO.md` | Dores por perfil (A a E), currículo revisado das 3 jornadas, jornada de implementação de ferramentas, arquitetura ClickMax + ZAIOS, estratégia comercial, programa de 12 semanas, roadmap, decisões pendentes |
| `docs/academy/comando-04/TECH_STACK_E_FORNECEDORES.md` | Zion Tech Stack em 3 níveis com gatilhos; matriz de PMS, channel manager, WhatsApp, CRM, IA, automação e preço (preços com data e fonte) |
| `docs/academy/comando-04/PESQUISA_JURIDICA_E_MERCADO.md` | Limites jurídicos da Jornada 1 (matrícula, zoneamento, APP, Cadastur, FNRH, SCP, superfície, multipropriedade, CVM) e benchmarking |

**Achados que mudam decisões:**
1. **"Jornada R$ 270" e "Acompanhamento R$ 2.900" já existem:**
   - **Club Base R$ 270:** inclui a Trilha de Desenvolvimento, reunião, masterclass e Land Bank; é o que a Zaya vende.
   - **Club Pro / Mentoria R$ 2.900:** com acompanhamento semanal, vendido na reunião do funil em uso desde 05/11.
   - Recomendação: uma escada só, com o Club como marca e a Academy como conteúdo. **Aguarda o Bruno.**
2. **Jornadas 2 e 3 não têm conteúdo.** No ClickMax, as turmas e os produtos "Trilha 2 · Gestão", "Trilha 3 · Operação" e o Combo estão arquivados. Unidades G e O do Método 360° pendentes na `producao/fila.json`.
3. Os 17 e-books do Método 360° (Z, D, F) estão "pronto para revisão", **nenhum aprovado.**
4. Fábrica de vídeo não portátil: o gerador com Piper aponta para pastas de outra sessão. O gerador com edge-tts funciona.
5. Vídeos dos A01 a A10 trazem "Zion Collection Club" (marca das mini mentorias); a Trilha 1 já os usa como bônus.
6. **Regras novas para ensinar:**
   - FNRH Digital obrigatória desde 20/04/2026 para quem tem Cadastur.
   - Mensagens de serviço da API do WhatsApp cobradas depois de 1.000 por mês desde 01/10/2026.
   - STJ (07/05/2026): estadia curta em condomínio residencial exige 2/3 da assembleia; Tema 1.443 pendente.

**Verificações feitas (08/11/2026):**
- Planilhas 01, 11, 13, 14, 17: 109 de 109 verificações.
- Mini mentorias A01, A02, A03, A06, A07: 295 de 295.
- 5 vídeos tutoriais íntegros (720p, áudio normal).

---

## 3. Decisões pendentes do Bruno

1. Arquitetura comercial: uma escada só (recomendado) ou Academy separada.
2. Preço das Jornadas 2 e 3 para operadores.
3. Programa de 12 semanas como conteúdo do Club Pro / Mentoria; tamanho da turma; quem revisa.
4. Primeiro experimento: experiência gratuita "Venda pelo WhatsApp" (recomendado) ou piloto de Operação O03 (limpeza).
5. Advogado para revisar o módulo de estruturas de parceria.
6. Citar marcas de fornecedores nas aulas; parcerias comerciais com aviso ao membro.
7. Liberar a rede da sessão para conferir fontes primárias (planalto.gov.br, gov.br, stj.jus.br, Meta, fornecedores).

Mais as pendências antigas:
- Resultado do teste fechado da ZAIOS.
- E-mail de contato nos Termos.
- Revisão jurídica.
- Texto e remetente do e-mail de acesso.
- Aprovação da conta de vendedor no ClickMax (em análise).

---

## 4. Ciclo de trabalho combinado

GPT define → Claude executa → Claude testa → Bruno encaminha → GPT avalia → Bruno aprova → próximo comando.

**Sem autorização:**
- Não alterar produtos, preços, checkouts, automações nem a Zaya.
- Não publicar páginas.
- Não disparar mensagens.
- Não ativar anúncios.
- Não alterar a ZAIOS nem o Lovable.
- Não gastar créditos Lovable.
- Não produzir em escala.

**Próximo comando sugerido:** Comando 05, a experiência gratuita "Venda pelo WhatsApp" em rascunho local, depois das decisões 1 e 4.
