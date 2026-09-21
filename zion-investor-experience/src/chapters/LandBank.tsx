import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { BigNumber, BigNumberGrid } from "@/components/BigNumber";
import { Chain } from "@/components/Chain";
import { ProportionBar } from "@/components/ProportionBar";
import { DataTable } from "@/components/DataTable";
import { OpportunityGrid } from "@/components/OpportunityCard";
import { landBank } from "@/lib/data";
import { hectares } from "@/lib/format";

export function LandBank() {
  const share = (id: string) => Number(landBank.layers.find((l) => l.id === id)?.share?.replace("%", "").replace(",", ".") ?? 0);
  return (
    <Chapter id="land-bank" number="08" title="Land bank" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="08" title="Land bank" />
        <div className="grid gap-12 md:grid-cols-[3fr_2fr] md:gap-[6vw] md:items-end">
          <Statement text="O pipeline por trás da plataforma." support="Hectares mapeados em quatro camadas, do contato do proprietário ao projeto com alvará. Capacidade de território, nunca promessa de retorno." />
          <BigNumber metric={landBank.total} />
        </div>
        <div className="bloco">
          <Chain steps={landBank.pipeline.map((p, i) => ({ number: String(i + 1).padStart(2, "0"), label: p }))} />
        </div>
        <div className="bloco">
          <ProportionBar
            segments={[
              { label: "Ativos em avaliação", share: share("assets"), tone: "gold" },
              { label: "Land bank de proprietários", share: share("landbank"), tone: "sand" },
              { label: "Projetos", share: share("projects"), tone: "cream" },
            ]}
          />
          <div className="mt-12 grid gap-12 md:grid-cols-2 md:gap-[6vw]">
            <DataTable
              caption="Camadas"
              columns={[{ key: "label", label: "Camada" }, { key: "ha", label: "Hectares", align: "right" }, { key: "share", label: "Participação", align: "right" }]}
              rows={landBank.layers.map((l) => ({ _key: l.id, label: l.label, ha: l.hectares === null ? l.note ?? "" : hectares(l.hectares), share: l.share ?? "" }))}
              sourceId={landBank.sourceId}
              period={landBank.asOf.split("-").reverse().join("/")}
            />
            <DataTable
              caption="Por região"
              columns={[{ key: "label", label: "Região" }, { key: "ha", label: "Hectares", align: "right" }]}
              rows={landBank.regions.map((r) => ({ _key: r.id, label: r.label, ha: hectares(r.hectares) }))}
              sourceId={landBank.sourceId}
              period={landBank.asOf.split("-").reverse().join("/")}
            />
          </div>
          <p className="t-support mt-8" style={{ color: "var(--fg-2)" }}>{landBank.regionReading}</p>
        </div>
        <div className="bloco">
          <BigNumberGrid metrics={landBank.indicators} columns={4} />
        </div>
        <div className="bloco">
          <p className="t-label mb-8">Oportunidades em curso</p>
          <OpportunityGrid opportunities={landBank.opportunities} />
          <p className="t-table mt-6" style={{ color: "var(--muted)" }}>
            Áreas de terceiros mapeadas pela Zion. Zoneamento, licença e restrição ambiental constam do documento de origem de cada oportunidade.
          </p>
        </div>
      </div>
    </Chapter>
  );
}
