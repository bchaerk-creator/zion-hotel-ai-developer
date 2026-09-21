import type { Company } from "@data/types";

type Props = { core: Company; left: Company[]; right: Company[] };

const investorLabel: Record<Company["takesInvestors"], string> = {
  never: "Nunca recebe investidor",
  yes: "Recebe investidor",
  no: "Não recebe investidor",
  "per-structure": "Recebe investidor conforme estrutura",
};

function Arm({ c }: { c: Company }) {
  return (
    <div className="border-t py-5" style={{ borderColor: "var(--line)" }}>
      <p className="t-subtitle !text-[clamp(22px,2vw,28px)]">{c.name}</p>
      <p className="t-table mt-2" style={{ color: "var(--fg-2)" }}>{c.role}</p>
      <p className="mt-2 text-[12px]" style={{ color: "var(--muted)" }}>{c.remuneration}. {investorLabel[c.takesInvestors]}.</p>
    </div>
  );
}

/** Três colunas: braços à esquerda e à direita, núcleo ao centro com moldura dourada fina. */
export function EcosystemDiagram({ core, left, right }: Props) {
  return (
    <div className="grid gap-10 md:grid-cols-[1fr_1.1fr_1fr] md:items-center">
      <div>{left.map((c) => <Arm key={c.id} c={c} />)}</div>
      <div className="border border-gold p-8 md:p-10">
        <p className="t-label mb-4">Núcleo</p>
        <p className="t-subtitle">{core.name}</p>
        <p className="t-table mt-4" style={{ color: "var(--fg-2)" }}>{core.role}</p>
        <p className="mt-3 text-[12px]" style={{ color: "var(--muted)" }}>{core.remuneration}. {investorLabel[core.takesInvestors]}.</p>
      </div>
      <div>{right.map((c) => <Arm key={c.id} c={c} />)}</div>
    </div>
  );
}
