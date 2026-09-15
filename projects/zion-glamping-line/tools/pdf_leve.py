"""Gera a versão leve do Product Book (imagens recomprimidas, vetores intactos).
Uso: python3 tools/pdf_leve.py [entrada.pdf] [saida.pdf]
"""
import sys, pymupdf
src = sys.argv[1] if len(sys.argv) > 1 else "ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf"
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".pdf", "_leve.pdf")
doc = pymupdf.open(src)
doc.rewrite_images(dpi_threshold=120, dpi_target=110, quality=72, lossy=True, lossless=True)
doc.save(dst, garbage=4, deflate=True)
print(dst, round(__import__("os").path.getsize(dst) / 1e6, 1), "MB", doc.page_count, "páginas")
