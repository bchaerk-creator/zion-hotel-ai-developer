import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { DataTable } from "@/components/DataTable";
import { model } from "@/lib/data-investor";
import { brl } from "@/lib/format";
import { photo } from "@/lib/photos";

export function Sede() {
  return (
    <Chapter id="sede" number="14" title="Uma sede" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="14" title="Uma sede" />
        <Statement text={`Uma sede de ${model.units} unidades.`} support={model.configuration.recommendation + " " + model.configuration.caveat} />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <Photo photo={photo("flo_zenital")} className="!aspect-[4/5]" />
          <div className="self-end">
            <DataTable
              caption="Premissas, calibradas contra os demonstrativos de 2025"
              columns={[{ key: "label", label: "Premissa" }, { key: "value", label: "Valor" }]}
              rows={model.assumptions.map((a) => ({ _key: a.id, label: a.label, value: a.note ? `${a.value}. ${a.note}` : a.value }))}
              sourceId={model.sourceId}
              status="estimate"
            />
          </div>
        </div>
        <div className="bloco">
          <DataTable
            caption="Quadro de pessoal validado contra o modelo"
            columns={[
              { key: "units", label: "Unidades" },
              { key: "roles", label: "Equipe fixa" },
              { key: "payroll", label: "Folha ao mês", align: "right" },
              { key: "annual", label: "Ao ano com encargos", align: "right" },
              { key: "fixed", label: "Custo fixo com diárias de pico e administrativo", align: "right" },
            ]}
            rows={model.staffing.plans.map((p) => ({ _key: String(p.units), units: String(p.units), roles: p.roles.join(", "), payroll: brl(p.monthlyPayroll), annual: brl(p.annualPayrollWithCharges), fixed: brl(p.annualFixedCost) }))}
            sourceId={model.sourceId}
            status="estimate"
          />
          <p className="t-table mt-4" style={{ color: "var(--muted)" }}>{model.staffing.rule}</p>
        </div>
      </div>
    </Chapter>
  );
}
