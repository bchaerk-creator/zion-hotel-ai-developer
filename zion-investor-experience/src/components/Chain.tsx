type Step = { number: string; label: string; note?: string };

/** Sequência numerada horizontal. Só para sequências reais. */
export function Chain({ steps }: { steps: Step[] }) {
  return (
    <ol className="grid gap-x-8 gap-y-10" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(150px, 1fr))` }}>
      {steps.map((s) => (
        <li key={s.number + s.label} className="border-t pt-5" style={{ borderColor: "var(--line)" }}>
          <p className="font-serif text-[28px] font-light leading-none text-gold">{s.number}</p>
          <p className="t-subtitle mt-4 !text-[clamp(22px,2vw,28px)]">{s.label}</p>
          {s.note && (
            <p className="t-table mt-2" style={{ color: "var(--muted)" }}>
              {s.note}
            </p>
          )}
        </li>
      ))}
    </ol>
  );
}
