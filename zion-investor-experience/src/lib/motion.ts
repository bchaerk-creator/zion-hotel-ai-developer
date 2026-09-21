/**
 * Movimento de MASTER 13.6. Só hero e frases de impacto animam.
 * As propriedades initial e animate são sempre as mesmas no servidor e no
 * cliente, para o HTML estático não ficar preso em opacidade zero. Com
 * prefers-reduced-motion, a duração cai a zero e o conteúdo aparece pronto.
 */
const ease = [0.16, 1, 0.3, 1] as const;

export const heroPhoto = (reduce: boolean) => ({
  initial: { scale: reduce ? 1 : 1.06 },
  animate: { scale: 1 },
  transition: { duration: reduce ? 0 : 5.5, ease },
});

export const heroLine = (index: number, reduce: boolean) => ({
  initial: { opacity: 0, y: 28 },
  animate: { opacity: 1, y: 0 },
  transition: reduce ? { duration: 0 } : { duration: 1.2, delay: 0.6 + index * 0.35, ease },
});

export const statement = (reduce: boolean) => ({
  initial: { opacity: 0, y: 22 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.2 },
  transition: reduce ? { duration: 0 } : { duration: 1.6, ease },
});
