import base from "./vitest.config.mjs";
export default { ...base, test: { ...base.test, coverage: { enabled: true, reportOnFailure: true, provider: "v8", reporter: ["json-summary"], include: ["src/calc/**/*.ts", "src/exercicios/*-calculo.ts"], reportsDirectory: "./cobertura" } } };
