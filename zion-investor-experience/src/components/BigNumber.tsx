import type { Metric } from "@data/types";
import { SourceBadge } from "./SourceBadge";

export function BigNumber({ metric, size = "lg" }: { metric: Metric; size?: "lg" | "md" }) {
  return (
    <div>
      <p className={size === "lg" ? "t-number" : "t-subtitle"}>{metric.value}</p>
      <p className="t-table mt-3">{metric.label}</p>
      {metric.context && (
        <p className="mt-1 text-[12px]" style={{ color: "var(--muted)" }}>
          {metric.context}
        </p>
      )}
      <div className="mt-3">
        <SourceBadge sourceId={metric.sourceId} status={metric.status} period={metric.period} />
      </div>
    </div>
  );
}

export function BigNumberGrid({ metrics, columns = 4 }: { metrics: Metric[]; columns?: 2 | 4 }) {
  const cols = columns === 4 ? "md:grid-cols-4" : "md:grid-cols-2";
  return (
    <div className={`grid grid-cols-2 gap-8 ${cols}`}>
      {metrics.map((m) => (
        <BigNumber key={m.id} metric={m} size={columns === 4 ? "md" : "lg"} />
      ))}
    </div>
  );
}
