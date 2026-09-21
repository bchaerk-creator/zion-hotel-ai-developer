import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { EcosystemDiagram } from "@/components/EcosystemDiagram";
import { platform } from "@/lib/data";

export function Ecossistema() {
  const byId = (id: string) => platform.companies.find((c) => c.id === id)!;
  return (
    <Chapter id="ecossistema" number="07" title="Ecossistema" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="07" title="Ecossistema" />
        <Statement text="Cada braço faz uma coisa. A holding coordena." support="Marca e método na holding. Capital na Collection. Operação na Management. Produto na Store. Cada destino em uma SPE, com resultado segregado." />
        <div className="bloco">
          <EcosystemDiagram core={byId("holding")} left={[byId("collection"), byId("management")]} right={[byId("store"), byId("spe")]} />
        </div>
      </div>
    </Chapter>
  );
}
