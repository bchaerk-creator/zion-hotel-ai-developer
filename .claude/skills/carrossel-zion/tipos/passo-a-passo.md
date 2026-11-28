# Tipo: passo a passo (8 slides)

**Objetivo:** salvamento (lista e passo a passo são o que as pessoas guardam).

## Estrutura
| # | Papel | O que entra | Visual (`visual.tipo`) |
|---|---|---|---|
| 1 | Capa | Promessa + resultado em N passos + "Arrasta pro lado." | nenhum |
| 2 | Jeito antigo | Dor do método antigo e o jeito novo em uma frase | nenhum |
| 3 | Passo 1 | Primeira decisão, com a regra de escolha | `tabela` |
| 4 | Passo 2 | O que pedir, com os parâmetros | `chat` (print do prompt) |
| 5 | Passo 3 | O que pedir em seguida | `lado` (resultado ao lado da conversa) |
| 6 | Passo 4 | Como finalizar/exportar | `pasta` (arquivos gerados) |
| 7 | Resultado | O que a pessoa leva, em uma frase | nenhum |
| 8 | CTA | "Salva pra..." + "comenta PALAVRA que eu te mando ... no direct." | nenhum |

Máximo de 30 palavras por slide. Um passo por slide. Capa e CTA sem visual.

## `slides.json`
```json
{
  "marca": "Zion Collection · Bruno Chaerk",
  "tema": "texto curto da pasta",
  "slides": [
    {"papel": "capa", "kicker": "Passo a passo", "titulo": "...", "texto": "..."},
    {"papel": "texto", "kicker": "O jeito antigo", "titulo": "...", "texto": "..."},
    {"papel": "passo", "kicker": "Passo 1", "titulo": "...", "texto": "...",
     "visual": {"tipo": "tabela", "colunas": ["Objetivo", "Tipos"], "linhas": [["Alcance", "Opinião forte, notícia"]]}},
    {"papel": "passo", "kicker": "Passo 2", "titulo": "...", "texto": "...",
     "visual": {"tipo": "chat", "legenda": "Exemplo de prompt", "texto": "..."}},
    {"papel": "passo", "kicker": "Passo 3", "titulo": "...", "texto": "...",
     "visual": {"tipo": "lado", "esquerda": "Conversa", "direita": "Carrossel", "legenda": "..."}},
    {"papel": "passo", "kicker": "Passo 4", "titulo": "...", "texto": "...",
     "visual": {"tipo": "pasta", "nome": "carrossel", "arquivos": ["slide-01.png"]}},
    {"papel": "texto", "kicker": "O resultado", "titulo": "...", "texto": "..."},
    {"papel": "cta", "kicker": "Salva e comenta", "titulo": "...", "texto": "..."}
  ],
  "legenda": "texto do post"
}
```
