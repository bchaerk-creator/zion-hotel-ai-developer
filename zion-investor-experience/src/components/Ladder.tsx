/** Lista vertical em serifa grande, do mais apagado ao mais escuro. */
export function Ladder({ rungs }: { rungs: string[] }) {
  const n = rungs.length;
  return (
    <ol className="t-list">
      {rungs.map((r, i) => (
        <li
          key={r}
          className="border-b py-4"
          style={{ borderColor: "var(--line)", opacity: 0.35 + (0.65 * (i + 1)) / n }}
        >
          {r}
        </li>
      ))}
    </ol>
  );
}
