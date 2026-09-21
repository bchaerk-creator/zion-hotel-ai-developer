import { HeroPhoto } from "@/components/HeroPhoto";
import { company } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Intro() {
  return (
    <section id="intro" data-chapter="00" data-title="Introdução">
      <HeroPhoto
        photo={photo("bubble_deck")}
        eyebrow={company.tagline}
        lines={["O futuro da", "hospitalidade", "está sendo construído", "na natureza."]}
        primary={{ label: "Explorar a oportunidade", href: "#oportunidade" }}
        secondary={{ label: "Acesso para investidores", href: "/acesso/" }}
      />
    </section>
  );
}
