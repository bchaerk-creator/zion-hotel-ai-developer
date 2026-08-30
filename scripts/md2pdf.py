#!/usr/bin/env python3
"""Gera o PDF de leitura/assinatura dos documentos jurídicos em Markdown.

Mesmo subconjunto de Markdown do md2docx.py, renderizado via PyMuPDF Story.
Uso: md2pdf.py entrada.md saida.pdf "Título do rodapé"
"""
import html as html_mod
import re
import sys

import pymupdf

CSS = """
body { font-family: sans-serif; font-size: 9.5px; color: #0A0A0A; line-height: 1.45; }
h1 { font-size: 16px; text-align: center; margin: 14px 0 10px 0; }
h2 { font-size: 12px; color: #8A6F1F; margin: 16px 0 6px 0; }
h3 { font-size: 10.5px; margin: 12px 0 5px 0; }
p  { margin: 0 0 6px 0; text-align: justify; }
ul, ol { margin: 0 0 6px 14px; }
li { margin: 0 0 3px 0; }
blockquote { margin: 4px 0 8px 12px; font-style: italic; font-size: 9px; color: #444444; }
table { width: 100%; margin: 4px 0 10px 0; }
th { background-color: #1C1C1C; color: #FFFFFF; font-size: 8.5px; padding: 4px; text-align: left; }
td { border: 0.5px solid #BBBBBB; font-size: 8.5px; padding: 4px; vertical-align: top; }
hr { margin: 10px 0; }
"""


def inline(text):
    text = html_mod.escape(text).replace("&lt;br&gt;", "<br>")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def to_html(md):
    lines = md.split("\n")
    out, i, list_open = [], 0, None
    while i < len(lines):
        stripped = lines[i].strip()

        if list_open and not re.match(r"^([-*]|\d+\.) ", stripped):
            out.append(f"</{list_open}>")
            list_open = None

        if not stripped or stripped == "<br>":
            i += 1
            continue

        if stripped == "---":
            out.append('<p style="color:#C9A84C">' + "_" * 96 + "</p>")
            i += 1
            continue

        if (
            stripped.startswith("|")
            and i + 1 < len(lines)
            and lines[i + 1].strip().startswith("|")
            and set(lines[i + 1].strip().replace("|", "").replace(" ", "")) <= {"-", ":"}
        ):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            head, body = rows[0], rows[2:]
            cells = "".join(f"<th>{inline(c)}</th>" for c in head)
            out.append(f"<table><tr>{cells}</tr>")
            for row in body:
                cells = "".join(f"<td>{inline(c)}</td>" for c in row)
                out.append(f"<tr>{cells}</tr>")
            out.append("</table>")
            continue

        if stripped.startswith("#"):
            level = min(len(stripped) - len(stripped.lstrip("#")), 3)
            out.append(f"<h{level}>{inline(stripped.lstrip('# ').strip())}</h{level}>")
            i += 1
            continue

        if stripped.startswith("> "):
            out.append(f"<blockquote>{inline(stripped[2:])}</blockquote>")
            i += 1
            continue

        match = re.match(r"^([-*]|\d+\.) ", stripped)
        if match:
            tag = "ul" if match.group(1) in "-*" else "ol"
            if list_open != tag:
                if list_open:
                    out.append(f"</{list_open}>")
                out.append(f"<{tag}>")
                list_open = tag
            item = re.sub(r"^([-*]|\d+\.) ", "", stripped)
            out.append(f"<li>{inline(item)}</li>")
            i += 1
            continue

        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    if list_open:
        out.append(f"</{list_open}>")
    return "".join(out)


def render(md_path, pdf_path, footer_text):
    md = open(md_path, encoding="utf-8").read()
    story = pymupdf.Story(html=to_html(md), user_css=CSS)
    writer = pymupdf.DocumentWriter(pdf_path)
    frame = pymupdf.Rect(62, 62, 533, 770)
    more, page = 1, 0
    while more:
        page += 1
        device = writer.begin_page(pymupdf.paper_rect("a4"))
        more, _ = story.place(frame)
        story.draw(device)
        writer.end_page()
    writer.close()

    doc = pymupdf.open(pdf_path)
    for number, pg in enumerate(doc, start=1):
        pg.draw_line((62, 782), (533, 782), color=(0.79, 0.66, 0.30), width=0.6)
        pg.insert_text((62, 795), footer_text, fontsize=7, color=(0.35, 0.35, 0.35))
        pg.insert_text((505, 795), f"{number} / {doc.page_count}", fontsize=7, color=(0.35, 0.35, 0.35))
    doc.save(pdf_path, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    print(f"gerado: {pdf_path} ({doc.page_count} páginas)")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], sys.argv[3])
