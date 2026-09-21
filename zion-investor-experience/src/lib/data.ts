import type {
  BrandData, CompanyData, DocumentsData, LandBankData, LegalData, MarketData,
  OperationsData, PlatformData, ProgramData, RevenueData, Source, SourcesData,
} from "@data/types";
import companyJson from "@data/company.json";
import operationsJson from "@data/operations.json";
import revenueJson from "@data/revenue.json";
import brandJson from "@data/brand.json";
import programJson from "@data/program.json";
import platformJson from "@data/platform.json";
import landBankJson from "@data/landBank.json";
import marketJson from "@data/market.json";
import documentsJson from "@data/documents.json";
import sourcesJson from "@data/sources.json";
import legalJson from "@data/legal.json";

/**
 * Camada pública de dados. Os arquivos com investorOnly (model, capex, raise,
 * returns) não são importados aqui de propósito: a edição pública não pode
 * renderizar nenhum dado de retorno.
 */
export const company = companyJson as CompanyData;
export const operations = operationsJson as OperationsData;
export const revenue = revenueJson as RevenueData;
export const brand = brandJson as BrandData;
export const program = programJson as ProgramData;
export const platform = platformJson as PlatformData;
export const landBank = landBankJson as LandBankData;
export const market = marketJson as MarketData;
export const documents = documentsJson as DocumentsData;
export const legal = legalJson as LegalData;

const sourceMap = new Map<string, Source>((sourcesJson as SourcesData).sources.map((s) => [s.id, s]));

export function getSource(id: string): Source {
  const s = sourceMap.get(id);
  if (!s) throw new Error(`Fonte desconhecida: ${id}`);
  return s;
}
