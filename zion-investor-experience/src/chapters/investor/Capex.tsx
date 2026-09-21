import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { CapexTable } from "@/components/CapexTable";
import { DataTable } from "@/components/DataTable";
import { Photo } from "@/components/Photo";
import { SourceBadge } from "@/components/SourceBadge";
import { capex } from "@/lib/data-investor";
import { brl } from "@/lib/format";
import { photo } from "@/lib/photos";

export function Capex() {
  return (
    <Chapter id="capex" number="15" title="CAPEX" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="15" title="CAPEX" />
        <Statement text={`${brl(capex.allIn.value)} all-in.`} support={`Sede de ${capex.units} unidades, ${brl(capex.allIn.perUnit)} por chave com terreno arrendado, taxas e obras de sítio. A implantação leva meses, não anos, porque o produto chega pronto da Store.`} />
        <div className="bloco">
          <CapexTable capex={capex} />
        </div>
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <DataTable
            caption="Obras de sítio por tier"
            columns={[{ key: "label", label: "Tier" }, { key: "value", label: "Valor", align: "right" }]}
            rows={capex.siteWorks.tiers.map((t) => ({ _key: t.id, label: t.label + (t.id === capex.siteWorks.selectedTier ? ", adotado no modelo" : ""), value: brl(t.value) }))}
            sourceId={capex.sourceId}
            status="estimate"
          />
          <DataTable
            caption="Custo por chave, só implantação"
            columns={[{ key: "label", label: "Sede" }, { key: "value", label: "Por chave", align: "right" }]}
            rows={capex.perKeyBySize.map((k) => ({ _key: String(k.units), label: `${k.units} unidades`, value: brl(k.value) }))}
            sourceId={capex.sourceId}
            status="estimate"
          />
        </div>
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <div className="self-end">
            <p className="t-label mb-4">Referência de mercado</p>
            <p className="t-subtitle">{capex.marketReference.label}: {capex.marketReference.range} por chave, {capex.marketReference.buildTime}.</p>
            <div className="mt-3">
              <SourceBadge sourceId={capex.marketReference.sourceId} status={capex.marketReference.status} />
            </div>
            <p className="t-label mt-12 mb-4">Opcionais</p>
            {capex.optionals.map((o) => (
              <p key={o.id} className="t-subtitle">{o.label}: {brl(o.perUnit)} por unidade.</p>
            ))}
          </div>
          <Photo photo={photo("flo_piscina")} className="!aspect-[4/5]" />
        </div>
      </div>
    </Chapter>
  );
}
