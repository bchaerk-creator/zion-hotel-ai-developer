# Zion Investor Experience

Experiência digital para investidores da Zion Hotel Group International.
Fonte única de números, decisões e identidade: `docs/MASTER.md`. Plano por fase: `docs/PLAN.md`.

## Rodar

```
npm install
npm run dev          # http://localhost:3000
npm run build        # gera o site estático em out/
npm run validate     # confere os JSON de data/ contra as regras do master
npm run typecheck
```

## Estado

- Fase 1, edição pública em português: pronta em `/`, com formulário em `/acesso`.
- Fotos: colocar os 14 arquivos de MASTER 13.4 em `public/photos/` com os mesmos nomes. Sem o arquivo, a página mostra um placeholder escuro com o nome que falta.
- Edição para investidores (`/investor`): próxima etapa, depende de aprovação e do gate por NDA.

## Regras que o código garante

- Nenhum número vive em componente. Tudo vem de `data/*.json`, com fonte, período e status.
- A edição pública não importa os arquivos marcados `investorOnly` (model, capex, raise, returns).
- `scripts/validate-data.mjs` falha se aparecer termo proibido, fonte desconhecida ou aritmética que não fecha.
