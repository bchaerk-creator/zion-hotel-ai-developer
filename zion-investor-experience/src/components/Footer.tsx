import type { LegalData } from "@data/types";

export function Footer({ legal }: { legal: LegalData }) {
  return (
    <footer className="bg-black tone-dark text-cream">
      <div className="wrap border-t py-14" style={{ borderColor: "var(--line)" }}>
        <p className="font-serif text-[22px] tracking-[0.18em] text-gold">ZION</p>
        <p className="t-table mt-2 text-sand">Zion Hotel Group International · Integrated Real Estate &amp; Hospitality Development</p>
        <p className="mt-10 max-w-[80ch] text-[12.5px] leading-relaxed text-muted-dark">{legal.footer}</p>
        <p className="mt-6 text-[12px] text-muted-dark">Material informativo. Versão de setembro de 2026.</p>
      </div>
    </footer>
  );
}
