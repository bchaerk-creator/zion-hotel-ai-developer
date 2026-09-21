import type { Metric } from "@data/types";
import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { DataTable } from "@/components/DataTable";
import { BigNumber, BigNumberGrid } from "@/components/BigNumber";
import { Chain } from "@/components/Chain";
import { RevenueTable } from "@/components/RevenueTable";
import { brand, operations, revenue } from "@/lib/data";
import { photo, type PhotoKey } from "@/lib/photos";

function rowsFor(metrics: Metric[], context: string) {
  return metrics.filter((m) => m.context === context).map((m) => ({ _key: m.id, label: m.label, value: m.value }));
}

export function Prova() {
  const cols = [
    { key: "label", label: "Indicador" },
    { key: "value", label: "2025", align: "right" as const },
  ];
  return (
    <Chapter id="prova" number="05" title="A prova" bg="moss">
      <div className="wrap chapter">
        <ChapterLabel number="05" title="A prova" />
        <Statement text="Antes de escalar, operamos." support="Duas sedes em operação, com demonstrativo de resultado. É o que calibra cada premissa do modelo." />
        <div className="bloco grid gap-14 md:grid-cols-2 md:gap-[6vw]">
          {operations.sites.map((site) => (
            <div key={site.id}>
              <Photo photo={photo(site.photo.replace(".jpg", "") as PhotoKey)} />
              <p className="t-subtitle mt-8">
                {site.name} <span style={{ color: "var(--muted)" }}>· {site.state}</span>
              </p>
              <p className="t-table mt-2 text-sand">
                Desde {site.start} · terreno {site.land.toLowerCase()} · {site.concept.toLowerCase()} · {site.units} unidades
              </p>
              <div className="mt-6">
                <DataTable columns={cols} rows={rowsFor(operations.fy2025.metrics, site.name)} sourceId={operations.fy2025.sourceId} period={operations.fy2025.period} />
              </div>
            </div>
          ))}
        </div>
        <p className="t-support mt-12" style={{ color: "var(--fg-2)" }}>{operations.fy2025.reading}</p>
        <p className="t-support mt-4" style={{ color: "var(--muted)" }}>{operations.perimeterNote}</p>

        <div className="bloco">
          <p className="t-label mb-8">Primeiro semestre de 2026</p>
          <DataTable
            columns={[
              { key: "label", label: "Indicador" },
              { key: "uru", label: "Urubici", align: "right" },
              { key: "flo", label: "Florianópolis", align: "right" },
              { key: "cons", label: "Consolidado", align: "right" },
            ]}
            rows={["Receita bruta", "Custo variável", "EBITDA", "Margem EBITDA"].map((label) => {
              const find = (ctx: string) => operations.h12026.metrics.find((m) => m.label === label && m.context === ctx)?.value ?? "";
              return { _key: label, label, uru: find("Urubici"), flo: find("Florianópolis"), cons: find("Consolidado") };
            })}
            sourceId={operations.h12026.sourceId}
            period={operations.h12026.period}
          />
          <p className="t-table mt-6 max-w-[70ch]" style={{ color: "var(--muted)" }}>{operations.h12026.caveat}</p>
        </div>

        <div className="bloco">
          <p className="t-label mb-8">Marca</p>
          <BigNumberGrid metrics={[...brand.ratings, brand.audience[0], brand.audience[1]]} columns={4} />
          <div className="mt-12 grid gap-8 md:grid-cols-2 md:gap-[6vw]">
            <div className="grid grid-cols-2 gap-8">
              <BigNumber metric={brand.channelEconomics.metrics[0]} size="md" />
              <BigNumber metric={brand.channelEconomics.metrics[1]} size="md" />
            </div>
            <p className="t-support self-end" style={{ color: "var(--fg-2)" }}>{brand.channelEconomics.reading}</p>
          </div>
        </div>

        <div className="bloco">
          <Chain steps={revenue.timeline.map((t) => ({ number: t.step, label: t.label, note: t.note }))} />
        </div>

        <div className="bloco grid gap-12 md:grid-cols-[2fr_3fr] md:gap-[6vw]">
          <div>
            <p className="t-label mb-6">O que a Zion já faturou</p>
            <BigNumber metric={revenue.total} />
          </div>
          <RevenueTable data={revenue} />
        </div>
      </div>
    </Chapter>
  );
}
