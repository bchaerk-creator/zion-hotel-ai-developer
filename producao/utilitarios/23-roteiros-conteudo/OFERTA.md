# Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos

Status: arquivos prontos e testados; **oferta enviada para aprovação em 16/11/2026** (rodada diária automática). **Oferta aprovada e página publicada em 17/11/2026.**

**ClickMax:** produto `74ea712d-8186-4011-9bd7-76af916ef87b`; oferta `b0f2a1e3-424b-424d-a00b-74284182f210` (R$ 19, checkout `ujYWp_XYpj`, status `pending` desde 16/11 04h53 UTC, sem erro de sincronização); página `cc7b6b14-5777-42ed-a708-4a39770c3836` em `/roteiros-conteudo` (publicada em 17/11). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/roteiros-23/`, ligados à oferta.

**Por que a 23 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno; E05 e E06 aguardam os PDFs A01 a A10. A 23 é a próxima ferramenta "A fazer" (E09).
**Sobreposição verificada:** os criativos da Zion Collection 06 são anúncios do próprio produto da Zion, não roteiros para o anfitrião gravar a hospedagem dele. A 23 usa a mecânica de textos das Ferramentas 11 e 30 (campo vazio vira [PREENCHA], opcionais somem). Nenhuma alegação de que vem da rotina das unidades da Zion e nenhuma regra de rede social apresentada como fato.

## 1. Tarefa concreta
Transformar o que diferencia a hospedagem em 8 vídeos curtos (15 a 30 s) com gancho, cenas, texto na tela, legenda e chamada, e num calendário de postagem que o anfitrião consegue manter.
- **Evidência:** item 23 do Catálogo. Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para preencher uma ficha da sua hospedagem e receber 8 roteiros curtos de vídeo, com gancho, cenas, texto na tela, legenda e o dia de postar cada um."
Tempo para começar: cerca de 15 minutos para preencher a ficha. Seguidores, alcance e reservas não dependem só dos roteiros.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Roteiros-Conteudo-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Ficha (13 campos da hospedagem + calendário), Roteiros (8, com data e situação) e Modelos |
| `Roteiros-Conteudo-Zion-EXEMPLO.xlsx` | Hospedagem fictícia "Refúgio do Vale": 8 de 8 roteiros prontos, um vídeo a cada 3 dias de 01/12 a 22/12/2026 |
| `Roteiros-Modelo.pdf` | Os 8 roteiros com campos entre colchetes, para usar sem planilha (2 páginas) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de um roteiro e do calendário |
| `Ferramenta23-Roteiros-Conteudo-Zion.zip` | Pacote completo |

Roteiros: V01 Tour de 15 segundos, V02 Diferencial em destaque (cena extra se houver segundo diferencial), V03 Uma manhã aqui, V04 Pergunta que mais chega, V05 Bastidores, V06 Para quem é (e para quem não é), V07 O que fazer por perto (troca para "não sair" se o campo estiver vazio), V08 Como reservar. Data do roteiro N = data do primeiro vídeo + (N − 1) × dias entre vídeos; sem data → [PREENCHA]; intervalo não numérico ou menor que 1 → [CONFIRA]. Textos escritos sem artigo antes dos campos, para não errar concordância ("o banheira", "no Pousada").

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **31 de 31**. Os 8 roteiros, a situação e a data de cada um comparados com uma montagem independente em Python em 11 cenários: exemplo, completo, só obrigatórios, falta o cuidado, sem passeios por perto, sem data, intervalo zero, intervalo em texto, intervalo de 7 dias com virada de mês, aspas e texto longo, vazio. Nenhuma célula com erro em 11 arquivos; maior roteiro 771 caracteres. Na revisão do texto foram corrigidos erros de concordância e duas frases.
Revisão visual do guia, dos modelos, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais; celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Sabe que precisa postar, mas não sabe o quê?"
- **Colapso de crença:** "preciso de ideia criativa todo dia" — o que falta é um roteiro com o que a casa já tem.
- **Reencadramento:** de filmar no improviso para gravar cenas planejadas, com legenda pronta.
- **Inevitabilidade:** ficha + 8 objetivos + calendário = constância sem travar.
- **Resultado educacional:** você aprende a descrever o diferencial, a estrutura de um vídeo curto e a manter um calendário.
Botão: "Quero os roteiros" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A).

## 6. Perguntas frequentes
Não precisa editar vídeo. · Não garante seguidores nem reservas. · Hóspedes só com autorização por escrito. · Depois dos 8, novo ciclo. · Funciona no celular.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta23`)
1. **c23a · Não sabe o quê:** "Sabe que precisa postar, mas não sabe o quê?" + tela do roteiro (dados fictícios). Primeira linha: "Uma ficha, oito roteiros prontos."
2. **c23b · Calendário:** tela do calendário. Primeira linha: "O dia de postar cada vídeo, sem travar."
3. **c23c · Gancho:** "Os 3 primeiros segundos." Primeira linha: "Gancho, cenas, texto na tela e legenda, já escritos."

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
16/11/2026 (rodada diária): 4 arquivos e página de acesso conferidos no ar (status 200) e ligados à oferta; `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`, sem erro de sincronização.

## Publicação (17/11/2026)
Oferta aprovada (`status` approved, sem erro de sincronização). Página publicada; depois da propagação, status 200 com título, reembolso e capa: https://infoprodutos-zion.clickmax.space/roteiros-conteudo. O checkout é um iframe bloqueado neste ambiente, então a compra não foi testada.
