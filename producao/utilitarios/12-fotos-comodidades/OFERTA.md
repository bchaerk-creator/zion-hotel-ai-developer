# Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio

Status: arquivos prontos e testados; **oferta enviada para aprovação em 14/11/2026** (rodada diária automática). Página em rascunho; será publicada quando a oferta estiver ativa.

**ClickMax:** produto `d2c18a5d-04e6-4b61-b7c2-881001227801`; oferta `1651f122-ea41-417d-abb1-2838c6b793d3` (R$ 19, checkout `BduC1TgySd`, status `pending` desde 14/11 04h54 UTC, sem erro de sincronização); página `ee0a4b0e-4381-44ba-a6d0-7400b9c38e9f` em `/fotos-comodidades` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/fotos-12/`, ligados à oferta.

**Por que a 12 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno; E05 e E06 dependem da liberação dos PDFs A01 a A10 (PENDENCIAS_BRUNO.md, item 5). A 12 é a ferramenta mais antiga da lista ainda "A fazer".
**Sobreposição verificada:** o Arsenal 01 e a Zion Collection 06 ("Seu Airbnb Está Vazio?") diagnosticam a oferta inteira (onde o hóspede para, sete notas, prioridades) e citam fotos e comodidades só como hipótese a investigar; nenhum dos dois traz lista de fotos para fotografar nem conferência casa × anúncio (`grep` em `producao/zion-collection/06-airbnb-vazio/ebook/conteudo` e no Arsenal). A 12 é de execução: o que fotografar, a situação de cada foto e o que corrigir nas comodidades. O guia diz que o diagnóstico do anúncio inteiro é outro produto. Nenhuma alegação de que vem da rotina das unidades da Zion e nenhuma regra de plataforma apresentada como fato.

## 1. Tarefa concreta
Planejar as fotos do anúncio (por ambiente, obrigatórias marcadas), acompanhar cada uma até a publicação com a ordem certa e conferir, andando pela casa, se cada comodidade existe, está marcada no anúncio e tem foto.
- **Evidência:** item 12 do Catálogo (E05 e E09). Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para planejar as fotos do seu anúncio, acompanhar cada uma até a publicação e conferir se o que está marcado no anúncio existe de verdade na hospedagem."
Tempo para começar: cerca de 30 minutos para ajustar a lista e responder as comodidades. Reservas dependem também de preço, localização, avaliações e calendário.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Fotos-Comodidades-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Fotos (18 sugeridas, até 60), Comodidades (29 sugeridas, até 60) e Painel |
| `Fotos-Comodidades-Zion-EXEMPLO.xlsx` | Chalé fictício: 14 fotos, 5 de 7 obrigatórias prontas, 4 publicadas, 2 com a mesma ordem; comodidades: 1 para remover (ar-condicionado), 3 para marcar, 3 sem foto, 1 sem resposta, 16 OK |
| `Roteiro-do-Dia-das-Fotos.pdf` | Lista para levar no dia, com caixas e dicas (1 página) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Fotos e Casa × anúncio |
| `Ferramenta12-Fotos-Comodidades-Zion.zip` | Pacote completo |

Regras (Fotos, primeira que se aplica): Descreva a foto; Diga se é obrigatória; Confira a ordem (texto, menor que 1 ou não inteira); Ordem repetida; Publicada sem ordem; Obrigatória ainda não aprovada (obrigatória fora de Aprovada/Publicada); OK. Situação em branco conta como Falta tirar.
Comodidades: Responda (existe ou marcada em branco); Remover do anúncio (não existe e está marcada); Marcar no anúncio (existe e não está marcada); Não se aplica; Falta foto (precisa de foto e não tem); OK.
Painel: contagens e "o que fazer primeiro" na ordem remover → alertas de fotos → marcar → falta foto → sem resposta → lista vazia → pronto.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **23 de 23**. O alerta de cada foto, a situação de cada comodidade, as 11 contagens do Painel e a leitura "o que fazer primeiro" comparados com uma regra independente em Python: exemplo, versão em branco, 8 cenários aleatórios com erros, 4 cenários aleatórios limpos (até 40 fotos e 45 comodidades) e 6 casos de borda (tudo pronto, só falta marcar, só falta foto, publicada sem ordem, ordem tripla, lista vazia), cobrindo todos os ramos da leitura. Nenhuma célula com erro em 20 arquivos.
Revisão visual do guia, do roteiro, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais; celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "O anúncio mostra o que a casa tem?"
- **Colapso de crença:** "fotos e comodidades eu resolvo de memória" — é assim que sobra o ar-condicionado que saiu e falta a lareira.
- **Reencadramento:** de fotografar e marcar de improviso para uma lista e uma conferência andando pela casa.
- **Inevitabilidade:** lista de fotos + situação + casa × anúncio = o hóspede encontra o que viu.
- **Resultado educacional:** você aprende a planejar fotos, acompanhar até publicar e conferir as comodidades.
Botão: "Quero o checklist" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A).

## 6. Perguntas frequentes
Não precisa de fotógrafo. · Não mexe no anúncio. · Serve para qualquer plataforma (lista é ponto de partida). · Foto não garante reserva. · Funciona no celular.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta12`)
1. **c12a · O que a casa tem:** "O anúncio mostra o que a casa tem?" + tela Casa × anúncio (dados fictícios). Primeira linha: "Comece por tirar do anúncio o que não existe."
2. **c12b · Dia das fotos:** "Faltou o banheiro na sessão de fotos?" + roteiro. Primeira linha: "Uma lista para levar no dia das fotos."
3. **c12c · Ordem:** tela de Fotos com ordem repetida. Primeira linha: "Cada foto, de falta tirar até publicada."

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
14/11/2026 (rodada diária): 4 arquivos e página de acesso conferidos no ar (status 200) e ligados à oferta; `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`, sem erro de sincronização.
