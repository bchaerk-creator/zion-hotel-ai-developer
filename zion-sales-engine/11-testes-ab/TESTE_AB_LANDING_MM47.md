# Plano de teste A/B · Landing da Mini Mentoria (R$ 47)

Agente: ZION CONVERSION · 25/11/2026 · **Plano. Nada foi publicado nem ligado.** Rodar o teste exige "aprovado" de Bruno (publicar as páginas, anúncios, orçamento). Marcação: [E] evidência, [H] hipótese, [NC] não confirmado. Nenhuma taxa de conversão real aparece aqui (repositório público).

## 0. Atualização P0 de coerência (25/11/2026): o teste passa a usar as variantes v2
As variantes v1 (`/mini-mentoria-a` e `/mini-mentoria-b`) ficam como histórico e **não** entram mais no teste. O teste usa as **v2**, geradas por `07-landing-pages/mini-mentoria/comum_v2.py` (rascunhos não publicados, oferta `0c71eeba…`):
| Variante | Página (id) | Slug | Estado |
|---|---|---|---|
| A v2 | `98ef3607-d18b-4bff-924f-6a5e6897b570` | `/mini-mentoria-a-v2` | rascunho, `lastPublishedAt` null |
| B v2 | `1dba4c0f-61d4-43fa-99ec-0698dfad7a9d` | `/mini-mentoria-b-v2` | rascunho, `lastPublishedAt` null |
- **CTA padrão:** `QUERO ACESSAR A PLATAFORMA POR R$47` em todo botão que leva ao checkout. Botões anteriores à oferta só **rolam** (âncoras): na A, "VER A PLATAFORMA POR DENTRO" (topo) e "VER O QUE ESTÁ INCLUÍDO" (após as telas); na B não há botão antes da oferta.
- **Variável principal (continua única):** na **A** o preço aparece desde o topo ("Mini Mentoria de Estruturação Zion · R$47 · pagamento único") e o primeiro botão de pagamento vem junto da oferta completa; na **B** o topo não mostra preço nem botão, e o primeiro botão com preço vem só depois da oferta e dos entregáveis. Em ambas, o bloco de oferta (produto, R$47, pagamento único, sem mensalidade, 12 meses, 9 módulos, 70 aulas e materiais, garantia de 7 dias, Pix e cartão à vista) aparece **antes** de qualquer botão que leve ao pagamento.
- **Eventos:** o clique em "QUERO ACESSAR A PLATAFORMA POR R$47" é o clique qualificado (rótulo único); os cliques de rolagem têm rótulos próprios e não contam como intenção de compra. Todos usam `data-cx-cta`; separar por texto do botão no ClickMax/`09-tracking`.
- **Rótulos concorrentes:** o validador do ClickMax avisa que A usa 3 rótulos (2 de rolagem + 1 de compra). É intencional (ordem P0: botão antes da oferta não pode levar ao pagamento).
- Os critérios, a amostra e a regra de decisão das seções 1 a 7 permanecem; onde o texto abaixo cita `-a`/`-b` e `comum.py`, leia `-a-v2`/`-b-v2` e `comum_v2.py`. Pré-condição nova: Bruno confere no celular o checkout limpo (`08-checkouts/CHECKOUT_LIMPO_MM47.md`) antes de qualquer tráfego.

## 1. Hipótese e variável
- **Hipótese [H]:** quem chega por anúncio frio decide melhor depois de ver a dor, a quebra da crença, o método, a aplicação e a oferta; mostrar o botão com preço já no topo (A) pode captar quem já está decidido, mas tirar o botão do topo (B) pode aumentar a compra por visitante porque o clique ocorre com mais entendimento. A direção do efeito é **desconhecida**; o teste existe para medir, não para confirmar.
- **Variável principal (única):** posição do primeiro CTA de compra. **A:** `/mini-mentoria-a` (CTA com preço no hero). **B:** `/mini-mentoria-b` (primeiro CTA após a oferta e os entregáveis). Todo o resto é idêntico (mesmo gerador `07-landing-pages/mini-mentoria/comum.py`): copy, fotos, telas, preço, checkout, oferta `0c71eeba…`.
- Não testar junto: preço, oferta, criativo, público. Se o criativo for diferente entre A e B o teste fica inválido.

## 2. Métricas e critérios de sucesso (definidos ANTES)
| Papel | Métrica | Definição |
|---|---|---|
| **Primária** | Compras aprovadas por visitante único da página | pagamento confirmado (Pix pago ou cartão aprovado), não Pix gerado; vendas reais de clientes (excluir compras de teste de Bruno, sempre) |
| Secundária 1 | Visitante único → checkout visto | gatilho `checkout_viewed` [NC: dispara no carregamento do iframe e **infla**, usar só como tendência] |
| Secundária 2 | Pix gerado → Pix pago | `pix_generated` e `purchase_approved` |
| Guarda 1 | Reembolsos em 7 dias por compra | não pode piorar em B vs A além do acaso |
| Guarda 2 | Custo por compra aprovada (CPA) vs líquido do Pix R$ 44,51 menos imposto | variante vencedora precisa respeitar o teto; imposto = parâmetro (sem valor assumido) |
| Descartar | CTR do anúncio, cliques no botão isolados, tempo na página | não decidem |

**Regra de decisão (fixada agora):**
1. Teste só é lido ao atingir o **tamanho de amostra mínimo por variante** (seção 3) **e** o período mínimo (seção 5).
2. Uma variante vence se a diferença na métrica primária atingir 95% de confiança (teste de duas proporções, bicaudal) **e** as guardas não pioram. Caso contrário: **empate técnico**; manter a versão ao vivo atual e testar outra hipótese.
3. Vitória sem confiança, ou com poucas compras, **não** autoriza escalar nem declarar vencedora.

## 3. Tamanho de amostra
Fórmula (duas proporções, bicaudal; α = 5%, poder = 80%):
`n por variante = ( z(1−α/2)·√(2·p̄·(1−p̄)) + z(1−β)·√(p1(1−p1)+p2(1−p2)) )² / (p2−p1)²`, com `p̄ = (p1+p2)/2`, `p2 = p1·(1+efeito relativo)`.
- Parâmetros a definir por DATA antes de começar: `p1` (taxa **medida** de compra aprovada por visitante único da página no ClickMax, tráfego pago, sem tráfego de servidor/bot) e o **efeito mínimo** que valeria a pena (sugestão de partida [H]: 30% relativo).
- Ferramenta: `11-testes-ab/amostra.py` (`python3 -I amostra.py --base <taxa> --efeito-relativo 0.30`), testada em `test_amostra.py` contra a referência da própria documentação do ClickMax (base 10%, efeito 20%, 95% → 3.841 por variação [E, docs.clickmax.io/features/create/funnels/ab-test]) e contra a fórmula clássica (5%→6% ≈ 8.158).
- **Enquanto não existir taxa real:** cenários HIPOTÉTICOS (rotulados) para dimensionar orçamento e prazo, α 5%, poder 80%:

| Taxa base (hipotética) | Efeito relativo | Visitantes únicos por variante | Total |
|---|---|---|---|
| 1% | 30% | 19.827 | 39.654 |
| 2% | 30% | 9.798 | 19.596 |
| 3% | 30% | 6.455 | 12.910 |
| 5% | 30% | 3.780 | 7.560 |
| 2% | 50% | 3.826 | 7.652 |

  Leitura: com taxa baixa, o teste exige muitos visitantes; ver "O que NÃO concluir". Se o volume pago disponível não alcança o `n`, **não rodar** o A/B por compra; usar a métrica secundária só como indício e decidir por julgamento qualitativo, sem chamar de vencedora.
- Custo estimado do teste = `n total × custo por visita única` (parâmetro; preencher com o custo real medido, sem inventar).

## 4. Como dividir o tráfego (e o que é verificado)
Três caminhos, do mais para o menos confiável:
1. **Divisão no ClickMax (preferido) [H, não testado].** Teste A/B de funil: no card da página, **Fazer Teste A/B** → Variação A = `/mini-mentoria-a`, Variação B = `/mini-mentoria-b` → divisão 50%/50% (soma 100%) → URL do teste (slug `teste-ab-…`) → **Objetivo do teste = Venda na página** → deixar **Escolher a vencedora automaticamente** desligado [E, docs: "Crie um teste A/B de funil"]. Vantagem: sorteio aleatório por visitante, mesma URL para o anúncio. Requer **publicar o funil**: precisa de "aprovado" e de um funil com as duas páginas (hoje elas são páginas soltas, em rascunho). Limitação: o checkout é embutido em cada página; a venda conta na variação onde o visitante comprou [NC, a conferir no primeiro dia].
2. **Anúncios separados na mesma campanha/conjunto, mesmo criativo [E sobre o método; entrega NÃO é igual].** Duplicar cada anúncio: o do A tem destino `/mini-mentoria-a` e Tags de URL com `utm_content=<criativo>-varA`; o do B tem destino `/mini-mentoria-b` e `utm_content=<criativo>-varB`. O resto das tags é o padrão único de `09-tracking/PADRAO_UTM.md` (`utm_campaign=mm47` fixo, `utm_term={{ad.id}}`, `sck` e ids); nunca trocar `utm_campaign` entre variantes e **nunca usar `utm_term` para a variante**. **O Meta não garante 50/50** entre anúncios do mesmo conjunto: por isso a análise usa **visitantes únicos realmente recebidos por variante** (não o gasto) e confere se a distribuição de dispositivo e posicionamento é comparável. Alternativa melhor dentro do Meta: ferramenta de Experimentos (teste A/B) [NC: não verificada aqui, só leitura no Windsor; qualquer escrita no Meta exige "aprovado"].
3. **Dois conjuntos de anúncios idênticos (um por variante)** com o mesmo público e orçamento, só se o Meta Experimentos não estiver disponível. Pior controle (públicos se sobrepõem); só com orçamentos iguais.
Em todos: mesmos criativos, mesmo público, mesmo período. A venda é atribuída pelo sufixo `-varA`/`-varB` do `utm_content` (e, como segunda checagem, pelo `ad_id`, já que cada variante é um anúncio separado), gravados em `sales_get_utms` [E: campos utm gravados; **gravação de UTM na venda ainda não provada com venda real de anúncio**, ver auditoria].

## 5. Período
- **Mínimo:** 14 dias corridos (dois ciclos semanais completos; compra de infoproduto varia por dia da semana) **e** o `n` por variante atingido; o que vier por último.
- **Máximo:** 28 dias. Se não atingir `n`, encerrar como **inconclusivo** (não "vencedora por maioria").
- Congelar durante o teste: preço, oferta, criativos, público, orçamento, páginas A e B (qualquer edição reinicia a contagem), checkout, automações de pós-compra.

## 6. Critérios de parada
Parar **antes do prazo** somente se: (a) falha técnica (checkout fora do ar, página quebrada, Pix não gera, acesso não entrega), (b) violação de promessa/compliance (reclamação do anúncio, frase incompatível), (c) estouro do teto de gasto aprovado por Bruno, (d) uma variante com guarda de reembolso claramente fora do aceitável (definir limite com Bruno antes). **Não** parar por "está ganhando" no meio do teste.

## 7. O que NÃO concluir com poucos dados
- Com poucas compras (ordem de dezenas por variante), uma diferença de 2 a 3 vendas é ruído. Não declarar vencedora, não escalar, não apagar a perdedora.
- Não concluir por CTR, cliques no botão, rolagem ou `checkout_viewed` (inflado).
- Não somar compras de teste de Bruno, reembolsadas ou sem UTM; não comparar períodos diferentes entre A e B.
- Faturamento não é lucro: comparar o CPA ao líquido (Pix R$ 44,51 [E]) menos imposto e reembolsos.
- Resultado em uma fonte de tráfego (Meta frio) não vale para outra (lista, orgânico).
- Empate técnico é um resultado válido: significa "a posição do CTA não é a alavanca"; testar a próxima hipótese (por exemplo VSL no topo, ver `06-criativos/ROTEIRO_VSL.md`).

## 8. Registro
Antes de começar, copiar este plano para uma linha no `LOG.md` com data e `p1`/efeito mínimo escolhidos; ao final, registrar: visitantes únicos e compras aprovadas por variante, confiança, guardas e decisão. Dados reais ficam fora do repositório (público): guardar no scratchpad/painel e citar só o veredito.
