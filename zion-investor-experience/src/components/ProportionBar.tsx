type Segment = { label: string; share: number; tone: "gold" | "sand" | "cream" };

const toneClass = { gold: "bg-gold", sand: "bg-sand", cream: "bg-cream" };

/** Barra de 14px dividida em dourado, areia e creme. */
export function ProportionBar({ segments }: { segments: Segment[] }) {
  return (
    <div>
      <div className="flex h-[14px] w-full overflow-hidden" role="img" aria-label={segments.map((s) => `${s.label} ${s.share}%`).join(", ")}>
        {segments.map((s) => (
          <div key={s.label} className={toneClass[s.tone]} style={{ width: `${s.share}%`, minWidth: s.share > 0 ? 2 : 0 }} />
        ))}
      </div>
      <ul className="mt-4 flex flex-wrap gap-x-8 gap-y-2">
        {segments.map((s) => (
          <li key={s.label} className="t-table flex items-center gap-3">
            <span className={`inline-block h-[10px] w-[10px] ${toneClass[s.tone]}`} aria-hidden />
            {s.label}
            <span style={{ color: "var(--muted)" }}>{String(s.share).replace(".", ",")}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
