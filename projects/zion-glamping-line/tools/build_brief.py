# -*- coding: utf-8 -*-
"""Converte documentos Markdown da pasta 00_BRIEFING (brief, revisões, checklists) em HTML A4 no padrão Zion, para PDF com export_pdf.js.
Suporta: títulos #/##/###, parágrafos, listas com '-', listas numeradas, tabelas |a|b|, **negrito**, *itálico*, `código`.
Uso: python3 build_brief.py 00_BRIEFING/ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.md"""
import html, os, re, sys
from svgkit import zion_mark_html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    s = s.replace("⚠️", '<span class="warn">⚠️</span>')
    return s

def md_to_html(md):
    out = []; lines = md.splitlines(); i = 0; title = ""
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            title = ln[2:].strip(); out.append(f"<h1>{inline(title)}</h1>"); i += 1; continue
        if ln.startswith("## "): out.append(f"<h2>{inline(ln[3:])}</h2>"); i += 1; continue
        if ln.startswith("### "): out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells): rows.append(cells)
                i += 1
            head = rows[0]; body = rows[1:]
            out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</table>")
            continue
        if re.match(r"^\s*- ", ln):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*- ", lines[i]): out.append(f"<li>{inline(lines[i].strip()[2:])}</li>"); i += 1
            out.append("</ul>"); continue
        if re.match(r"^\d+\. ", ln):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                item = re.sub(r"^\d+\. ", "", lines[i]); out.append(f"<li>{inline(item)}</li>"); i += 1
            out.append("</ol>"); continue
        if ln.strip() == "": i += 1; continue
        par = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")) and not re.match(r"^\d+\. ", lines[i]): par.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(par))}</p>")
    return title, "\n".join(out)

CSS = """
@page{size:A4;margin:16mm 14mm 18mm} body{font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:#1B2117;background:#FEF5F0;margin:0;padding:18mm 16mm;font-size:10.5px;line-height:1.5}
.brand{display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.4em;font-size:22px;margin-bottom:2px} .brand .sub{display:block;font-weight:400;font-size:8.5px;letter-spacing:.3em;color:#8B714E}
h1{font-size:24px;letter-spacing:.22em;font-weight:300;margin:26px 0 8px;text-transform:uppercase} h2{font-size:12px;letter-spacing:.25em;color:#8B714E;margin:22px 0 8px;text-transform:uppercase;page-break-after:avoid}
h3{font-size:11px;letter-spacing:.15em;margin:14px 0 6px} p{margin:0 0 8px} code{font-family:Menlo,Consolas,monospace;font-size:9.5px;background:#F3EBE3;padding:0 3px}
table{width:100%;border-collapse:collapse;margin:6px 0 12px;font-size:9.4px;page-break-inside:auto} tr{page-break-inside:avoid} th,td{border-bottom:1px solid #DED6BF;padding:4px 6px;text-align:left;vertical-align:top} th{font-weight:600;background:#F3EBE3;font-size:8.6px;letter-spacing:.08em;text-transform:uppercase}
ul,ol{margin:0 0 10px 18px;padding:0} li{margin:0 0 4px} .warn{color:#8B714E} .foot{margin-top:26px;padding-top:8px;border-top:1px solid #DED6BF;font-size:8px;letter-spacing:.2em;color:#8B714E;display:flex;justify-content:space-between}
"""

def build(path):
    md = open(path, encoding="utf-8").read(); title, body = md_to_html(md)
    code = os.path.basename(path).split("_")[0]
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>
<div class="brand">{zion_mark_html('30px', color='#1B2117')}<span>ZION<span class="sub">GLAMPING COLLECTION · CABIN DESIGN &amp; ENGINEERING SYSTEM</span></span></div>
{body}
<div class="foot"><span>ZION GLAMPING · {html.escape(code)}</span><span>{html.escape(title)}</span><span>UNIDADE: MM · 2026</span></div></body></html>"""
    out = os.path.splitext(path)[0] + ".html"; open(out, "w", encoding="utf-8").write(doc); print("html ->", out); return out

if __name__ == "__main__":
    for p in sys.argv[1:] or [os.path.join(ROOT, "00_BRIEFING", "ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.md")]:
        build(p if os.path.isabs(p) else os.path.join(ROOT, p))
