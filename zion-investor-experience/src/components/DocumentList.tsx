import type { DocumentsData, KitDocument } from "@data/types";

type Props = { documents: KitDocument[]; statusLabels: DocumentsData["statusLabels"]; canDownload: boolean };

/** Tabela de documentos com ação à direita. Fase 1: sem download, o arquivo chega pelo data room. */
export function DocumentList({ documents, statusLabels, canDownload }: Props) {
  return (
    <div className="table-scroll">
      <table className="t-table w-full">
        <thead>
          <tr className="border-b" style={{ borderColor: "var(--line)" }}>
            <th scope="col" className="t-th py-3 pr-6 text-left font-medium" style={{ color: "var(--muted)" }}>Documento</th>
            <th scope="col" className="t-th py-3 pr-6 text-left font-medium" style={{ color: "var(--muted)" }}>Situação</th>
            <th scope="col" className="t-th py-3 text-right font-medium" style={{ color: "var(--muted)" }}>Acesso</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((d) => (
            <tr key={d.id} className="border-b" style={{ borderColor: "var(--line)" }}>
              <td className="py-4 pr-6">
                <span className="t-subtitle !text-[clamp(20px,1.8vw,24px)]">{d.title}</span>
                {d.note && <span className="mt-1 block text-[12px]" style={{ color: "var(--muted)" }}>{d.note}</span>}
              </td>
              <td className="py-4 pr-6 align-top" style={{ color: "var(--fg-2)" }}>{statusLabels[d.status]}</td>
              <td className="py-4 text-right align-top whitespace-nowrap">
                {canDownload && d.file ? (
                  <a href={`/documents/${d.file}`} className="t-table inline-flex min-h-12 items-center border px-5 hover:border-cream" style={{ borderColor: "var(--line)" }} download>
                    Baixar
                  </a>
                ) : (
                  <span className="t-source !no-underline">Pelo data room</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
