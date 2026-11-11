# Auditoria · para onde o site manda quem procura o clube (11/11/2026)

Oferta nova: Zion Collection Club, 2x de R$ 48,50 ou R$ 97, checkout ClickMax `https://payments.clickmax.io/v_4pU5zNYj`, landing em `/zion-collection` (GitHub Pages). Ainda NÃO está dentro do zionhotelgroup.com.

## Divergências encontradas
| Onde | Hoje | Problema |
|---|---|---|
| Menu e rodapé do site ("Club Zion Collection"), Home (2 botões), Sobre, Land Bank | → `/club` → redireciona para `/land-members` | Cai na inscrição antiga: 6x de R$ 45 ou R$ 270 (Asaas), planos R$ 980 e R$ 2.900 |
| `/inscreva` | → `/club` → `/land-members` | idem |
| `/metodo` | texto "6x de R$ 45 ou R$ 270 à vista, por trilha" e link para `/land-members` | preço antigo |
| `/raio-x` | 4 botões "Conhecer o clube" → `/land-members`; a inscrição de R$ 97 do próprio raio-x aponta para o checkout Asaas antigo | mistura preço novo com checkout antigo |
| `/store` | link para `/clube` | rota não existe (página vazia) |
| Página do dossiê (`/dossie/<id>`), `/consultoria/obrigado` | oferta "Zion Land Members + Radar · 6x de R$ 45 / R$ 270" (Asaas) | preço antigo |
| `/hub` | Mentoria em grupo R$ 2.784 a R$ 9.504 (Asaas) | oferta diferente, não é o clube; fica como está |
| `/land-members` (GitHub Pages) | a página antiga do clube, R$ 270 e planos | continua no ar e indexada |

## Correção proposta (precisa de "aprovado", porque mexe no que existe)
1. **Lovable (1 mensagem ao agente, consome créditos):** criar a rota `/clube` servindo a landing nova (GitHub Pages `zion-collection/`), e fazer `/club` e `/inscreva` redirecionarem para `/clube`. Com isso menu, rodapé, Home, Sobre e Land Bank passam a cair na oferta nova sem editar cada página. Corrige também o link quebrado da `/store`.
2. **`/land-members`:** trocar a oferta de R$ 270 e os planos por um redirecionamento para `/clube` (ou manter só para quem já comprou, sem botão de compra).
3. **`/metodo` e `/raio-x` (GitHub Pages):** trocar os textos de R$ 270 e os links de `/land-members` para `/clube`; no raio-x, apontar a inscrição de R$ 97 para o checkout ClickMax.
4. **Dossiê e consultoria/obrigado (Lovable):** trocar a oferta "Land Members + Radar R$ 270" pelo clube R$ 97 com o checkout ClickMax (entra na mesma mensagem do item 1).

Sem o item 1, os anúncios funcionam (vão para o GitHub Pages), mas quem navega pelo site continua vendo R$ 270.
