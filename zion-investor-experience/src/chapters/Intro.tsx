import { HeroPhoto } from "@/components/HeroPhoto";
import { company, legal } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Intro({ edition = "public" }: { edition?: "public" | "investor" }) {
  const investor = edition === "investor";
  return (
    <section id="intro" data-chapter="00" data-title="Introdução">
      <HeroPhoto
        photo={photo("aerea_mata")}
        eyebrow={company.tagline}
        topline={investor ? legal.investorEditionLine : undefined}
        lines={["O futuro da", "hospitalidade", "está sendo construído", "na natureza."]}
        primary={{ label: "Explorar a oportunidade", href: "#oportunidade" }}
        secondary={investor ? { label: "Ir ao CAPEX e retorno", href: "#programa" } : { label: "Acesso para investidores", href: "/acesso/" }}
      />
    </section>
  );
}
