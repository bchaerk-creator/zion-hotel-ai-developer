import type { LandBankData } from "@data/types";
import { intBR } from "@/lib/format";

/** O único fundo dourado de toda a experiência. */
export function ModuleBlock({ module }: { module: LandBankData["module"] }) {
  return (
    <div className="bg-gold tone-dark text-cream">
      <div className="wrap chapter grid gap-12 md:grid-cols-2 md:gap-[6vw]">
        <div>
          <h2 className="t-chapter !text-[clamp(40px,4.8vw,76px)]">
            Um módulo Zion.
            <br />
            {module.suites} suítes.
            <br />
            {String(module.hectares).replace(".", ",")} hectares.
          </h2>
          <p className="t-support mt-8 text-cream/85">{module.origin}</p>
        </div>
        <div className="self-end">
          <p className="t-label !text-cream/80">Capacidade do território</p>
          <div className="table-scroll mt-4">
            <table className="t-table w-full">
              <thead>
                <tr className="border-b border-cream/30">
                  <th scope="col" className="t-th py-3 text-left font-medium text-cream/80">Módulos</th>
                  {module.capacity.map((c) => (
                    <th key={c.modules} scope="col" className="t-th py-3 text-right font-medium text-cream/80">
                      {c.modules} módulos
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-cream/30">
                  <td className="py-3">Suítes</td>
                  {module.capacity.map((c) => (
                    <td key={c.modules} className="py-3 text-right tabular-nums">{intBR(c.suites)}</td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-[12px] text-cream/80">{module.note}</p>
        </div>
      </div>
    </div>
  );
}
