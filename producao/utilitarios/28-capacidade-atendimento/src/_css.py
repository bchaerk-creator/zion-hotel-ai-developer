import pathlib
R = pathlib.Path(__file__).resolve().parents[4]
FONTS = R / "docs/assets/fonts"
CSS = f"""
@font-face {{ font-family: Cormorant; src: url('{(FONTS/'cormorant.woff2').as_uri()}'); }}
@font-face {{ font-family: Aventa; src: url('{(FONTS/'aventa.woff2').as_uri()}'); }}
:root {{ --musgo:#1B2117; --creme:#FEF5F0; --areia:#DED6BF; --terra:#8B714E; --dourado:#C9B37E; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Aventa, Arial, sans-serif; color: var(--musgo); background: var(--creme); font-size: 11pt; line-height: 1.45; }}
h1, h2, h3 {{ font-family: Cormorant, Georgia, serif; font-weight: 600; margin: 0 0 .4em; line-height: 1.1; }}
h1 {{ font-size: 40pt; }} h2 {{ font-size: 26pt; }} h3 {{ font-size: 15pt; margin-top: .8em; }}
.kicker {{ font-size: 8.5pt; letter-spacing: .18em; text-transform: uppercase; color: var(--terra); font-weight: 700; margin-bottom: 6px; }}
.page {{ width: 210mm; height: 297mm; padding: 18mm 18mm 16mm; position: relative; overflow: hidden; page-break-after: always; background: var(--creme); }}
.page:last-child {{ page-break-after: auto; }}
.foot {{ position: absolute; bottom: 9mm; left: 18mm; right: 18mm; font-size: 7.5pt; color: #6b6656; display: flex; justify-content: space-between; border-top: 1px solid var(--areia); padding-top: 4px; }}
.box {{ background: #fff; border: 1px solid var(--areia); border-radius: 10px; padding: 12px 14px; margin: 10px 0; }}
.box.ex {{ border-left: 5px solid var(--dourado); }} .box.alerta {{ border-left: 5px solid #A0522D; }}
.tag {{ display:inline-block; font-size: 8pt; font-weight:700; padding: 2px 8px; border-radius: 99px; background: var(--musgo); color: var(--creme); }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
th {{ background: var(--musgo); color: var(--creme); text-align: left; padding: 5px 7px; font-weight: 600; }}
td {{ border-bottom: 1px solid var(--areia); padding: 5px 7px; vertical-align: top; }}
.ok {{ background:#C8E6C0; }} .pend {{ background:#F4C7C3; font-weight:700; }}
ol.passos li {{ margin: 0 0 6px; }} .linha {{ border-bottom: 1px solid #b9b19b; height: 22px; }}
.fict {{ color:#A0522D; font-weight:700; font-size: 8.5pt; }}
.bolha {{ background:#E7F3E2; border-radius: 10px 10px 10px 2px; padding: 9px 12px; font-size: 10pt; margin: 6px 0; }}
mark {{ background:#F4C7C3; font-weight:700; }}
"""
