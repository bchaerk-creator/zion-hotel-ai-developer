# Zion Hotel Academy · Arsenal Interativo 01 · Seu Airbnb Está Vazio?

Projeto isolado (não altera o site institucional, funis, Land Bank, Collection, checkouts, Asaas ou ClickMax).
Status: Bloco 01 (telas 01 a 08) em validação. Não publicado comercialmente.

- `src/app.html` – telas e interface (fragmento com marcadores `{{...}}`)
- `src/logic.js` – cálculos e motor de feedback, sem dependências (roda no navegador e no Node)
- `src/img/` – fotos reais da Zion Bubble Glamping usadas nas telas
- `build.py` – gera `dist/index.html`, autocontido (fontes, logo, fotos e lógica embutidos; jsPDF via cdnjs)
- `tests/logic.test.js` – 32 testes de fórmulas, cenários A/B/C e casos de borda: `node tests/logic.test.js`
- `tests/e2e.js` – 28 verificações de ponta a ponta no navegador (Playwright): `node tests/e2e.js <saida> <jspdf.umd.min.js>`

Privacidade: respostas salvas só no `localStorage` do aparelho do aluno; nada é enviado a servidores; nenhuma senha é pedida.
