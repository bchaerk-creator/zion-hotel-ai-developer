import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { program } from "@/lib/data";
import { photo } from "@/lib/photos";

export function Brasil() {
  return (
    <Chapter id="brasil" number="03" title="Brasil" bg="cream">
      <div className="wrap chapter">
        <ChapterLabel number="03" title="Brasil" />
        <Statement text="Um país inteiro de destinos por desenvolver." support={`${program.totalDestinations} destinos em ${program.corridors.length} corredores, escolhidos por demanda o ano inteiro, mercado emissor próximo e natureza que sustenta a marca.`} />
        <div className="bloco grid grid-cols-2 gap-8 md:grid-cols-4">
          {program.corridors.map((c) => (
            <div key={c.id}>
              <p className="t-number">{c.count}</p>
              <p className="t-table mt-3">{c.label}</p>
              <p className="mt-1 text-[12px]" style={{ color: "var(--muted)" }}>destinos no programa</p>
            </div>
          ))}
        </div>
      </div>
      <div className="relative min-h-[80svh] tone-dark text-cream">
        <Photo photo={photo("aerea_araucaria")} veil="phrase" fill />
        <div className="wrap relative flex min-h-[80svh] flex-col justify-end pb-[12vh] pt-[12vh]">
          <Statement text="Natureza, litoral, cultura e montanha." support="Quatro corredores. Um único padrão de produto, operação e marca." />
        </div>
      </div>
    </Chapter>
  );
}
