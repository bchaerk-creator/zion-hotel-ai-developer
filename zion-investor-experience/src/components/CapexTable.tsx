import type { CapexData } from "@data/types";
import { brl } from "@/lib/format";
import { DataTable } from "./DataTable";

/** Blocos, subtotal, contingência, giro, taxas, obras de sítio e all-in. */
export function CapexTable({ capex }: { capex: CapexData }) {
  const columns = [
    { key: "label", label: `Sede de ${capex.units} unidades` },
    { key: "total", label: "Total", align: "right" as const },
    { key: "perUnit", label: "Por unidade", align: "right" as const },
  ];
  const rows = [
    ...capex.blocks.map((b) => ({ _key: b.id, label: b.note ? `${b.label} *` : b.label, total: brl(b.total), perUnit: b.perUnit === null ? "" : brl(b.perUnit) })),
    { _key: "subtotal", _total: true, label: "Subtotal de implantação", total: brl(capex.implementationSubtotal), perUnit: "" },
    { _key: "contingency", label: `Contingência técnica, ${capex.contingency.rate}`, total: brl(capex.contingency.value), perUnit: "" },
    { _key: "wc", label: `Capital de giro, ${brl(capex.workingCapital.perUnit)} por unidade`, total: brl(capex.workingCapital.value), perUnit: "" },
    { _key: "impl", _total: true, label: "Total de implantação", total: brl(capex.implementationTotal.value), perUnit: brl(capex.implementationTotal.perUnit) },
    { _key: "fees", label: capex.fees.label, total: brl(capex.fees.value), perUnit: "" },
    { _key: "site", label: `Obras de sítio, ${capex.siteWorks.tiers.find((t) => t.id === capex.siteWorks.selectedTier)?.label}`, total: brl(capex.siteWorks.value), perUnit: "" },
    { _key: "allin", _total: true, label: "CAPEX all-in", total: brl(capex.allIn.value), perUnit: brl(capex.allIn.perUnit) },
  ];
  return (
    <div>
      <DataTable columns={columns} rows={rows} sourceId={capex.sourceId} status="estimate" />
      {capex.blocks.some((b) => b.note) && (
        <p className="mt-4 text-[12px]" style={{ color: "var(--muted)" }}>
          * {capex.blocks.filter((b) => b.note).map((b) => b.note).join(" ")}
        </p>
      )}
    </div>
  );
}
