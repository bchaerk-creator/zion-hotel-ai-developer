/**
 * Tipos dos arquivos de /data. Fonte única: docs/MASTER.md.
 * Nenhum número vive em componente. Todo número tem sourceId, period e status.
 */

export type MetricStatus = "validated" | "estimate" | "pending";

export type Metric = {
  id: string;
  value: string;
  label: string;
  context?: string;
  sourceId: string;
  period: string;
  status: MetricStatus;
};

export type SourceKind =
  | "dre"
  | "system"
  | "company"
  | "crm"
  | "model"
  | "internal"
  | "public"
  | "external";

export type Source = {
  id: string;
  label: string;
  kind: SourceKind;
  date?: string;
  note?: string;
};

export type SourcesData = { sources: Source[] };

/* company.json */
export type MethodTrack = {
  id: "developer" | "operation";
  name: string;
  pillars: string[];
  certification: string;
};

export type CompanyData = {
  name: string;
  positioning: string;
  neverSay: string[];
  tagline: string;
  message: string;
  brandConcept: { name: string; description: string; note: string };
  story: string[];
  founder: {
    name: string;
    role: string;
    bio: string;
    portrait: { file: string | null; status: "pending" | "available" };
  };
  method: {
    name: string;
    description: string;
    tracks: MethodTrack[];
    rule: string;
  };
};

/* operations.json */
export type SiteProfile = {
  id: "urubici" | "florianopolis";
  name: string;
  state: string;
  start: number;
  land: string;
  concept: string;
  units: number;
  photo: string;
  operatingCompany: string;
};

export type OperationsData = {
  sites: SiteProfile[];
  perimeterNote: string;
  fy2025: { sourceId: string; period: string; reading: string; metrics: Metric[] };
  h12026: { sourceId: string; period: string; caveat: string; metrics: Metric[] };
};

/* revenue.json */
export type RevenuePeriod = {
  id: string;
  period: string;
  value: string;
  valueNumber: number;
  basis: string;
  sourceId: string;
  status: MetricStatus;
};

export type RevenueData = {
  asOf: string;
  periods: RevenuePeriod[];
  total: Metric;
  documented: Metric;
  doNotUse: { value: string; reason: string };
  timeline: { step: string; label: string; note: string }[];
};

/* brand.json */
export type BrandData = {
  sourceId: string;
  ratings: Metric[];
  audience: Metric[];
  channelEconomics: { metrics: Metric[]; reading: string };
};

/* model.json */
export type Assumption = { id: string; label: string; value: string; note?: string };

export type StaffingPlan = {
  units: number;
  roles: string[];
  monthlyPayroll: number;
  annualPayrollWithCharges: number;
  peakDailies: number;
  annualFixedCost: number;
};

export type ScenarioId = "conservative" | "base" | "optimistic";

export type Scenario = {
  id: ScenarioId;
  label: string;
  occupancy: string;
  grossRevenue: number;
  ebitda: number;
  ebitdaMargin: string;
  netIncome: number;
  yieldOnCapital: string;
  multiple7y: string;
  capitalReturnCycle: string;
};

export type ForecastRow = {
  year: number;
  occupancy: string;
  grossRevenue: number;
  ebitda: number;
  netIncome: number;
};

export type ModelData = {
  sourceId: string;
  units: number;
  assumptions: Assumption[];
  staffing: { plans: StaffingPlan[]; rule: string };
  year1: { scope: string; scenarios: Scenario[]; warning: string };
  forecast: {
    unit: string;
    format: string;
    scenarios: { id: ScenarioId; label: string; rows: ForecastRow[] }[];
    warning: string;
  };
  configuration: { recommendation: string; caveat: string };
  investorOnly: true;
};

/* capex.json */
export type CapexBlock = { id: string; label: string; total: number; perUnit: number | null; note?: string };

export type CapexData = {
  sourceId: string;
  units: number;
  currency: "BRL";
  blocks: CapexBlock[];
  implementationSubtotal: number;
  contingency: { rate: string; value: number };
  workingCapital: { perUnit: number; value: number };
  implementationTotal: { value: number; perUnit: number };
  fees: { label: string; value: number };
  siteWorks: { selectedTier: string; value: number; tiers: { id: string; label: string; value: number }[] };
  allIn: { value: number; perUnit: number };
  perKeyBySize: { units: number; value: number }[];
  marketReference: { label: string; range: string; buildTime: string; sourceId: string; status: MetricStatus };
  optionals: { id: string; label: string; perUnit: number }[];
  pending: string[];
  investorOnly: true;
};

/* program.json */
export type Destination = { name: string; state: string; note?: string };
export type Wave = { wave: number; year: number; destinations: Destination[] };
export type Corridor = { id: string; label: string; count: number };

export type ProgramData = {
  sourceId: string;
  totalDestinations: number;
  unitsPerSite: number;
  waves: Wave[];
  corridors: Corridor[];
  notes: string[];
  consolidated: {
    scenario: ScenarioId;
    year: number;
    sites: number;
    revenue: string;
    partnerResult: string;
    margin: string;
    collectionCoordination: { sitesUpTo: number; cost: string }[];
    note: string;
  };
};

/* raise.json */
export type Tranche = { id: "A" | "B" | "C"; value: string; milestone: string };

export type RaiseData = {
  sourceId: string;
  programCapex: Metric;
  cashNeed: { scenario: ScenarioId; label: string; peak: string; peakYear: number; backToZero: number }[];
  round: { value: string; sizedBy: string; selfFinancingShare: string };
  tranches: Tranche[];
  terms: { gracePerSite: string; distribution: string };
  investorOnly: true;
};

/* returns.json */
export type ReturnRow = { id: string; label: string; multiple7y: string; irr: string; isBenchmark: boolean };

export type ReturnsData = {
  sourceId: string;
  perSite: { id: ScenarioId; label: string; yieldOnCapital: string; multiple7y: string; capitalReturnCycle: string }[];
  comparison: ReturnRow[];
  honestyNote: string;
  forbiddenWord: string;
  investorOnly: true;
};

/* platform.json */
export type Company = {
  id: string;
  name: string;
  role: string;
  remuneration: string;
  takesInvestors: "never" | "yes" | "no" | "per-structure";
};

export type ZionFee = { id: string; label: string; value: number; nature: "one-off" | "annual" | "none" };

export type Valuation = { id: string; label: string; today: string | null; maturity: string };

export type VicePresidency = {
  id: string;
  label: string;
  annualCost: number;
  allocation: { collection: number; store: number; management: number };
};

export type PlatformData = {
  companies: Company[];
  outsidePerimeter: { name: string; site: string }[];
  outsidePerimeterNote: string;
  capitalModel: { name: string; principles: string[] };
  exclusivity: string;
  remunerationPerSite: { scope: string; sourceId: string; fees: ZionFee[]; note: string };
  valuation: { method: string; sourceId: string; status: MetricStatus; arms: Valuation[]; note: string };
  organization: {
    cluster: VicePresidency[];
    matureTotal: number;
    costByPhase: { sitesUpTo: number; cost: number }[];
    principle: string;
  };
  management: { margins: { sites: number; margin: string }[]; governance: string[] };
  store: { revenuePerSite: number; programRevenue: number; principle: string; thirdPartyTarget: string };
  reserved: string[];
};

/* landBank.json */
export type Layer = { id: string; label: string; hectares: number | null; share: string | null; note?: string };
export type Region = { id: string; label: string; hectares: number };
export type OpportunityStatus = "development" | "fundraising" | "analysis" | "analysis-formalizing";

export type Opportunity = {
  id: string;
  name: string;
  state: string;
  hectares: number | null;
  status: OpportunityStatus;
  statusLabel: string;
  facts: { label: string; value: string }[];
};

export type LandBankData = {
  sourceId: string;
  asOf: string;
  total: Metric;
  layers: Layer[];
  regions: Region[];
  regionReading: string;
  indicators: Metric[];
  pipeline: string[];
  opportunities: Opportunity[];
  module: {
    suites: number;
    hectares: number;
    origin: string;
    capacity: { modules: number; suites: number }[];
    note: string;
  };
  rules: string[];
};

/* market.json */
export type MarketData = {
  thesis: { id: string; label: string; text: string }[];
  numbers: Metric[];
  sustainability: { facts: string[]; certifications: string; carbon: string };
  publicCredit: { id: string; name: string; institution: string; terms: string[]; status: MetricStatus; sourceId: string }[];
  publicCreditNote: string;
};

/* documents.json */
export type DocumentStatus = "current" | "current-update-revenue" | "reserved" | "outdated";

export type KitDocument = {
  id: string;
  title: string;
  file: string | null;
  status: DocumentStatus;
  note?: string;
  dataRoom: boolean;
};

export type DocumentsData = { documents: KitDocument[]; statusLabels: Record<DocumentStatus, string> };

/* legal.json */
export type LegalData = {
  footer: string;
  footerNote: string;
  investorEditionLine: string;
  editions: { id: "public" | "investor"; label: string; rules: string[] }[];
  forbidden: { term: string; use: string }[];
  writing: string[];
};
