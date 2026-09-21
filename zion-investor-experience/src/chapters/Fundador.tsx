import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Chain } from "@/components/Chain";
import { company } from "@/lib/data";

export function Fundador() {
  const { founder, method } = company;
  return (
    <Chapter id="fundador" number="04" title="O fundador" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="04" title="O fundador" />
        <div className="grid gap-12 md:grid-cols-[2fr_3fr] md:gap-[6vw]">
          <div className="relative aspect-[4/5] bg-moss">
            <div className="absolute inset-0 flex items-end p-5">
              <p className="t-source !no-underline text-sand/70">Retrato a fornecer: {founder.name}</p>
            </div>
          </div>
          <div className="self-end">
            <Statement as="p" text={founder.name} />
            <p className="t-subtitle mt-4 text-sand">{founder.role}</p>
            <p className="t-support mt-8">{founder.bio}</p>
          </div>
        </div>
        <div className="bloco">
          <p className="t-label mb-3">{method.name}</p>
          <p className="t-subtitle max-w-[28ch]">{method.description} {method.rule}</p>
          <div className="mt-14 grid gap-14 md:grid-cols-2 md:gap-[6vw]">
            {method.tracks.map((t) => (
              <div key={t.id}>
                <p className="t-table mb-6 text-sand">Trilho {t.name} · certificação {t.certification}</p>
                <Chain steps={t.pillars.map((p, i) => ({ number: String(i + 1).padStart(2, "0"), label: p }))} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </Chapter>
  );
}
