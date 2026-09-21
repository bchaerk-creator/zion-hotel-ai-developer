import type { Opportunity } from "@data/types";

/** Grade de dois, separada por fio de 1px. Nunca sombra, nunca canto arredondado. */
export function OpportunityCard({ opportunity: o }: { opportunity: Opportunity }) {
  return (
    <article className="py-8">
      <p className="t-label">{o.statusLabel}</p>
      <h3 className="t-subtitle mt-3">
        {o.name}
        {o.state && <span style={{ color: "var(--muted)" }}> · {o.state}</span>}
      </h3>
      {o.facts.length > 0 && (
        <dl className="t-table mt-5 grid grid-cols-2 gap-x-6 gap-y-2">
          {o.facts.map((f) => (
            <div key={f.label} className="contents">
              <dt style={{ color: "var(--muted)" }}>{f.label}</dt>
              <dd>{f.value}</dd>
            </div>
          ))}
        </dl>
      )}
    </article>
  );
}

export function OpportunityGrid({ opportunities }: { opportunities: Opportunity[] }) {
  return (
    <div className="grid border-t md:grid-cols-2" style={{ borderColor: "var(--line)" }}>
      {opportunities.map((o, i) => (
        <div
          key={o.id}
          className={`border-b ${i % 2 === 0 ? "md:border-r md:pr-10" : "md:pl-10"}`}
          style={{ borderColor: "var(--line)" }}
        >
          <OpportunityCard opportunity={o} />
        </div>
      ))}
    </div>
  );
}
