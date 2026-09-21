import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { DataTable } from "@/components/DataTable";
import { returns } from "@/lib/data-investor";

export function Retorno() {
  return (
    <Chapter id="retorno" number="18" title="O retorno" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="18" title="O retorno" />
        <Statement text="No conservador sem saída, a Zion rende menos que a Selic." support="Dizer isso faz parte da credibilidade. O retorno vem da operação no plano e da saída a múltiplo de EBITDA, não de premissa otimista." />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <DataTable
            caption="Por sede de 12 unidades, ano 1"
            columns={[{ key: "label", label: "Cenário" }, { key: "y", label: "Yield sobre capital", align: "right" }, { key: "m", label: "Múltiplo em 7 anos", align: "right" }, { key: "c", label: "Ciclo de retorno do capital", align: "right" }]}
            rows={returns.perSite.map((s) => ({ _key: s.id, label: s.label, y: s.yieldOnCapital, m: s.multiple7y, c: s.capitalReturnCycle }))}
            sourceId={returns.sourceId}
            status="estimate"
          />
          <DataTable
            caption="Comparação em 7 anos"
            columns={[{ key: "label", label: "Alternativa" }, { key: "m", label: "Múltiplo", align: "right" }, { key: "irr", label: "TIR", align: "right" }]}
            rows={returns.comparison.map((r) => ({ _key: r.id, _total: r.isBenchmark, label: r.label, m: r.multiple7y, irr: r.irr }))}
            sourceId={returns.sourceId}
            status="estimate"
          />
        </div>
        <p className="t-support mt-12" style={{ color: "var(--fg-2)" }}>Cenários são hipóteses e não representam resultado futuro. Saída a 6x EBITDA é premissa de modelagem, não compromisso.</p>
      </div>
    </Chapter>
  );
}
