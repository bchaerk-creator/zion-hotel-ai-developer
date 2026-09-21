import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { InvestorGate } from "@/components/InvestorGate";
import { legal } from "@/lib/data";
import { INVESTOR_TOTAL, investorChapters } from "@/lib/chapters";
import { Intro } from "@/chapters/Intro";
import { Oportunidade } from "@/chapters/Oportunidade";
import { Mercado } from "@/chapters/Mercado";
import { Brasil } from "@/chapters/Brasil";
import { Fundador } from "@/chapters/Fundador";
import { Prova } from "@/chapters/Prova";
import { Destinos } from "@/chapters/Destinos";
import { Ecossistema } from "@/chapters/Ecossistema";
import { LandBank } from "@/chapters/LandBank";
import { Desenvolvimento } from "@/chapters/Desenvolvimento";
import { Capital } from "@/chapters/Capital";
import { Estrutura } from "@/chapters/Estrutura";
import { Visao } from "@/chapters/Visao";
import { Acesso } from "@/chapters/Acesso";
import { Programa } from "@/chapters/investor/Programa";
import { Sede } from "@/chapters/investor/Sede";
import { Capex } from "@/chapters/investor/Capex";
import { Forecast } from "@/chapters/investor/Forecast";
import { Captacao } from "@/chapters/investor/Captacao";
import { Retorno } from "@/chapters/investor/Retorno";
import { Valor } from "@/chapters/investor/Valor";
import { Documentos } from "@/chapters/investor/Documentos";

export const metadata: Metadata = {
  title: "Edição para investidores · Zion Hotel Group International",
  robots: { index: false, follow: false },
};

/** Edição para investidores. Uso confidencial, após NDA. */
export default function InvestorEdition() {
  return (
    <InvestorGate>
      <Header total={INVESTOR_TOTAL} initial={investorChapters[0]} accessHref="#acesso" />
      <main>
        <Intro edition="investor" />
        <Oportunidade />
        <Mercado />
        <Brasil />
        <Fundador />
        <Prova />
        <Destinos />
        <Ecossistema />
        <LandBank />
        <Desenvolvimento />
        <Capital />
        <Estrutura />
        <Visao />
        <Programa />
        <Sede />
        <Capex />
        <Forecast />
        <Captacao />
        <Retorno />
        <Valor />
        <Documentos />
        <Acesso number="21" edition="investor" />
      </main>
      <Footer legal={legal} />
    </InvestorGate>
  );
}
