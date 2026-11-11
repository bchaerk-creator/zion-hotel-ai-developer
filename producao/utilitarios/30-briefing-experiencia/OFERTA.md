# Ferramenta 30 · Gerador de Briefing de Experiência

Status: arquivos prontos e testados; **oferta enviada para aprovação em 11/11/2026** (rodada diária automática). Página em rascunho; será publicada quando a oferta estiver ativa.

**ClickMax:** produto `ba7395b4-56d6-455b-ae7c-82575f9a6274`; oferta `f28b840b-cd7d-457f-bff5-6fd6636212e2` (R$ 19, checkout `IO3t7_0ZHV`, status `pending` desde 11/11 04h58 UTC, sem erro de sincronização); página `7531d1b2-1f19-44f3-a3ad-7d87c9b0911f` em `/briefing-experiencia` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/briefing-30/`, ligados à oferta.

**Por que a 30 nesta rodada:** o próximo da fila era o e-book E08 (Gestão e operação), mas ele se sobrepõe à Jornada 2 (Gestão) da Fábrica Educacional; Bruno decide (PENDENCIAS_BRUNO.md). A 30 completa a linha de experiências junto com a 29 (custos), sem sobreposição com Club, Land Bank ou Mentoria.

## 1. Tarefa concreta
Escrever uma vez as informações de uma experiência (passeio, café, trilha, aula) e, para cada saída, ter prontos a descrição, as mensagens ao cliente e o briefing de quem conduz, com o dia de enviar cada uma.
- **Base:** mesma mecânica de textos da Ferramenta 11 (Kit de Mensagens). Nenhuma alegação de que vem da rotina das unidades da Zion.
- **Evidência:** item 30 do Catálogo (E10). Nenhuma pesquisa de mercado nova.

## 2. Promessa
"Aprenda o passo a passo para escrever o briefing da sua experiência uma vez e gerar, a cada saída, a descrição, as mensagens ao cliente e o briefing de quem conduz."
Tempo para começar: cerca de 20 minutos para preencher a ficha da experiência. O resultado externo (lotação, avaliações) não depende só da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Briefing-Experiencia-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Ficha (experiência + saída, situação do mínimo) e Mensagens (B01–B08 com data de envio e aviso do que falta) |
| `Briefing-Experiencia-Zion-EXEMPLO.xlsx` | Experiência fictícia "Café da manhã na trilha do mirante", saída em 12/12/2026, 5 pessoas, mínimo 4: 8 de 8 textos prontos, "Mínimo atingido" |
| `Mensagens-Modelo-Experiencia.pdf` | Os 8 modelos com campos para completar (1 página) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: passos, exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas da ficha e das mensagens |
| `Ferramenta30-Briefing-Experiencia-Zion.zip` | Pacote completo |

Regras: cada texto junta segmentos fixos (campo vazio vira `[PREENCHA: rótulo]`), opcionais (só entram com todos os campos) e de campo vazio; data de envio: logo, data−2 (B03/B04), data−1 (B05/B06), data (B08) ou sob demanda (B07); situação da saída: preencha a data, preencha mínimo e participantes, precisam ser números, mínimo atingido (B03) ou abaixo do mínimo (B04).

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **27 de 27**. Cada texto, data de envio e a situação da saída comparados com uma regra independente em Python nos cenários completo, só obrigatórios, falta "o que levar", abaixo do mínimo, sem data, aspas e texto longo (maior mensagem 1.077 caracteres), vazio e exemplo; nenhuma célula com erro. Uma falha corrigida: número digitado como texto fazia o mínimo sempre "atingido" (agora `VALUE()` com proteção).
Revisão visual do guia, dos modelos, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais; celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Toda saída, a mesma explicação de novo?"
- **Colapso de crença:** mandar tudo de cabeça, cada vez, faz faltar alguma coisa.
- **Reencadramento:** de mensagens soltas para uma ficha única que gera tudo.
- **Inevitabilidade:** ficha + dados da saída + data de envio = cliente e guia sabem o mesmo.
- **Resultado educacional:** você aprende a escrever o briefing, conferir o mínimo e enviar cada texto no dia.
Botão: "Quero o gerador de briefing" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A).

## 6. Perguntas frequentes
Serve para passeios, trilhas, cafés, aulas e vivências. · Não verifica segurança, seguro nem autorizações. · Não envia mensagens sozinha. · Um arquivo por experiência. · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta30`)
1. **c30a · Mesma explicação:** "Toda saída, a mesma explicação de novo?" + tela Mensagens. Primeira linha: "Escreva uma vez, use em toda saída."
2. **c30b · Quem conduz:** tela do briefing B06 (dados fictícios). Primeira linha: "O guia sabe da restrição do grupo antes de chegar?"
3. **c30c · Mínimo:** tela da ficha com "Mínimo atingido". Primeira linha: "Confirmar ou remarcar: a planilha diz qual mensagem usar."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos + página de acesso. Manutenção baixa.
Indicadores: visitas à página, conversão do checkout, reembolsos, custo por venda (quando houver anúncio aprovado).

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```
