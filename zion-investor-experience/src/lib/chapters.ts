export type Bg = "black" | "moss" | "cream" | "leaf" | "gold" | "photo";

export type ChapterMeta = { id: string; number: string; title: string; bg: Bg };

/** Edição pública, indicador "/ 13". Títulos em português, como o site será lido. */
export const publicChapters: ChapterMeta[] = [
  { id: "intro", number: "00", title: "Introdução", bg: "photo" },
  { id: "oportunidade", number: "01", title: "A oportunidade", bg: "black" },
  { id: "mercado", number: "02", title: "O mercado", bg: "cream" },
  { id: "brasil", number: "03", title: "Brasil", bg: "cream" },
  { id: "fundador", number: "04", title: "O fundador", bg: "black" },
  { id: "prova", number: "05", title: "A prova", bg: "moss" },
  { id: "destinos", number: "06", title: "Destinos", bg: "photo" },
  { id: "ecossistema", number: "07", title: "Ecossistema", bg: "black" },
  { id: "land-bank", number: "08", title: "Land bank", bg: "black" },
  { id: "desenvolvimento", number: "09", title: "Desenvolvimento", bg: "leaf" },
  { id: "capital", number: "10", title: "O capital", bg: "black" },
  { id: "estrutura", number: "11", title: "Estrutura jurídica", bg: "cream" },
  { id: "visao", number: "12", title: "A visão", bg: "black" },
  { id: "acesso", number: "13", title: "Acesso para investidores", bg: "moss" },
];

export const PUBLIC_TOTAL = 13;

/** Edição para investidores, indicador "/ 21". Capítulos 00 a 12 iguais à pública. */
export const investorChapters: ChapterMeta[] = [
  ...publicChapters.slice(0, 13),
  { id: "programa", number: "13", title: "O programa", bg: "black" },
  { id: "sede", number: "14", title: "Uma sede", bg: "cream" },
  { id: "capex", number: "15", title: "CAPEX", bg: "black" },
  { id: "forecast", number: "16", title: "Forecast", bg: "black" },
  { id: "captacao", number: "17", title: "A captação", bg: "moss" },
  { id: "retorno", number: "18", title: "O retorno", bg: "black" },
  { id: "valor", number: "19", title: "Zion e valor", bg: "cream" },
  { id: "documentos", number: "20", title: "Documentos", bg: "black" },
  { id: "acesso", number: "21", title: "Próximo passo", bg: "moss" },
];

export const INVESTOR_TOTAL = 21;
