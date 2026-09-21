"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Logo } from "./Logo";

type Props = { total: number; initial: { number: string; title: string }; accessHref: string };

/** Faixa fixa preta a 88% com desfoque, indicador de capítulo e fio dourado de progresso. */
export function Header({ total, initial, accessHref }: Props) {
  const [current, setCurrent] = useState(initial);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const sections = Array.from(document.querySelectorAll<HTMLElement>("[data-chapter]"));
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) {
          const el = visible.target as HTMLElement;
          setCurrent({ number: el.dataset.chapter ?? "", title: el.dataset.title ?? "" });
        }
      },
      { rootMargin: "-45% 0px -45% 0px", threshold: [0, 0.1, 0.5] },
    );
    sections.forEach((s) => observer.observe(s));

    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      setProgress(max > 0 ? Math.min(1, h.scrollTop / max) : 0);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  return (
    <header className="fixed inset-x-0 top-0 z-50 bg-black/88 backdrop-blur-md tone-dark">
      <div className="absolute inset-x-0 top-0 h-[2px] bg-line-dark" aria-hidden>
        <div className="h-full bg-gold" style={{ width: `${progress * 100}%` }} />
      </div>
      <div className="wrap flex h-16 items-center justify-between gap-6">
        <Link href="/" className="flex items-center text-gold hover:text-cream" aria-label="Zion, início">
          <Logo variant="wordmark" height={16} />
        </Link>
        <div className="flex items-baseline gap-4">
          <p className="t-table text-cream" aria-live="polite">
            {current.number} <span className="text-muted-dark">/ {String(total).padStart(2, "0")}</span>
          </p>
          <p className="t-table hidden text-sand sm:block">{current.title}</p>
          <Link href={accessHref} className="t-label hidden md:block hover:text-cream">
            Acesso
          </Link>
        </div>
      </div>
    </header>
  );
}
