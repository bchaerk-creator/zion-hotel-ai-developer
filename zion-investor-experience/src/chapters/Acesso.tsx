import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { InvestorForm } from "@/components/InvestorForm";

export function Acesso() {
  return (
    <Chapter id="acesso" number="13" title="Acesso para investidores" bg="moss">
      <div className="wrap chapter">
        <ChapterLabel number="13" title="Acesso para investidores" />
        <Statement text="Edição para investidores, após NDA." support="CAPEX, forecast de 7 anos, condições da rodada e retorno por sede, sempre com o cenário conservador ao lado do base. Acesso após qualificação e assinatura do NDA." />
        <div className="bloco">
          <InvestorForm />
        </div>
      </div>
    </Chapter>
  );
}
