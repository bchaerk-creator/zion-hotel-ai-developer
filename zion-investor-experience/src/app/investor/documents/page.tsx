import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { InvestorGate } from "@/components/InvestorGate";
import { DocumentList } from "@/components/DocumentList";
import { Statement } from "@/components/Statement";
import { documents, legal } from "@/lib/data";
import { INVESTOR_TOTAL } from "@/lib/chapters";

export const metadata: Metadata = {
  title: "Data room · Zion Hotel Group International",
  robots: { index: false, follow: false },
};

export default function DataRoomPage() {
  const kit = documents.documents.filter((d) => d.dataRoom);
  return (
    <InvestorGate>
      <Header total={INVESTOR_TOTAL} initial={{ number: "20", title: "Documentos" }} accessHref="/investor/#acesso" />
      <main className="bg-black tone-dark text-cream">
        <section id="documentos" data-chapter="20" data-title="Documentos" className="wrap chapter pt-[24vh]">
          <p className="t-label mb-8">Data room</p>
          <Statement text="O kit de documentos." support="Fase 1: a lista. Os arquivos chegam pelo data room após a assinatura do NDA. O download direto entra na Fase 3, com registro de acesso." />
          <div className="bloco">
            <DocumentList documents={kit} statusLabels={documents.statusLabels} canDownload={false} />
          </div>
        </section>
      </main>
      <Footer legal={legal} />
    </InvestorGate>
  );
}
