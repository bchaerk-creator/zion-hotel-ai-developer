import type { ModelData } from "@data/types";
import { mi } from "@/lib/format";
import { DataTable } from "./DataTable";

type Props = { forecast: ModelData["forecast"]; sourceId: string };

/** Sete anos, um bloco por cenário, valores em R$ milhões. */
export function ForecastTable({ forecast, sourceId }: Props) {
  const columns = [
    { key: "year", label: "Ano" },
    { key: "occupancy", label: "Ocupação", align: "right" as const },
    { key: "revenue", label: "Receita bruta", align: "right" as const },
    { key: "ebitda", label: "EBITDA", align: "right" as const },
    { key: "net", label: "Lucro líquido", align: "right" as const },
  ];
  return (
    <div className="grid gap-14">
      {forecast.scenarios.map((s) => (
        <DataTable
          key={s.id}
          caption={`${s.label}, ${forecast.unit}`}
          columns={columns}
          rows={s.rows.map((r) => ({ _key: String(r.year), year: String(r.year), occupancy: r.occupancy, revenue: mi(r.grossRevenue), ebitda: mi(r.ebitda), net: mi(r.netIncome) }))}
          sourceId={sourceId}
          status="estimate"
        />
      ))}
    </div>
  );
}
