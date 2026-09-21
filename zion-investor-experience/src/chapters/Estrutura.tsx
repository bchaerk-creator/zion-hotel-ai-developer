import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { LegalStack } from "@/components/LegalStack";
import { platform } from "@/lib/data";

export function Estrutura() {
  const byId = (id: string) => platform.companies.find((c) => c.id === id)!;
  return (
    <Chapter id="estrutura" number="11" title="Estrutura jurídica" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="11" title="Estrutura jurídica" />
        <Statement text="Um veículo por destino." support="A holding detém marca e método. A Collection recebe o capital e coordena. Cada sede é uma SPE com resultado segregado. Operadora e Store prestam serviço a preço publicado." />
        <div className="bloco max-w-[820px]">
          <LegalStack stack={[byId("holding"), byId("collection"), byId("spe")]} providers={[byId("management"), byId("store")]} />
        </div>
        <p className="t-table mt-12 max-w-[70ch]" style={{ color: "var(--muted)" }}>
          Fora do perímetro: {platform.outsidePerimeter.map((o) => `${o.name} (${o.site})`).join(" e ")}. {platform.outsidePerimeterNote}
        </p>
      </div>
    </Chapter>
  );
}
