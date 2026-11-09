"""Recalcula a planilha EXEMPLO da Ferramenta 05 no LibreOffice (cópia temporária) e imprime o resumo em JSON.
Somente leitura: o arquivo original não é alterado. Uso: python3 -I f05_recalc.py <xlsx>"""
import json, subprocess, sys, tempfile, pathlib, shutil
from openpyxl import load_workbook

orig = pathlib.Path(sys.argv[1])
tmp = pathlib.Path(tempfile.mkdtemp())
src = tmp / "in.xlsx"; shutil.copy(orig, src)
out = tmp / "out"; out.mkdir()
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(out), str(src)],
               check=True, capture_output=True, timeout=180)
wb = load_workbook(out / "in.xlsx", data_only=True)
rot = {"Subtotal dos itens": "subtotal", "Reserva para imprevistos": "reserva", "Total com reserva": "total",
       "Verba disponível": "verba", "Diferença (verba − total com reserva)": "diferenca", "Leitura": "leitura"}
res = {}
for ws in wb.worksheets:
    for row in ws.iter_rows(min_col=1, max_col=2):
        a, b = row[0].value, row[1].value
        if isinstance(a, str) and a.strip() in rot and rot[a.strip()] not in res:
            res[rot[a.strip()]] = b
print(json.dumps(res, ensure_ascii=False))
