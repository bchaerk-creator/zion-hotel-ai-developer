import { existsSync } from "node:fs";
import { join } from "node:path";

/** Fotos de MASTER 13.4. O arquivo entra em public/photos com o mesmo nome. */
export const photos = {
  aerea_mata: { file: "aerea_mata.jpg", alt: "Bubble isolada no meio da araucária, vista de drone" },
  aerea_zenital: { file: "aerea_zenital.jpg", alt: "Deck completo visto de cima: bubble, jacuzzi, rede e apoio" },
  aerea_noturna: { file: "aerea_noturna.jpg", alt: "Duas bubbles vistas de cima, à noite" },
  bubble_frontal: { file: "bubble_frontal.jpg", alt: "Bubble com o céu refletido" },
  bubble_deck: { file: "bubble_deck.jpg", alt: "Bubble sobre deck na mata, Urubici" },
  bubble_jacuzzi: { file: "bubble_jacuzzi.jpg", alt: "Bubble ensolarada com jacuzzi" },
  interior_ceu: { file: "interior_ceu.jpg", alt: "Interior da bubble com o céu na cúpula" },
  jacuzzi_mata: { file: "jacuzzi_mata.jpg", alt: "Deck com jacuzzi na mata atlântica" },
  jacuzzi_zenital: { file: "jacuzzi_zenital.jpg", alt: "Jacuzzi vista de cima" },
  flo_noturna: { file: "flo_noturna.jpg", alt: "Bubble iluminada com telescópio sob as estrelas" },
  flo_casal_deck: { file: "flo_casal_deck.jpg", alt: "Casal caminhando no deck, Florianópolis" },
  flo_casal_roupao: { file: "flo_casal_roupao.jpg", alt: "Casal de roupão diante da bubble" },
  flo_piscina: { file: "flo_piscina.jpg", alt: "Piscina com bandeja flutuante" },
  flo_deck_mata: { file: "flo_deck_mata.jpg", alt: "Deck na mata, Florianópolis" },
} as const;

export type PhotoKey = keyof typeof photos;

export type PhotoRef = { key: PhotoKey; src: string | null; alt: string };

/** Resolve no build. Sem o arquivo, o componente Photo mostra o placeholder. */
export function photo(key: PhotoKey): PhotoRef {
  const p = photos[key];
  const exists = existsSync(join(process.cwd(), "public", "photos", p.file));
  return { key, src: exists ? `/photos/${p.file}` : null, alt: p.alt };
}
