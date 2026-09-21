import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { BigNumberGrid } from "@/components/BigNumber";
import { Photo } from "@/components/Photo";
import { market } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Mercado() {
  return (
    <Chapter id="mercado" number="02" title="O mercado" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="02" title="O mercado" />
        <Statement text="O luxo mudou do material para o estado." support="New luxury e turismo de desaceleração. A categoria de hospedagem na natureza ainda não tem operador consolidado no Brasil." />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <ul>
            {market.thesis.map((t) => (
              <li key={t.id} className="border-t py-6" style={{ borderColor: "var(--line)" }}>
                <p className="t-subtitle !text-[clamp(22px,2.2vw,30px)]">{t.label}</p>
                <p className="t-body mt-2" style={{ color: "var(--muted)" }}>{t.text}</p>
              </li>
            ))}
          </ul>
          <Photo photo={photo("interior_ceu")} className="md:self-start" />
        </div>
        <div className="bloco">
          <p className="t-label mb-8">Números de mercado, aguardando fonte oficial</p>
          <BigNumberGrid metrics={market.numbers} columns={4} />
        </div>
      </div>
    </Chapter>
  );
}
