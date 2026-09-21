import type { CapexData, ModelData, RaiseData, ReturnsData } from "@data/types";
import modelJson from "@data/model.json";
import capexJson from "@data/capex.json";
import raiseJson from "@data/raise.json";
import returnsJson from "@data/returns.json";

/**
 * Dados marcados investorOnly. Só a rota /investor importa este módulo.
 * A edição pública nunca chega aqui, por construção.
 */
export const model = modelJson as ModelData;
export const capex = capexJson as CapexData;
export const raise = raiseJson as RaiseData;
export const returns = returnsJson as ReturnsData;

for (const [name, d] of Object.entries({ model, capex, raise, returns })) {
  if (d.investorOnly !== true) throw new Error(`${name}.json precisa de investorOnly: true`);
}
