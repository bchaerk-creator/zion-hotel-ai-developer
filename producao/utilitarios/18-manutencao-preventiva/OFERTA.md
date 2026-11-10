# Ferramenta 18 · Planner de Manutenção Preventiva

Status: arquivos prontos e testados. Nada publicado nem anunciado (rodada diária automática, 09/11/2026).

**ClickMax (rascunhos):** produto `ec984b9b-8282-49ea-9155-89cd63214868`; oferta `a7beacee-6e6a-458a-aff4-6d7a62a4f94a` (R$ 19, checkout `9EgkyYXxs_`; pendência: `sellerStatus`); página `5c8911fb-ab5d-4c81-be8e-b9f5dcc3c560` em `/manutencao-preventiva` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/manutencao-18/`, ligados à oferta.

**Por que a 18 e não a 01 ou a 21 nesta rodada:** em 09/11 Bruno aprovou a arquitetura comercial (Comando 05A/05B: promessas sem duplicação). A 01 (ficha de apresentação do terreno) se sobrepõe a B05, B10 e ao Dossiê do Land Bank; a 21 (mensagens de reservas) à A07. A 18 preenche uma lacuna registrada na auditoria (`docs/zaios/AUDITORIA_ACADEMY_ZAIOS.md`: manutenção preventiva sem ferramenta, só a 14 parcial) e é uma das ferramentas do e-book E08. A 01 e a 21 ficam para depois da decisão de Bruno.

## 1. Tarefa concreta
Montar e seguir um plano de manutenção preventiva: o que conferir, de quanto em quanto tempo, quem faz, quando foi a última vez, o que está atrasado e quanto custa por ano.
- **Base Zion:** Manual Técnico e Manutenção (Bíblia Operacional, Notion): ronda diária de 8 itens (hidromassagem, pH e cloro, aquecimento, ar-condicionado, iluminação, bombas, deck, área externa) e a regra de não liberar a hidromassagem sem medir pH. A copy diz que **a ronda diária sugerida parte da rotina usada nas unidades da Zion** (verdadeiro; autorização de 06/11). As demais tarefas são genéricas.
- **Evidência:** item 18 do Catálogo; lacuna O05 na auditoria da Academy. Nenhuma pesquisa de mercado nova; nenhuma frequência apresentada como regra (todas como "ponto de partida").

## 2. Promessa
"Aprenda o passo a passo para montar um plano de manutenção preventiva da sua hospedagem: o que conferir, de quanto em quanto tempo, quem faz e o que está atrasado."
Tempo para começar: cerca de 30 minutos para ajustar a lista e anotar as últimas datas. Resultado externo (menos defeitos) não depende só da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Manutencao-Preventiva-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Plano (120 linhas, 21 tarefas sugeridas, data de hoje com HOJE()), Registro (400 linhas) e Painel |
| `Manutencao-Preventiva-Zion-EXEMPLO.xlsx` | Hospedagem fictícia com 3 áreas e 16 tarefas, hoje = 15/11/2026: 2 atrasadas, 4 em breve, 9 em dia, 1 sem registro; custo anual R$ 4.731,38 |
| `Ficha-de-Ronda-Preventiva.pdf` | Ronda diária da semana (7 dias) e tarefas feitas, para imprimir |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 3 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Próximas tarefas e de Painel com valores calculados |
| `Ferramenta18-Manutencao-Preventiva-Zion.zip` | Pacote completo |

Regras: intervalo = dias da frequência (Diária 1 … Anual 365) ou os dias informados; última vez = máximo entre a data anotada no Plano e as do Registro para aquele nº; próxima = última + intervalo; dias = próxima − hoje; situação: Escolha a frequência, Sem registro, Informe a data de hoje, Data futura, Atrasada (< 0), Vence em breve (≤ aviso), Em dia; custo anual = custo por vez × 365 ÷ intervalo. Registro: Informe a data, Nº não existe no Plano, Data futura, OK. Painel: contagens, mais urgente, custo anual e leitura.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **31 de 31**. Cada linha do Plano (intervalo, última vez, próxima, situação, custo anual, dias), cada linha do Registro e os 10 resultados do Painel comparados com uma conta independente em Python: exemplo, versão em branco, 10 cenários aleatórios com erros, 5 cenários aleatórios limpos (até 100 tarefas e 150 registros) e 10 casos de borda (vazio, sem frequência, dias personalizados, registro mais recente e mais antigo, data futura, limite do aviso, sem data de hoje, registro sem data e nº inválido, tudo em dia). Exemplo conferido à mão. Nenhuma célula com erro em 27 arquivos.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular.
**Não testado:** Excel e Google Sheets reais (SUMPRODUCT(MAX(...)) e HOJE() funcionam no LibreOffice); celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "O problema aparece quando o hóspede chega?"
- **Colapso de crença:** "eu lembro quando precisa" não funciona: cada item tem o seu tempo e a memória falha.
- **Reencadramento:** de consertar quando quebra para conferir antes, com data.
- **Inevitabilidade:** lista + frequência + responsável + registro = você vê o atrasado antes do hóspede.
- **Resultado educacional:** você aprende a montar o plano, registrar e ler o painel semanal.
Botão: "Quero o planner" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho; não promete Club, Land Bank, Mentoria nem ZAIOS (Comando 05A).

## 6. Perguntas frequentes
Frequências são ponto de partida. · Não substitui profissionais, vistorias nem laudos. · Serve para uma casa ou várias (até 120 tarefas). · Conserto vai para um quadro de ocorrências. · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta18`)
1. **c18a · Quando o hóspede chega:** "O problema aparece quando o hóspede chega?" + tela Próximas tarefas. Primeira linha: "Filtro, detector, calha, gás: quando foi a última vez?"
2. **c18b · Painel:** tela Painel (2 atrasadas, dados fictícios). Primeira linha: "Toda semana, veja o que passou da data e comece por ali."
3. **c18c · Ronda:** ficha de ronda. Primeira linha: "A ronda diária que parte da rotina das unidades da Zion, pronta para imprimir."

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
