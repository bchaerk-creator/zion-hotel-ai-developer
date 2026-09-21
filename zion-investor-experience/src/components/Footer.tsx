import type { LegalData } from "@data/types";
import { Logo } from "./Logo";

export function Footer({ legal }: { legal: LegalData }) {
  return (
    <footer className="bg-black tone-dark text-cream">
      <div className="wrap border-t py-14" style={{ borderColor: "var(--line)" }}>
        <div className="text-gold"><Logo variant="lockup" height={52} label="Zion Hotel Group International" /></div>
        <p className="t-table mt-6 text-sand">Integrated Real Estate &amp; Hospitality Development</p>
        <p className="mt-10 max-w-[80ch] text-[12.5px] leading-relaxed text-muted-dark">{legal.footer}</p>
        <p className="mt-6 text-[12px] text-muted-dark">Material informativo. Versão de setembro de 2026.</p>
      </div>
    </footer>
  );
}
