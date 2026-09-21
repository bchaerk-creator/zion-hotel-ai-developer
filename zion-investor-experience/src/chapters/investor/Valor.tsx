import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { DataTable } from "@/components/DataTable";
import { platform } from "@/lib/data";
import { brl } from "@/lib/format";

const nature = { "one-off": "Uma vez", annual: "Ao ano", none: "Sem fee" };

export function Valor() {
  const r = platform.remunerationPerSite;
  const v = platform.valuation;
  const o = platform.organization;
  return (
    <Chapter id="valor" number="19" title="Zion e valor" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="19" title="Zion e valor" />
        <Statement text="O que a Zion ganha, às claras." support={`${r.note} A Zion não participa do lucro da SPE e não aporta produto em espécie. O custo de fabricação da Store é reservado.`} />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <DataTable
            caption={`Remuneração da Zion por sede, ${r.scope.toLowerCase()}`}
            columns={[{ key: "label", label: "Fonte" }, { key: "value", label: "Valor", align: "right" }, { key: "nature", label: "Natureza" }]}
            rows={r.fees.map((f) => ({ _key: f.id, label: f.label, value: f.value === 0 ? "R$ 0" : brl(f.value), nature: nature[f.nature] }))}
            sourceId={r.sourceId}
            status="estimate"
          />
          <div>
            <DataTable
              caption={`Valor estimado dos braços, ${v.method.toLowerCase()}`}
              columns={[{ key: "label", label: "Braço" }, { key: "today", label: "Hoje", align: "right" }, { key: "mat", label: "Na maturidade", align: "right" }]}
              rows={v.arms.map((a) => ({ _key: a.id, _total: a.id === "platform", label: a.label, today: a.today ?? "", mat: a.maturity }))}
              sourceId={v.sourceId}
              status={v.status}
            />
            <p className="t-table mt-4" style={{ color: "var(--muted)" }}>{v.note}</p>
          </div>
        </div>
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <div>
            <DataTable
              caption="Cluster de vice-presidências compartilhadas"
              columns={[{ key: "label", label: "VP" }, { key: "cost", label: "Custo anual", align: "right" }, { key: "c", label: "Collection", align: "right" }, { key: "s", label: "Store", align: "right" }, { key: "m", label: "Management", align: "right" }]}
              rows={[
                ...o.cluster.map((x) => ({ _key: x.id, label: x.label, cost: brl(x.annualCost), c: x.allocation.collection ? `${x.allocation.collection}%` : "", s: x.allocation.store ? `${x.allocation.store}%` : "", m: x.allocation.management ? `${x.allocation.management}%` : "" })),
                { _key: "total", _total: true, label: "Total maduro", cost: brl(o.matureTotal), c: "", s: "", m: "" },
              ]}
              sourceId="org-plan"
              status="estimate"
            />
            <p className="t-table mt-4" style={{ color: "var(--muted)" }}>{o.principle} Custo do cluster por fase, com equipe e terceirizados: {o.costByPhase.map((c) => `${brl(c.cost)} até ${c.sitesUpTo} sedes`).join(", ")}.</p>
          </div>
          <div>
            <DataTable
              caption="Margem da operadora por escala"
              columns={[{ key: "label", label: "Sedes" }, { key: "value", label: "Margem", align: "right" }]}
              rows={platform.management.margins.map((m) => ({ _key: String(m.sites), label: `${m.sites} sedes`, value: m.margin }))}
              sourceId="org-plan"
              status="estimate"
            />
            <ul className="t-support mt-8" style={{ color: "var(--fg-2)" }}>
              {platform.management.governance.map((g) => (
                <li key={g} className="border-t py-3" style={{ borderColor: "var(--line)" }}>{g}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </Chapter>
  );
}
