import type { PhotoRef } from "@/lib/photos";

type Veil = "none" | "hero" | "phrase" | "block";

const veilStyle: Record<Veil, string | undefined> = {
  none: undefined,
  hero: "linear-gradient(180deg, rgba(26,33,3,.5) 0%, rgba(26,33,3,.9) 100%)",
  phrase: "linear-gradient(180deg, rgba(26,33,3,.2) 0%, rgba(26,33,3,.85) 100%)",
  block: "rgba(26,33,3,.74)",
};

type Props = { photo: PhotoRef; veil?: Veil; className?: string; fill?: boolean; priority?: boolean };

/**
 * Foto com véu de MASTER 13.4. Sem o arquivo em public/photos, mostra um
 * placeholder escuro com o nome do arquivo, para a equipe saber o que falta.
 */
export function Photo({ photo, veil = "none", className = "", fill = false, priority = false }: Props) {
  const base = fill ? "absolute inset-0" : "relative w-full aspect-[4/3]";
  return (
    <div className={`${base} overflow-hidden bg-moss ${className}`} aria-hidden={photo.src ? undefined : true}>
      {photo.src ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={photo.src}
          alt={photo.alt}
          className="h-full w-full object-cover"
          loading={priority ? "eager" : "lazy"}
          decoding="async"
        />
      ) : (
        <div className="absolute inset-0 flex items-end p-5">
          <p className="t-source !no-underline text-sand/70">Foto a fornecer: {photo.key}.jpg</p>
        </div>
      )}
      {veil !== "none" && <div className="absolute inset-0" style={{ background: veilStyle[veil] }} />}
    </div>
  );
}
