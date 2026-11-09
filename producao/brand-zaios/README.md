# ZAIOS SYSTEM · geradores do Brand Kit v1.1

Os arquivos do kit (SVG, PNG, manual) **não ficam neste repositório público** até a aprovação. Aqui ficam só os geradores.

```
python3 producao/brand-zaios/gerar_kit.py <pasta>          # SVG com texto em curvas (requer fonttools e brotli)
node producao/brand-zaios/render_png.js <pasta>            # PNG (Playwright)
python3 producao/brand-zaios/gerar_complementos.py <pasta> # paleta, contraste, tokens, favicon.ico
python3 producao/brand-zaios/gerar_manual.py <pasta>       # manual e aplicações (HTML)
node producao/brand-zaios/render_manual.js <pasta>         # manual em PDF e aplicações em PNG
```

**Fontes dos dados:**
- Símbolo: Z oficial, vetorizado de `docs/brand/zion-logo-escuro.png`.
- Tipografia: `docs/assets/fonts/aventa.woff2` (Aventa Variable).
- Paleta: proposta de referência do Bruno, de 09/11/2026.
