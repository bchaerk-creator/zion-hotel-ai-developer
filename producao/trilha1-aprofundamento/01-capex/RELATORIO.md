# Relatório · Aprofundamento 6A · CAPEX (Pilar 6)

27/11/2026 · versão 2 (coerência com a linha do curso, pedido de Bruno). Plano: `PLANO.md` v2. Guia: `../GUIA_COERENCIA.md`.

## O que mudou da versão 1
- Caso: a **Marina** (a mesma do curso inteiro), partindo da página 6 dela (R$ 690.529,18) e fechando contra o limite de R$ 870.130,80. A Helena saiu de todas as peças.
- Identidade visual da Trilha 1 (Playfair Display + Inter, verde, creme e dourado do curso), igual ao e-book e à ficha do Pilar 6.
- Nomes e pastas: `pilar6a/`, `pilar6a-aula/`, `Pilar-6A-CAPEX-*.pdf`, capas `p6a-c-*.jpg`; aulas «Aprofundamento 6A · CAPEX · …».

## Caso da Marina (exemplo ilustrativo)
CAPEX da fase R$ 791.131 · investimento total R$ 831.918,38 · folga até o limite R$ 38.212,42 · 16 de 39 linhas cotadas (41,0%), 89,1% do valor · degrau Estimador · a página 6 cobria 83,0% da 6A.

## Peças e testes (rodados de novo nesta sessão)
| Peça | Onde | Teste |
|---|---|---|
| Ficha «Faça agora · O seu CAPEX» | `docs/trilha1/pilar6a/` | 288 testes de lógica e 111 verificações e2e no iPhone 13, 0 falhas |
| Aula interativa (38 slides) | `docs/trilha1/apresentacao/pilar6a-aula/` | 380 verificações (celular e computador), 0 falhas |
| E-book (56 páginas, tamanho de letra do Pilar 6) | `docs/trilha1/materiais/Pilar-6A-CAPEX-ebook.pdf` | números conferidos por assert contra o plano; revisão visual lado a lado com o Pilar 6 |
| Checklist (2 páginas) | `docs/trilha1/materiais/Pilar-6A-CAPEX-checklist.pdf` | idem |
| Capas | `docs/trilha1/capas/p6a-c-*.jpg` | comparadas com as `p6-c-*` |
| Tutorial em vídeo | `tutorial/capex.json` | em produção (voz e formato dos tutoriais do curso: edge-tts Francisca, `producao/clube/tutoriais-video/make.py`); **Bruno aprova antes de entrar** |

## ClickMax (Trilha 1 `fa9a6c54`, módulo Pilar 6 `6e06c29d`), todas **desligadas**, entre o e-book do Pilar 6 e a Planilha 1
- `8e98bed7` Aprofundamento 6A · CAPEX · Aula interativa
- `bccdfac4` Aprofundamento 6A · CAPEX · Faça agora · O seu CAPEX
- `f1918e33` Aprofundamento 6A · CAPEX · E-book (PDF)
- `758e9b1c` Aprofundamento 6A · CAPEX · Checklist (PDF)
- (a criar) Tutorial da ficha, depois da aprovação do vídeo.

Ligar só com o "aprovado" de Bruno: o curso está em 5 turmas. A Plataforma de estruturação (R$ 97) é cópia separada e não recebeu as aulas.

## A confirmar por Bruno
- Seção 12 do `PLANO.md` (18 itens), em especial: terreno e giro fora do CAPEX; base da reserva; tabela do cap. 09 que compara a unidade pronta da página 6 com a conta cotada (ou só totais); registrar no CLAUDE.md a exceção da identidade da Trilha 1.
- E-book com 56 páginas (mesmo tamanho de letra do Pilar 6) em vez de 30 a 40.
- Pilar 6 atual: margem de referência de 40% e números da Zion Glamping Store na ficha (achado do mapa da viabilidade).
- Aula do Pilar 6 com dois defeitos (voltar ao slide; janela do apresentador), corrigidos só na 6A.
