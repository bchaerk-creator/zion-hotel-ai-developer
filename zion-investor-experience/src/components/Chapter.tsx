import type { ReactNode } from "react";
import type { Bg } from "@/lib/chapters";

const bgClass: Record<Bg, string> = {
  black: "bg-black tone-dark",
  moss: "bg-moss tone-dark",
  cream: "bg-cream tone-light",
  leaf: "bg-leaf tone-light",
  gold: "bg-gold tone-dark",
  photo: "bg-black tone-dark",
};

type Props = { id: string; number: string; title: string; bg: Bg; children: ReactNode; className?: string };

/** Uma ideia por tela. O header lê data-chapter para o indicador. */
export function Chapter({ id, number, title, bg, children, className = "" }: Props) {
  return (
    <section
      id={id}
      data-chapter={number}
      data-title={title}
      className={`relative ${bgClass[bg]} ${className}`}
      style={{ color: "var(--fg)" }}
    >
      {children}
    </section>
  );
}

export function ChapterLabel({ number, title }: { number: string; title: string }) {
  return (
    <p className="t-label mb-8">
      {number} · {title}
    </p>
  );
}
