import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Chain } from "@/components/Chain";
import { BigNumber } from "@/components/BigNumber";
import { DataTable } from "@/components/DataTable";
import { program } from "@/lib/data";
import { raise } from "@/lib/data-investor";

export function Programa() {
  const c = program.consolidated;
  return (
    <Chapter id="programa" number="13" title="O programa" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="13" title="O programa" />
        <div className="grid gap-12 md:grid-cols-[3fr_2fr] md:gap-[6vw] md:items-end">
          <Statement text={`${program.totalDestinations} sedes até ${program.waves[program.waves.length - 1].year}.`} support={`${program.unitsPerSite} unidades por sede, uma SPE por destino. Cada onda abre depois que a anterior opera no plano. O programa se autofinancia em parte a partir da terceira onda.`} />
          <BigNumber metric={raise.programCapex} />
        </div>
        <div className="bloco">
          <Chain steps={program.waves.map((w) => ({ number: String(w.wave).padStart(2, "0"), label: String(w.year), note: w.destinations.map((d) => d.name).join(" · ") }))} />
        </div>
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <DataTable
            caption={`Programa consolidado em ${c.year}, cenário ${c.scenario === "base" ? "base" : c.scenario}`}
            columns={[{ key: "label", label: "Indicador" }, { key: "value", label: String(c.year), align: "right" }]}
            rows={[
              { _key: "sites", label: "Sedes em operação", value: String(c.sites) },
              { _key: "rev", label: "Receita", value: c.revenue },
              { _key: "res", label: "Resultado ao sócio", value: c.partnerResult },
              { _key: "margin", label: "Margem", value: c.margin },
            ]}
            sourceId={program.sourceId}
            status="estimate"
          />
          <div>
            <DataTable
              caption="Coordenação da Collection, já descontada do resultado"
              columns={[{ key: "label", label: "Escala" }, { key: "value", label: "Custo ao ano", align: "right" }]}
              rows={c.collectionCoordination.map((x) => ({ _key: String(x.sitesUpTo), label: `Até ${x.sitesUpTo} sedes`, value: x.cost }))}
              sourceId={program.sourceId}
              status="estimate"
            />
            <p className="t-table mt-4" style={{ color: "var(--muted)" }}>{c.note} A Collection não cobra fee: a estrutura é bancada pelo resultado consolidado antes da distribuição.</p>
          </div>
        </div>
      </div>
    </Chapter>
  );
}
