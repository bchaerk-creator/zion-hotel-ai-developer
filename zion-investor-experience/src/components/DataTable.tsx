import type { ReactNode } from "react";
import type { MetricStatus } from "@data/types";
import { SourceBadge } from "./SourceBadge";

export type Column = { key: string; label: string; align?: "left" | "right" };
type Row = Record<string, ReactNode> & { _key?: string; _total?: boolean };

type Props = { columns: Column[]; rows: Row[]; caption?: string; sourceId?: string; status?: MetricStatus; period?: string };

/** Fios finos, sem fundo nas linhas, linha de total em peso 500. Rola no próprio contêiner. */
export function DataTable({ columns, rows, caption, sourceId, status = "validated", period }: Props) {
  return (
    <div>
      <div className="table-scroll">
        <table className="t-table w-full">
          {caption && <caption className="t-label pb-4 text-left">{caption}</caption>}
          <thead>
            <tr className="border-b" style={{ borderColor: "var(--line)" }}>
              {columns.map((c) => (
                <th
                  key={c.key}
                  scope="col"
                  className={`t-th py-3 pr-6 font-medium ${c.align === "right" ? "text-right" : "text-left"}`}
                  style={{ color: "var(--muted)" }}
                >
                  {c.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr
                key={r._key ?? i}
                className={`border-b ${r._total ? "font-medium" : ""}`}
                style={{ borderColor: "var(--line)" }}
              >
                {columns.map((c) => (
                  <td key={c.key} className={`py-3 pr-6 align-top ${c.align === "right" ? "text-right tabular-nums" : ""}`}>
                    {r[c.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {sourceId && (
        <div className="mt-3">
          <SourceBadge sourceId={sourceId} status={status} period={period} />
        </div>
      )}
    </div>
  );
}
