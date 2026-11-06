import sys, os, http.server, threading, functools, time
from playwright.sync_api import sync_playwright
ROOT=os.getcwd(); V=sys.argv[1].strip("/"); D=os.path.join(ROOT,V); PORT=int(os.environ.get("PORT","8811"))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(("127.0.0.1",PORT),functools.partial(Q,directory=ROOT));threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None, args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"]);pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.on("pageerror",lambda e:print("PAGEERR",e))
    pg.goto(f"http://127.0.0.1:{PORT}/{V}/scene.html");pg.wait_for_function("window.ready===true",timeout=90000)
    T=pg.evaluate("window.TOTAL")
    if sys.argv[2]=="test":
        os.makedirs(D+"/test",exist_ok=True)
        for ts in sys.argv[3:]:
            pg.evaluate(f"render({ts})");pg.screenshot(path=f"{D}/test/t{float(ts):06.2f}.jpg",type="jpeg",quality=85)
        print("ok",T)
    else:
        a,bb=(int(sys.argv[3]),int(sys.argv[4])) if len(sys.argv)>4 else (0,int(T*30))
        bb=min(bb,int(T*30));os.makedirs(D+"/out",exist_ok=True);t0=time.time()
        for i in range(a,bb):
            pg.evaluate(f"render({i/30})");pg.screenshot(path=f"{D}/out/{i+1:05d}.jpg",type="jpeg",quality=92)
            if i%150==0:print(i,bb,round(time.time()-t0),flush=True)
        print("done",T)
    b.close()
