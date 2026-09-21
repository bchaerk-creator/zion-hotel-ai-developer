"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import type { PhotoRef } from "@/lib/photos";
import { heroLine, heroPhoto } from "@/lib/motion";
import { Photo } from "./Photo";
import { Globe } from "./Globe";

type Cta = { label: string; href: string };
type Props = { photo: PhotoRef; eyebrow: string; topline?: string; lines: [string, string, string, string]; primary: Cta; secondary: Cta };

export function HeroPhoto({ photo, eyebrow, topline, lines, primary, secondary }: Props) {
  const reduce = useReducedMotion();
  return (
    <div className="relative min-h-[100svh] overflow-hidden tone-dark">
      <motion.div className="absolute inset-0" {...heroPhoto(!!reduce)}>
        <Photo photo={photo} veil="hero" fill priority />
      </motion.div>
      <Globe />
      <div className="wrap relative flex min-h-[100svh] flex-col justify-end pb-[10vh] pt-32">
        {topline && <p className="t-label mb-3">{topline}</p>}
        <p className="t-table mb-6 text-sand">{eyebrow}</p>
        <h1 className="t-hero text-cream">
          {lines.map((line, i) => (
            <motion.span key={line} className="block" {...heroLine(i, !!reduce)}>
              {line}
            </motion.span>
          ))}
        </h1>
        <div className="mt-10 flex flex-wrap gap-4">
          <Link
            href={primary.href}
            className="t-table inline-flex min-h-12 items-center bg-cream px-7 font-medium text-ink hover:bg-sand"
          >
            {primary.label}
          </Link>
          <Link
            href={secondary.href}
            className="t-table inline-flex min-h-12 items-center border border-sand px-7 text-sand hover:border-cream hover:text-cream"
          >
            {secondary.label}
          </Link>
        </div>
      </div>
    </div>
  );
}
