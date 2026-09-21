/** Traço fino do globo do guia de marca Zion. Só linhas, sem preenchimento. */
export function Globe({ className = "" }: { className?: string }) {
  return (
    <svg className={`globe ${className}`} viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden fill="none" stroke="currentColor" strokeWidth="1">
      <circle cx="600" cy="400" r="420" />
      <ellipse cx="600" cy="400" rx="420" ry="120" />
      <ellipse cx="600" cy="400" rx="150" ry="420" />
      <line x1="60" y1="400" x2="1140" y2="400" />
      <line x1="600" y1="-40" x2="600" y2="840" />
    </svg>
  );
}
