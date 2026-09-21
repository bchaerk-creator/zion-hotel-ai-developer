import type { MetricStatus } from "@data/types";
import { getSource } from "@/lib/data";

type Props = { sourceId: string; status: MetricStatus; period?: string; className?: string };

/** Validado: sublinhado fino. Pendente: tracejado, "Fonte em validação". */
export function SourceBadge({ sourceId, status, period, className = "" }: Props) {
  const source = getSource(sourceId);
  const pending = status === "pending";
  const showPeriod = period && !source.label.includes(period);
  const estimateSuffix = status === "estimate" && source.kind !== "company" ? ", estimativa" : "";
  const text = pending ? "Fonte em validação" : source.label + (showPeriod ? `, ${period}` : "") + estimateSuffix;
  return (
    <span className={`t-source ${pending ? "t-source--pending" : ""} ${className}`} title={source.note}>
      {text}
    </span>
  );
}
