# Coleta os efeitos sonoros que a cena registra (window.SFX) percorrendo a aula a cada 0,25 s, numa única sessão.
# Uso: python3 engine/sfxpass.py <pasta_da_aula>   (rodar a partir da raiz do projeto, onde fica node_modules)
import json, os, sys, http.server, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); V = sys.argv[1].strip('/')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8852), functools.partial(Q, directory=ROOT)); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None, args=["--use-angle=swiftshader","--enable-unsafe-swiftshader"]); pg = b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(f"http://127.0.0.1:8852/{V}/scene.html"); pg.wait_for_function("window.ready===true", timeout=120000)
    T = pg.evaluate("window.TOTAL"); t = 0.0
    while t < T: pg.evaluate(f"render({t})"); t += 0.25
    ev = pg.evaluate("window.SFX"); json.dump(ev, open(f"{V}/sfx_all.json","w")); print(len(ev), T); b.close()
