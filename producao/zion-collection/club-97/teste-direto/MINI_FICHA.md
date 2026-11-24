# Mini-ficha ANTES do pagamento (3 perguntas)

Rascunho local, 24/11/2026. Nada foi criado no ClickMax.

## As 3 perguntas escolhidas (das 12 do formulário do Meta)

| # | Pergunta (curta) | Campo "Forms Meta" de destino | Por que esta |
|---|---|---|---|
| 1 | O que você busca para tirar o projeto do papel? | `falta_papel_meta` | Separa direto quem precisa de capital ou parceiro de quem quer fazer sozinho. |
| 2 | Qual investimento previsto para o projeto? | `investimento` | Dá o tamanho do projeto e mostra se a conta fecha sem capital externo. |
| 3 | Quando o projeto estiver pronto, como você pretende operar? | `operador` | Separa quem quer operar, quem quer um operador e quem quer sócio. |

Leitura dos grupos: "precisa de investimento" = 1 em investimento/parceiro; "quer fazer sozinho" = 1 em conhecimento ou mentoria; "outros" = o resto.

## Opções de resposta (múltipla escolha, sem texto livre)

1. `falta_papel_meta` (opções que já existem no Meta e já aparecem nos leads, então batem com a base):
   - Investimento ou capital para o projeto
   - Um parceiro para desenvolver comigo
   - Mentoria de quem já opera
   - Conhecimento para fazer sozinho
2. `investimento` (faixas que já aparecem no Meta, confirmadas em dois leads: "R$ 400 mil a R$ 1 milhão" e "R$ 1 milhão a R$ 3 milhões"; as demais são sugestão a conferir no formulário do Meta):
   - Até R$ 150 mil
   - R$ 150 a 400 mil
   - R$ 400 mil a R$ 1 milhão
   - R$ 1 a R$ 3 milhões
   - Acima de R$ 3 milhões
3. `operador` (as opções do Meta não estão nos arquivos; sugestão, conferir antes de criar):
   - Eu mesmo(a) vou operar
   - Quero contratar um operador
   - Quero um sócio operador
   - Ainda não sei

Cuidado: o texto das opções precisa ser igual ao que o Meta grava, para o mesmo campo não ficar com dois jeitos de escrever a mesma resposta.

## Como entra na página (duas formas, por ordem de preferência)

A) Formulário do ClickMax embutido na mesma página, acima do bloco de checkout (`forms_create`, 3 campos de escolha, mapeados para os campos "Forms Meta" acima). O botão "FAÇA A SUA INSCRIÇÃO" leva ao formulário; depois dele vem o checkout. É o caminho mais curto para o lead.

B) Se o formulário não puder ficar na mesma página: botão que abre o formulário (página própria de formulário) e que, ao enviar, redireciona para a página curta já na âncora `#pagar`. Perde mais gente (um passo a mais).

Observação sobre a página curta atual: ela não tem formulário. Se a opção A valer, o formulário entra em `<section data-cx-section="offer">` entre o selo e o checkout; isso só se faz depois de confirmar abaixo.

## O que a documentação confirma e não confirma

Não consegui consultar a documentação pública: `docs.clickmax.io` não resolve a partir desta sessão (o domínio não está liberado na rede do ambiente). Também não há cópia da documentação no repositório, e as ferramentas `mcp__clickmax__*` estão sem conexão. Portanto:

- Confirma: nada, por esta fonte.
- Não confirma, e precisa ser verificado: (1) se um formulário do ClickMax pode ser embutido na mesma página de vendas antes do `data-cx-checkout`; (2) se o checkout aceita pré-preenchimento (nome, e-mail, telefone) por parâmetro de URL ou pelo lead já criado pelo formulário; (3) se o envio do formulário pode redirecionar para `#pagar`; (4) se as regras de HTML da página (`pages_validate_html`) aceitam o bloco de formulário.
- Pendência de ação: liberar `docs.clickmax.io` na rede da sessão, ou refazer a consulta numa sessão com o ClickMax conectado (`pages_generation_context_get` e a skill do ClickMax dizem o que a página aceita). Não invento nada além disso.
