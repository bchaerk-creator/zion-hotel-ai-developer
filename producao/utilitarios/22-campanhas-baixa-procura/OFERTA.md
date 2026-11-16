# Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Procura

Status: arquivos prontos e testados; **oferta enviada para aprovação em 15/11/2026** (rodada diária automática). **Oferta aprovada e página publicada em 16/11/2026.**

**ClickMax:** produto `e9a5c19f-134e-495c-84f9-6bb5bbf7caf5`; oferta `b34854f5-1848-4596-ac9c-e592090db377` (R$ 19, checkout `DVd1Z5pOef`, status `pending` desde 15/11 04h53 UTC, sem erro de sincronização); página `e23ecfe2-8ea0-4120-9232-8491fa061b86` em `/campanhas-baixa-procura` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/campanhas-22/`, ligados à oferta.

**Por que a 22 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno; E05 e E06 aguardam os PDFs A01 a A10. A 22 é a próxima ferramenta "A fazer" da lista (E09).
**Sobreposição verificada:** o bump da Zion Collection 06 (Calendário comercial de 30 dias) é um roteiro diário para melhorar o anúncio; não planeja campanhas por período nem confere piso (`producao/zion-collection/06-airbnb-vazio/bump/acoes.py`). A Ferramenta 01 (Diária Mínima) calcula o piso; a 22 usa o piso como trava e indica a 01 como produto separado. Nenhuma alegação de que vem da rotina das unidades da Zion; nenhuma regra de plataforma apresentada como fato.

## 1. Tarefa concreta
Encontrar os períodos que costumam ficar vazios, medir a ocupação de cada um contra uma meta do próprio anfitrião, planejar campanhas com antecedência sem vender abaixo do piso e registrar o que cada campanha trouxe.
- **Evidência:** item 22 do Catálogo. Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para encontrar os períodos fracos da sua hospedagem, planejar campanhas sem vender abaixo do piso e acompanhar o que cada campanha trouxe."
Tempo para começar: cerca de 20 minutos para preencher a base e listar os períodos. Reservas dependem também de preço, anúncio, localização e avaliações. Faturamento não é lucro.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Base, Períodos (20), Campanhas (60) e Painel |
| `Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx` | 3 chalés fictícios, diária R$ 420, piso R$ 300, meta 50%: 4 períodos (3 abaixo da meta, 1 sem campanha), 6 campanhas (2 com alerta: última hora a R$ 273 abaixo do piso; tema especial começa depois do período), 14 noites vendidas, R$ 5.628 de faturamento bruto atribuído |
| `Ficha-de-Campanha.pdf` | Uma página para pensar cada campanha antes de lançar |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Períodos e Campanhas |
| `Ferramenta22-Campanhas-Baixa-Procura-Zion.zip` | Pacote completo |

Regras: noites disponíveis = (último dia − primeiro dia + 1) × unidades; ocupação = reservadas ÷ disponíveis; situação do período: Confira as datas, Preencha a aba Base (unidades ausentes ou menores que 1), Informe as noites reservadas, Reservadas maior que disponíveis, Defina a meta, Abaixo da meta, Na meta ou acima. Campanha: diária com desconto = diária × (1 − desconto); líquido por noite = diária com desconto × (1 − taxas) − custo da estadia ÷ estadia mínima (vazia = 1); alerta na ordem Período não cadastrado, Escolha o tipo, Preencha a aba Base, Confira o desconto (0% a 99%), Confira a estadia mínima, Confira as datas, Abaixo do piso, Não cobre o custo, Termina antes do período, Começa depois do período, OK. Faturamento bruto atribuído = noites vendidas × diária com desconto (só campanhas OK).

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **27 de 27**. Situação da base, as 5 colunas de cada período, alerta, diária, líquido e faturamento de cada campanha, as 9 linhas do Painel e a leitura "o que fazer agora" comparados com uma regra independente em Python: exemplo, versão em branco, 8 cenários aleatórios com erros, 4 limpos e 8 casos de borda (piso exato, não cobre o custo, estadia mínima diluindo o custo, termina antes, tudo coberto e no ar, planejadas sem nada no ar, sem períodos, período de um dia). Contas do exemplo conferidas à mão (420 × 0,65 = 273; 357 × 0,82 − 120 ÷ 3 = 252,74). Nenhuma célula com erro em 22 arquivos. **Falha real encontrada e corrigida:** com 0 unidades na Base, a ocupação dividia por zero; agora o período pede "Preencha a aba Base".
Revisão visual do guia, da ficha, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais; celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Calendário vazio nos mesmos meses?"
- **Colapso de crença:** "no período fraco, o jeito é baixar o preço na última hora" — às vezes a estadia nem paga a limpeza.
- **Reencadramento:** de reagir na última semana para planejar com antecedência e trava no piso.
- **Inevitabilidade:** períodos × meta + campanha com piso + registro do resultado = o que funcionou se repete no ano seguinte.
- **Resultado educacional:** você aprende a encontrar os períodos fracos, escolher o tipo de campanha, proteger o preço e medir o que trouxe.
Botão: "Quero o planner" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A); cita a Planilha Diária Mínima como produto separado.

## 6. Perguntas frequentes
Sem piso, confere só o custo (calcule com a Diária Mínima). · Não garante reservas. · Não publica campanhas; contato só com autorização. · Serve para uma casa (1 unidade). · Funciona no celular.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta22`)
1. **c22a · Mesmos meses:** "Calendário vazio nos mesmos meses?" + tela de Períodos (dados fictícios). Primeira linha: "Planeje o período fraco antes de ele chegar."
2. **c22b · Piso:** "Desconto abaixo do piso?" + tela de Campanhas com o alerta. Primeira linha: "A planilha confere antes de ir para o ar."
3. **c22c · Tipos:** "Estadia longa, pacote, público da região." Primeira linha: "Desconto não é a única saída."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos + página de acesso. Manutenção baixa.
Indicadores: visitas à página, conversão do checkout, reembolsos, custo por venda (quando houver anúncio aprovado).

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
15/11/2026 (rodada diária): 4 arquivos e página de acesso conferidos no ar (status 200) e ligados à oferta; `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`, sem erro de sincronização.

## Publicação (16/11/2026)
Oferta aprovada (`status` approved, sem erro de sincronização). Página publicada; 404 no primeiro minuto e meio (propagação), depois status 200 com título, reembolso e capa: https://infoprodutos-zion.clickmax.space/campanhas-baixa-procura. O checkout é um iframe bloqueado neste ambiente, então a compra não foi testada.
