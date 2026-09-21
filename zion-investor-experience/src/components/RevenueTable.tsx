import type { RevenueData } from "@data/types";
import { SourceBadge } from "./SourceBadge";

export function RevenueTable({ data }: { data: RevenueData }) {
  return (
    <div className="table-scroll">
      <table className="t-table w-full">
        <thead>
          <tr className="border-b" style={{ borderColor: "var(--line)" }}>
            <th scope="col" className="t-th py-3 pr-6 text-left font-medium" style={{ color: "var(--muted)" }}>Período</th>
            <th scope="col" className="t-th py-3 pr-6 text-right font-medium whitespace-nowrap" style={{ color: "var(--muted)" }}>Receita bruta</th>
            <th scope="col" className="t-th py-3 text-left font-medium" style={{ color: "var(--muted)" }}>Base</th>
          </tr>
        </thead>
        <tbody>
          {data.periods.map((p) => (
            <tr key={p.id} className="border-b" style={{ borderColor: "var(--line)" }}>
              <td className="py-3 pr-6">{p.period}</td>
              <td className="py-3 pr-6 text-right tabular-nums whitespace-nowrap">{p.value}</td>
              <td className="py-3">
                <span className="block">{p.basis}</span>
                <SourceBadge sourceId={p.sourceId} status={p.status} />
              </td>
            </tr>
          ))}
          <tr className="border-b font-medium" style={{ borderColor: "var(--line)" }}>
            <td className="py-3 pr-6">Total até 30/06/2026</td>
            <td className="py-3 pr-6 text-right tabular-nums whitespace-nowrap">{data.total.value}</td>
            <td className="py-3">{data.documented.value} documentados em demonstrativo de resultado</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
