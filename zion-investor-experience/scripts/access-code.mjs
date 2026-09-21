// Gera o hash do código de acesso da edição para investidores.
// Uso: node scripts/access-code.mjs "meu-codigo"  →  cole em NEXT_PUBLIC_INVESTOR_CODE_HASH
import { createHash } from "node:crypto";
const code = process.argv[2];
if (!code) {
  console.error("Uso: node scripts/access-code.mjs <codigo>");
  process.exit(1);
}
console.log(createHash("sha256").update(code.trim()).digest("hex"));
