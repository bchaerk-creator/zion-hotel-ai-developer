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
- Edição para investidores em `/investor`, com data room em `/investor/documents`, atrás de um código de acesso.

## Código de acesso da edição para investidores

```
node scripts/access-code.mjs "seu-codigo"      # imprime o hash SHA-256
NEXT_PUBLIC_INVESTOR_CODE_HASH=<hash> npm run build
```

Só o hash entra no build, nunca o código. Sem a variável, a página mostra "acesso ainda não configurado".

Limite honesto da Fase 1: o site é estático, então o conteúdo da edição para investidores está no
código-fonte da página mesmo antes de digitar o código. O bloqueio evita o acesso casual e a indexação
(`noindex`), não substitui proteção real. Para um deploy de teste com dados reais, ative a proteção por
senha do host (Vercel Password Protection ou Cloudflare Access) na rota `/investor`. O login por NDA com
conteúdo servido só a quem assinou é a Fase 3.

## Regras que o código garante

- Nenhum número vive em componente. Tudo vem de `data/*.json`, com fonte, período e status.
- A edição pública não importa os arquivos marcados `investorOnly` (model, capex, raise, returns).
- `scripts/validate-data.mjs` falha se aparecer termo proibido, fonte desconhecida ou aritmética que não fecha.
