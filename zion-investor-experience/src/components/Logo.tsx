type Variant = "monogram" | "wordmark" | "lockup";

/** Proporção largura/altura de cada arquivo em public/brand, medida no build dos assets. */
const ratio: Record<Variant, number> = {monogram: 1.0, wordmark: 4.02, lockup: 3.703};

/**
 * Marca oficial como máscara: a cor vem de currentColor, então o logo
 * segue o token do contexto (Camel no cabeçalho, creme sobre foto).
 */
export function Logo({ variant = "wordmark", height = 18, className = "", label = "Zion" }: { variant?: Variant; height?: number; className?: string; label?: string }) {
  const url = `url(/brand/${variant}.png)`;
  return (
    <span
      role="img"
      aria-label={label}
      className={`inline-block bg-current ${className}`}
      style={{
        height,
        width: Math.round(height * ratio[variant]),
        WebkitMaskImage: url,
        maskImage: url,
        WebkitMaskSize: "contain",
        maskSize: "contain",
        WebkitMaskRepeat: "no-repeat",
        maskRepeat: "no-repeat",
        WebkitMaskPosition: "left center",
        maskPosition: "left center",
      }}
    />
  );
}
