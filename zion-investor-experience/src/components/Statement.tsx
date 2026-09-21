"use client";

import { motion, useReducedMotion } from "framer-motion";
import { statement } from "@/lib/motion";

type Props = { text: string; support?: string; as?: "h2" | "p"; className?: string };

/** Frase em caixa alta, serifa leve, até três linhas. Nada além de uma linha de apoio. */
export function Statement({ text, support, as = "h2", className = "" }: Props) {
  const reduce = useReducedMotion();
  const Tag = as;
  return (
    <motion.div className={className} {...statement(!!reduce)}>
      <Tag className="t-statement max-w-[16ch]">{text}</Tag>
      {support && <p className="t-support mt-8" style={{ color: "var(--fg-2)" }}>{support}</p>}
    </motion.div>
  );
}
