import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { Chain } from "@/components/Chain";
import { program } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Destinos() {
  const last = program.waves[program.waves.length - 1];
  return (
    <Chapter id="destinos" number="06" title="Destinos" bg="photo">
      <div className="relative">
        <Photo photo={photo("aerea_noturna")} veil="block" fill />
        <div className="wrap chapter relative">
          <ChapterLabel number="06" title="Destinos" />
          <Statement text={`${program.totalDestinations} destinos em ${program.waves.length} ondas.`} support={`De ${program.waves[0].year} a ${last.year}, ${program.unitsPerSite} unidades por sede. Cada onda abre depois que a anterior opera no plano.`} />
          <div className="bloco">
            <Chain
              steps={program.waves.map((w) => ({
                number: String(w.wave).padStart(2, "0"),
                label: String(w.year),
                note: w.destinations.map((d) => (d.state ? `${d.name} ${d.state}` : d.name) + (d.note ? ` (${d.note.toLowerCase()})` : "")).join(" · "),
              }))}
            />
          </div>
        </div>
      </div>
    </Chapter>
  );
}
