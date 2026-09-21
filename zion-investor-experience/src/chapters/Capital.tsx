import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { platform } from "@/lib/data";

export function Capital() {
  return (
    <Chapter id="capital" number="10" title="O capital" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="10" title="O capital" />
        <Statement text="Asset light puro." support="O investidor detém a SPE. A Zion é remunerada pelo que entrega: produto, desenvolvimento, implantação, operação e marca." />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <ol>
            {platform.capitalModel.principles.map((p, i) => (
              <li key={p} className="grid grid-cols-[48px_1fr] border-t py-6" style={{ borderColor: "var(--line)" }}>
                <span className="font-serif text-[28px] font-light leading-none text-gold">{String(i + 1).padStart(2, "0")}</span>
                <span className="t-support">{p}</span>
              </li>
            ))}
          </ol>
          <div className="self-end">
            <p className="t-label mb-4">Exclusividade</p>
            <p className="t-support" style={{ color: "var(--fg-2)" }}>{platform.exclusivity}</p>
            <p className="t-table mt-8" style={{ color: "var(--muted)" }}>
              Condições de captação, CAPEX, forecast e retorno estão na edição para investidores, disponível após NDA.
            </p>
          </div>
        </div>
      </div>
    </Chapter>
  );
}
