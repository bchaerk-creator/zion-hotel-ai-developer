import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Statement } from "@/components/Statement";
import { InvestorForm } from "@/components/InvestorForm";
import { legal } from "@/lib/data";

export const metadata: Metadata = { title: "Acesso para investidores · Zion Hotel Group International" };

export default function AcessoPage() {
  return (
    <>
      <Header total={13} initial={{ number: "13", title: "Acesso para investidores" }} accessHref="/acesso/" />
      <main className="bg-moss tone-dark text-cream">
        <section id="acesso" data-chapter="13" data-title="Acesso para investidores" className="wrap chapter pt-[24vh]">
          <p className="t-label mb-8">Acesso para investidores</p>
          <Statement text="Edição para investidores, após NDA." support={legal.investorEditionLine + " " + "Preencha o pedido. A equipe qualifica, envia o NDA e libera o acesso."} />
          <div className="bloco">
            <InvestorForm />
          </div>
        </section>
      </main>
      <Footer legal={legal} />
    </>
  );
}
