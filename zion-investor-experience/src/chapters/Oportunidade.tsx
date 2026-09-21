import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Ladder } from "@/components/Ladder";
import { company } from "@/lib/data";

export function Oportunidade() {
  return (
    <Chapter id="oportunidade" number="01" title="A oportunidade" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="01" title="A oportunidade" />
        <Statement text="A Bubble foi o começo." support={company.positioning} />
        <div className="bloco grid gap-12 md:grid-cols-2 md:gap-[6vw]">
          <ol className="t-list">
            {company.story.map((line) => (
              <li key={line} className="border-b py-3" style={{ borderColor: "var(--line)" }}>
                {line}
              </li>
            ))}
          </ol>
          <div>
            <p className="t-label mb-6">De onde a categoria vem e para onde vai</p>
            <Ladder rungs={["Camping", "Glamping", "Hospedagem na natureza", "Destino", "Hospitality real estate"]} />
            <p className="t-support mt-8" style={{ color: "var(--fg-2)" }}>
              {company.brandConcept.name}: {company.brandConcept.description}
            </p>
          </div>
        </div>
      </div>
    </Chapter>
  );
}
