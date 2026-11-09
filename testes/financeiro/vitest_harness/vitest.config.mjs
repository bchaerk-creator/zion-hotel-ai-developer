import path from "node:path";
import { defineConfig } from "vitest/config";
const r = (p) => path.resolve(import.meta.dirname, p);
export default defineConfig({
  test: { environment: "node", globals: true, include: ["src/test/*.test.ts"] },
  resolve: { alias: [
    { find: /^@\/components\/.*$/, replacement: r("stubs/componente.ts") },
    { find: /^@\/integrations\/supabase\/.*$/, replacement: r("stubs/supabase.ts") },
    { find: "@", replacement: r("src") },
  ] },
});
