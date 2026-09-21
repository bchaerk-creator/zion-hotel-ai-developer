import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { InvestorForm } from "@/components/InvestorForm";

export function Acesso({ number = "13", edition = "public" }: { number?: string; edition?: "public" | "investor" }) {
  const investor = edition === "investor";
  return (
    <Chapter id="acesso" number={number} title={investor ? "Próximo passo" : "Acesso para investidores"} bg="moss">
      <div className="wrap chapter">
        <ChapterLabel number={number} title={investor ? "Próximo passo" : "Acesso para investidores"} />
        {investor ? (
          <Statement text="Vamos falar de uma sede." support="Deixe o destino de interesse, a faixa de aporte ou o terreno que quer apresentar. A equipe da Zion agenda a conversa de due diligence e abre o data room completo." />
        ) : (
          <Statement text="Edição para investidores, após NDA." support="CAPEX, forecast de 7 anos, condições da rodada e retorno por sede, sempre com o cenário conservador ao lado do base. Acesso após qualificação e assinatura do NDA." />
        )}
        <div className="bloco">
          <InvestorForm />
        </div>
      </div>
    </Chapter>
  );
}
