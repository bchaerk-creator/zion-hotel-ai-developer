import type { Company } from "@data/types";

const investorLabel: Record<Company["takesInvestors"], string> = {
  never: "Nunca recebe investidor",
  yes: "Recebe investidor",
  no: "Não recebe investidor",
  "per-structure": "Recebe investidor conforme estrutura",
};

function Box({ c, highlight = false }: { c: Company; highlight?: boolean }) {
  return (
    <div className={`border p-6 md:p-8 ${highlight ? "border-gold" : ""}`} style={highlight ? undefined : { borderColor: "var(--line)" }}>
      <p className="t-subtitle !text-[clamp(22px,2.2vw,30px)]">{c.name}</p>
      <p className="t-table mt-2" style={{ color: "var(--fg-2)" }}>{c.role}</p>
      <p className="mt-3 text-[12px]" style={{ color: "var(--muted)" }}>
        {c.remuneration}. {investorLabel[c.takesInvestors]}.
      </p>
    </div>
  );
}

/** Caixas empilhadas ligadas por fio dourado vertical, prestadoras lado a lado embaixo. */
export function LegalStack({ stack, providers }: { stack: Company[]; providers: Company[] }) {
  return (
    <div>
      {stack.map((c, i) => (
        <div key={c.id}>
          <Box c={c} highlight={i === 0} />
          <div className="mx-auto h-12 w-px bg-gold" aria-hidden />
        </div>
      ))}
      <div className="grid gap-6 md:grid-cols-2">
        {providers.map((c) => (
          <Box key={c.id} c={c} />
        ))}
      </div>
    </div>
  );
}
