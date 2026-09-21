import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { Photo } from "@/components/Photo";
import { company } from "@/lib/data";
import { photo } from "@/lib/photos";
import { Globe } from "@/components/Globe";

export function Visao() {
  return (
    <Chapter id="visao" number="12" title="A visão" bg="black">
      <div className="relative overflow-hidden">
        <Globe />
        <div className="wrap chapter relative">
          <ChapterLabel number="12" title="A visão" />
          <Statement text={company.message} />
        </div>
      </div>
      <div className="relative min-h-[90svh]">
        <Photo photo={photo("flo_noturna")} veil="phrase" fill />
        <div className="wrap relative flex min-h-[90svh] flex-col justify-end pb-[12vh] pt-[12vh]">
          <Statement text="Construímos destinos." support="A próxima geração da hospitalidade não é um prédio. É um lugar." />
        </div>
      </div>
    </Chapter>
  );
}
