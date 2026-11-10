# Ferramenta 14 · Quadro de Ocorrências e Manutenção

Status: arquivos prontos e testados. Nada publicado nem anunciado (rodada diária automática, 07/11/2026).

**ClickMax (rascunhos):** produto `24e847f2-3c5c-4426-a148-7409eba0a56d`; oferta `74460a23-4459-4b82-8d45-70d683d02002` (R$ 19, checkout `sdDDSurhAZ`; pendência: `sellerStatus`); página `feb343db-8860-4bbf-891c-e6b359e37ea0` em `/quadro-ocorrencias` (rascunho). Entrega por arquivo e página de acesso em `docs/p/adbc67069af26ae0/ocorrencias-14/`.

## 1. Tarefa concreta
Registrar cada problema da hospedagem com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede.
- **Base real Zion:** Manual Técnico e Manutenção (Notion, Bíblia Operacional): ronda diária e "deixar problema sem avisar" como erro proibido. Generalizado; nada específico das bubbles.
- **Evidência pública:** reinspecionar depois da manutenção e padronizar o status da unidade são práticas recomendadas em governança (item E7 do Mapa de Oportunidades, fontes SiteMinder e SafetyCulture, consultadas em 06/11/2026). **Hipótese:** problemas avisados por mensagem se perdem; não temos número sobre isso.

## 2. Promessa
"Aprenda o passo a passo para registrar cada problema com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede."
Tempo para começar: cerca de 10 minutos (prazos, unidades, responsáveis). Resultado externo (problemas resolvidos a tempo) depende de quem resolve.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Ajustes (prazo por prioridade, editável), Cadastros, Ocorrências (500 linhas), Painel |
| `Quadro-Ocorrencias-Zion-EXEMPLO.xlsx` | Hospedagem fictícia com 4 unidades e 6 ocorrências (data de referência 07/11/2026) |
| `Ficha-de-Ronda.pdf` | Ronda básica de 8 itens + espaço para anotar problemas |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Painel e Ocorrências com valores calculados |
| `Ferramenta14-Quadro-Ocorrencias-Zion.zip` | Pacote completo |

Regras: prazo = digitado ou abertura + dias da prioridade; Atrasada = aberta com prazo antes da data de referência (hoje por padrão); "Complete os dados" sem unidade, prioridade, responsável ou data; "Fechada sem descrição" quando falta como foi resolvido; "Confira as datas" quando resolvida antes de aberta; unidade BLOQUEADA com ocorrência aberta marcada como bloqueio. Os prazos por prioridade (0, 2, 7 e 30 dias) são ponto de partida editável, não norma.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **13 de 13**, de primeira. Prazo usado, situação e dias de cada ocorrência e o painel por unidade (abertas, atrasadas, bloqueando, fechadas, custo, situação) comparados com uma regra independente em Python no exemplo e em 6 cenários aleatórios (até 25 ocorrências, com campos faltando, datas invertidas e prazos digitados); totais do painel do exemplo; data do painel sem a função TEXTO (independe do idioma do Excel); versão em branco; nenhuma célula com erro em 8 arquivos.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular.
**Não testado:** Excel e Google Sheets reais; uso no celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "O problema foi avisado. Alguém resolveu?"
- **Colapso de crença:** avisar no grupo não é o mesmo que ter alguém responsável e um prazo.
- **Reencadramento:** de "depois a gente vê" para "quem, até quando, e a unidade pode receber hóspede?".
- **Inevitabilidade:** uma linha por problema + prazo automático + painel = nada some.
- **Resultado educacional:** você aprende a priorizar, delegar com prazo e liberar a unidade com critério.
Botão: "Quero o meu quadro" · Público: Airbnb, casas, apartamentos, pousadas e glampings · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
Serve para apartamento? Sim. · Avisa sozinha? Não. · Prazos fixos? Não, editáveis. · Diz como consertar? Não; segurança segue profissional habilitado. · Celular? Pelo app do Google Sheets ou Excel.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta14`)
1. **c14a · Sem dono:** "O problema foi avisado. Alguém resolveu?" + tela Ocorrências. Primeira linha: "Cada problema com responsável, prioridade e prazo."
2. **c14b · Bloqueada:** tela Painel com "BLOQUEADA". Primeira linha: "Saiba quais unidades não podem receber hóspede antes da entrada."
3. **c14c · A ronda:** Ficha de Ronda. Primeira linha: "Uma ronda simples e um lugar único para anotar o que encontrar."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos ligados à oferta + página de acesso. Manutenção baixa.

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
10/11/2026 (rodada diária): `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`. O ClickMax devolveu erro de sincronização do gateway ("Não autorizado. Token inválido ou ausente."); registrado em PENDENCIAS_BRUNO.md. Página segue em rascunho até a oferta ficar ativa.
