import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Chain } from "@/components/Chain";
import { DataTable } from "@/components/DataTable";
import { raise } from "@/lib/data-investor";
import { nbsp } from "@/lib/format";

export function Captacao() {
  return (
    <Chapter id="captacao" number="17" title="A captação" bg="moss">
      <div className="wrap chapter">
        <ChapterLabel number="17" title="A captação" />
        <Statement text={`Rodada de ${nbsp(raise.round.value)}.`} support={`${raise.round.sizedBy}. ${raise.round.selfFinancingShare}. Três tranches liberadas por marco operacional, não por calendário.`} />
        <div className="bloco">
          <Chain steps={raise.tranches.map((t) => ({ number: t.id, label: t.value, note: t.milestone }))} />
        </div>
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <DataTable
            caption="Necessidade máxima de caixa do programa"
            columns={[{ key: "label", label: "Cenário" }, { key: "peak", label: "Pico", align: "right" }, { key: "year", label: "Ano do pico", align: "right" }, { key: "zero", label: "Caixa volta a zero", align: "right" }]}
            rows={raise.cashNeed.map((c) => ({ _key: c.scenario, label: c.label, peak: c.peak, year: String(c.peakYear), zero: String(c.backToZero) }))}
            sourceId={raise.sourceId}
            status="estimate"
          />
          <div className="self-end">
            <p className="t-label mb-4">Condições</p>
            <p className="t-subtitle">{raise.terms.gracePerSite}</p>
            <p className="t-subtitle mt-4">{raise.terms.distribution}</p>
          </div>
        </div>
      </div>
    </Chapter>
  );
}
