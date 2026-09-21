import type { Scenario } from "@data/types";
import { brl } from "@/lib/format";
import { DataTable } from "./DataTable";

type Props = { scenarios: Scenario[]; showReturns: boolean; sourceId: string; period?: string };

/**
 * Ano 1 por cenário. O conservador aparece sempre ao lado do base.
 * showReturns só é true na edição para investidores.
 */
export function ScenarioTable({ scenarios, showReturns, sourceId, period }: Props) {
  const columns = [
    { key: "label", label: "Ano 1, sede de 12 unidades" },
    ...scenarios.map((s) => ({ key: s.id, label: s.label, align: "right" as const })),
  ];
  const row = (label: string, pick: (s: Scenario) => string) =>
    Object.fromEntries([["_key", label], ["label", label], ...scenarios.map((s) => [s.id, pick(s)])]);
  const rows = [
    row("Ocupação", (s) => s.occupancy),
    row("Receita bruta", (s) => brl(s.grossRevenue)),
    row("EBITDA", (s) => brl(s.ebitda)),
    row("Margem EBITDA", (s) => s.ebitdaMargin),
    row("Lucro líquido", (s) => brl(s.netIncome)),
  ];
  if (showReturns) {
    rows.push(
      row("Yield sobre capital", (s) => s.yieldOnCapital),
      row("Múltiplo em 7 anos", (s) => s.multiple7y),
      row("Ciclo de retorno do capital", (s) => s.capitalReturnCycle),
    );
  }
  return <DataTable columns={columns} rows={rows} sourceId={sourceId} status="estimate" period={period} />;
}
