import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { DocumentList } from "@/components/DocumentList";
import { documents } from "@/lib/data";

export function Documentos() {
  const kit = documents.documents.filter((d) => d.dataRoom);
  return (
    <Chapter id="documentos" number="20" title="Documentos" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="20" title="Documentos" />
        <Statement text="O kit de documentos." support={`${kit.length} documentos no data room. Teaser, arquitetura jurídica e modelo dos 23 destinos ficam fora até a atualização para o asset light.`} />
        <div className="bloco">
          <DocumentList documents={kit} statusLabels={documents.statusLabels} canDownload={false} />
        </div>
      </div>
    </Chapter>
  );
}
