import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { ModuleBlock } from "@/components/ModuleBlock";
import { landBank, market } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Desenvolvimento() {
  return (
    <Chapter id="desenvolvimento" number="09" title="Desenvolvimento" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="09" title="Desenvolvimento" />
        <Statement text="Território vira projeto." support="Fundação pontual, estrutura modular, baixa densidade. A implantação respeita a clareira e pode ser desfeita." />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <Photo photo={photo("aerea_zenital")} />
          <div className="self-end">
            <p className="t-label mb-6">O que já é verdade na implantação</p>
            <ul className="t-list">
              {market.sustainability.facts.map((f) => (
                <li key={f} className="border-b py-3 !text-[clamp(20px,2vw,28px)]" style={{ borderColor: "var(--line)" }}>
                  {f}
                </li>
              ))}
            </ul>
            <p className="t-table mt-6" style={{ color: "var(--muted)" }}>
              {market.sustainability.certifications} {market.sustainability.carbon}
            </p>
          </div>
        </div>
      </div>
      <ModuleBlock module={landBank.module} />
    </Chapter>
  );
}
