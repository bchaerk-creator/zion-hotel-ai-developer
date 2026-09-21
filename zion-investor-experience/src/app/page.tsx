import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { legal } from "@/lib/data";
import { PUBLIC_TOTAL, publicChapters } from "@/lib/chapters";
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

/** Edição pública. Nenhum dado de retorno entra aqui. */
export default function PublicEdition() {
  return (
    <>
      <Header total={PUBLIC_TOTAL} initial={publicChapters[0]} accessHref="/acesso/" />
      <main>
        <Intro />
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
        <Acesso />
      </main>
      <Footer legal={legal} />
    </>
  );
}
