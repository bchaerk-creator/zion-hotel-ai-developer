# Harness de auditoria para os testes próprios da ZAIOS (vitest)

Não contém código da ZAIOS. Para usar:
1. Copie a pasta `src/` de uma cópia local da ZAIOS (fora deste repositório) para junto deste arquivo, sem `src/components` e `src/integrations`.
2. Instale `vitest@4.1.10` (e `@vitest/coverage-v8@4.1.10` para a cobertura) com `npm install --legacy-peer-deps`. Sem essa opção, o npm 10.9 falha com o erro "edgesOut".
3. Rode `npx vitest run --config vitest.config.mjs`.

Adaptações do ambiente, documentadas:
- **Ambiente `node`** em vez do `jsdom` da configuração original. Os testes executados não usam DOM.
- **Componentes de interface (`@/components/*`)** substituídos por `stubs/componente.ts`. Os testes executados validam cálculo e dados, não telas.
- **Cliente Supabase (`@/integrations/supabase/*`)** substituído por `stubs/supabase.ts`, que lança erro se for usado. Assim nenhum teste depende de serviço externo sem que isso apareça.
- **Os arquivos de teste não foram alterados.**
