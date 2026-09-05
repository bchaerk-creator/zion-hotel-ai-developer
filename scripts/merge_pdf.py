#!/usr/bin/env python3
"""Une os PDFs de assinatura num pacote único, com índice navegável.

Uso: merge_pdf.py saida.pdf entrada1.pdf entrada2.pdf ...
"""
import sys

import pymupdf


def merge(saida, entradas):
    doc = pymupdf.open()
    marcadores = []
    for nome in entradas:
        parte = pymupdf.open(nome)
        titulo = parte[0].get_text().strip().split("\n")[0][:70]
        marcadores.append([1, titulo, len(doc) + 1])
        doc.insert_pdf(parte)
        parte.close()
    doc.set_toc(marcadores)
    doc.save(saida, deflate=True, garbage=3)
    print(f"gerado: {saida} ({doc.page_count} páginas)")


if __name__ == "__main__":
    merge(sys.argv[1], sys.argv[2:])
