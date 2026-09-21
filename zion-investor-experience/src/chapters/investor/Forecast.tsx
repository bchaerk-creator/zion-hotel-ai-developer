import { Chapter, ChapterLabel } from "@/components/Chapter";
import { Statement } from "@/components/Statement";
import { ScenarioTable } from "@/components/ScenarioTable";
import { ForecastTable } from "@/components/ForecastTable";
import { model } from "@/lib/data-investor";

export function Forecast() {
  return (
    <Chapter id="forecast" number="16" title="Forecast" bg="black">
      <div className="wrap chapter">
        <ChapterLabel number="16" title="Forecast" />
        <Statement text="Três cenários, sete anos." support={`Ocupação de ${model.year1.scenarios[0].occupancy} a ${model.year1.scenarios[2].occupancy} no primeiro ano. ${model.forecast.warning}`} />
        <div className="bloco">
          <ScenarioTable scenarios={model.year1.scenarios} showReturns sourceId={model.sourceId} period="Ano 1" />
        </div>
        <div className="bloco">
          <p className="t-label mb-8">Forecast de 7 anos, {model.forecast.format}</p>
          <ForecastTable forecast={model.forecast} sourceId={model.sourceId} />
        </div>
      </div>
    </Chapter>
  );
}
